# How pGenie Works

This page explains pGenie's internal architecture so you can understand what happens when you run `pgn generate` and why the tool is designed the way it is.

---

## The Pipeline

Running `pgn generate` triggers the following stages:

```
Migrations (SQL)  ──┐
                    ├──▶  PostgreSQL analysis environment  ──▶  Schema + signature analysis  ──▶  Dhall codegen  ──▶  Artifacts
Queries (SQL)     ──┘
```

### 1. Analysis environment startup

By default, pGenie uses [Testcontainers](https://testcontainers.com/) to spin up a disposable PostgreSQL container on the fly. This is why Docker must be running before you invoke `pgn generate` in Docker execution mode. The container runs the major PostgreSQL version configured in `project1.pgn.yaml` (or PostgreSQL 18 if you do not set one).

When you pass `--database-url`, pGenie switches to live instance mode instead. In that mode it connects to the running PostgreSQL server, checks that the server's major version matches the `postgres` field in `project1.pgn.yaml`, creates a temporary database there for analysis, and drops it afterwards.

### 2. Schema application

All `.sql` files in your `migrations/` directory are applied to the temporary analysis database **in natural sort order** by filename. Natural sorting handles embedded numbers correctly — `migration-10.sql` is applied after `migration-9.sql`. This means your migrations must be named so that natural sorting produces the correct execution order (e.g. `1.sql`, `2.sql`, …, or `001.sql`, `002.sql`, …).

Once applied, the temporary database holds the exact schema your queries will run against.

### 3. Query analysis

For each `.sql` file in `queries/`, pGenie:

1. Prepares the statement against the live PostgreSQL instance using the extended query protocol. PostgreSQL's `DescribeStatement` message returns the OIDs of all parameter types and result columns.
2. Resolves each OID to a full type description - including composite type fields, enumeration labels, and array element types - by querying the system catalog (`pg_type`, `pg_attribute`, etc.).
3. Determines parameter nullability by consulting the schema and running the query with `NULL` supplied to each parameter and analysing the errors.
4. Compares the freshly-resolved signature against the existing **signature file** (`.sig1.pgn.yaml`) alongside the `.sql` file, if one exists. If the signatures are compatible (or no sig file exists yet), generation continues; if they differ, the build fails, forcing you to acknowledge the change. When no signature file exists, pGenie writes one with the inferred types. Signature files are intended to be committed alongside your SQL and edited by hand when you want to tighten constraints such as parameter nullability. To force pGenie to regenerate a signature file from scratch, delete it and re-run `pgn generate`.

### 4. Custom type signature validation

After analysing the queries, pGenie collects the custom PostgreSQL types they reference. For every referenced enum or composite type, it writes or validates a custom-type signature file under `types/<schema>/`.

- **Enums** record the ordered list of PostgreSQL labels.
- **Composites** record the field names, field types, and nullability-related constraints.
- **Domains** do not get a separate custom-type signature file yet.

As with query signature files, pGenie never silently overwrites an existing custom-type signature file.

### 5. Code generation

pGenie loads the code generators configured in your `project1.pgn.yaml`, if any. Each generator is a [Dhall](https://dhall-lang.org/) program referenced by URL (e.g. a raw GitHub URL). The generator receives a structured description of your entire project - schema, queries, type information - and produces a tree of output files.

Dhall is used for code generators because it is:

- **Hermetic**: Dhall expressions are pure and total. No side effects, no I/O, no hidden state.
- **Composable**: Generators can import shared utilities and templates.
- **Cacheable**: Dhall expressions are content-addressed. A generator at a pinned URL is evaluated once, its output hash is stored in `freeze1.pgn.yaml` and is used as a cache key for subsequent runs.
- **Secure**: Since Dhall cannot perform arbitrary I/O, you can safely run generators from untrusted sources without risking your system. The freeze file ensures that you are running the exact generator you expect, even if the remote URL changes.

The generated files are written to `artifacts/<generator-name>/`.

---

## Signature Files

pGenie maintains two kinds of signature files:

- **Query signature files** beside query files in `queries/`
- **Custom-type signature files** under `types/<schema>/`

Together they are an important part of pGenie's design:

- They provide a **stable, human-readable** record of each query's type signature that can be reviewed in pull requests.
- They make **schema drift impossible**: on every run, pGenie re-resolves query signatures and referenced custom types from the live database and compares them against the committed signature files. If a migration changes a query-facing type, pGenie detects the mismatch and fails the build, forcing you to either update the signature files or fix the migration.

**Lifecycle of a signature file:**

1. **Created by pGenie** the first time `pgn generate` (or `pgn analyse`) runs and a needed signature file does not exist.
2. **Read by pGenie** on every subsequent run — pGenie compares the freshly-resolved definition against the committed file and fails the build if they differ.
3. **Updated manually by you** when you want to tighten constraints (for example, query parameter nullability or composite field nullability) or when a schema change requires acknowledging a type change.
4. **Regenerated by pGenie** only if you delete the file and re-run generation.

pGenie never silently overwrites an existing signature file.

---

## The Freeze File

`freeze1.pgn.yaml` pins the content hash of every generator URL referenced in `project1.pgn.yaml`. It is analogous to `package-lock.json`, `Cargo.lock`, or `cabal.project.freeze`.

- When the freeze file exists, pGenie will verify that each downloaded generator matches its recorded hash, ensuring reproducible generation across machines and over time.
- When you want to upgrade a generator, delete the relevant entry from the freeze file (or delete the whole file) and run `pgn generate` - the new generator will be fetched and a new hash recorded.

See the [Freeze File](reference/freeze-file.md) reference for the full format and lifecycle.

---

## Index Analysis

The `pgn manage-indexes` command keeps your index set lean and correct as the application evolves. It connects to the same temporary analysis database used during generation, inspects all existing non-primary indexes from the catalog, and runs `EXPLAIN` on every query to detect sequential scans. It then produces a SQL migration that:

- **Drops** indexes that are no longer used by any observed query (unused), are exact duplicates of another index (redundant), or have composite trailing columns that no query needs (excessive).
- **Creates** new indexes for columns that appear in `WHERE` clauses but have no covering index.

This two-sided analysis means you never accumulate stale indexes that slow down writes without benefiting any read query.

---

## Caching

pGenie caches several things between runs to keep generation fast:

| What | Where | Invalidated when |
|---|---|---|
| Docker image (Docker mode only) | Docker's local image store | You purge Docker images |
| Dhall generator bytecode | OS cache directory | Generator URL or hash changes |
