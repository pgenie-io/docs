# How pGenie Works

This page explains pGenie's internal architecture so you can understand what happens when you run `pgn generate` and why the tool is designed the way it is.

---

## The Pipeline

Running `pgn generate` triggers the following stages:

```
Migrations (SQL)  ──┐
                    ├──▶  PostgreSQL container  ──▶  Schema + query analysis  ──▶  Dhall codegen  ──▶  Artifacts
Queries (SQL)     ──┘
```

### 1. Container startup

pGenie uses [Testcontainers](https://testcontainers.com/) to spin up a disposable PostgreSQL container on the fly. This is why Docker must be running before you invoke `pgn generate`. The container is started fresh every time and torn down when generation is complete.

### 2. Schema application

All `.sql` files in your `migrations/` directory are applied to the fresh database **in sorted filename order**. This means your migrations must be named so that lexicographic sorting produces the correct execution order (e.g. `1.sql`, `2.sql`, …, or `001.sql`, `002.sql`, …).

Once applied, the container holds the exact schema your queries will run against.

### 3. Query analysis

For each `.sql` file in `queries/`, pGenie:

1. Prepares the statement against the live PostgreSQL instance using the extended query protocol. PostgreSQL's `DescribeStatement` message returns the OIDs of all parameter types and result columns.
2. Resolves each OID to a full type description—including composite type fields, enumeration labels, and array element types—by querying the system catalog (`pg_type`, `pg_attribute`, etc.).
3. Determines parameter nullability by consulting the schema and any explicit `NOT NULL` constraints visible in the query plan.
4. Writes a **signature file** (`.sig1.pgn.yaml`) alongside the `.sql` file, recording the resolved parameter and result types. This file is committed alongside your SQL and acts as a reproducible snapshot of the query's type signature.

### 4. Code generation

pGenie loads the code generators configured in your `project1.pgn.yaml`. Each generator is a [Dhall](https://dhall-lang.org/) program referenced by URL (e.g. a raw GitHub URL). The generator receives a structured description of your entire project—schema, queries, type information—and produces a tree of output files.

Dhall is used for code generators because it is:

- **Hermetic**: Dhall expressions are pure and total—no side effects, no I/O, no hidden state.
- **Composable**: Generators can import shared utilities and templates.
- **Cacheable**: Dhall expressions are content-addressed. A generator at a pinned URL is evaluated once, its output cached in `freeze1.pgn.yaml`.

The generated files are written to `artifacts/<generator-name>/`.

---

## Signature Files

Signature files (`.sig1.pgn.yaml`) are an important part of pGenie's design:

- They provide a **stable, human-readable** record of each query's type signature that can be reviewed in pull requests.
- They allow code generation to be **reproduced without re-running analysis**—if the signature file is present and the query SQL has not changed, generation can proceed from the cached signature.
- They make schema drift visible: if a migration changes the type of a column referenced by a query, the signature file will be updated and the diff will be visible in version control.

---

## The Freeze File

`freeze1.pgn.yaml` pins the content hash of every generator URL referenced in `project1.pgn.yaml`. It is analogous to a `package-lock.json` or `cabal.project.freeze` file.

- When the freeze file exists, pGenie will verify that each downloaded generator matches its recorded hash, ensuring reproducible generation across machines and over time.
- When you want to upgrade a generator, delete the relevant entry from the freeze file (or delete the whole file) and run `pgn generate`—the new generator will be fetched and a new hash recorded.

---

## Index Analysis

The `pgn manage-indexes` command analyzes your queries for sequential scan patterns and suggests PostgreSQL indexes that could improve performance. It connects to the same ephemeral container used during generation and uses `EXPLAIN` output to detect full-table scans on large predicates.

---

## Caching

pGenie caches several things between runs to keep generation fast:

| What | Where | Invalidated when |
|---|---|---|
| Docker image | Docker's local image store | You purge Docker images |
| Dhall generator bytecode | OS cache directory | Generator URL or hash changes |
| PostgreSQL container | Restarted each run | N/A—always fresh |
