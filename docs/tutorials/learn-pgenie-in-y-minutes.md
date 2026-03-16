# Learn pGenie in Y Minutes

This is a complete walkthrough of pGenie's core features, inspired by the [Learn X in Y minutes](https://learnxinyminutes.com/) series. By the end you'll have set up a project, written migrations and queries, configured a generator, and generated a type-safe client library.

We'll build a simple **music catalogue** project - the same one used in the [pGenie demo](https://github.com/pgenie-io/demo).

---

## Prerequisites

- pGenie installed (`pgn --help` works)
- Docker installed and running (`docker info` succeeds)

---

## Step 1 - Create a Project Directory

```bash
mkdir music-catalogue
cd music-catalogue
```

---

## Step 2 - Write the Project File

Create `project1.pgn.yaml`:

```yaml
# Top-level namespace. Use your username or organization name.
space: my_space

# Project name. Used for library naming in generated artifacts.
name: music_catalogue

# Version for generated artifacts. SemVer format.
version: 1.0.0

# Code generators to run.
# Each key is an output directory name under artifacts/.
# Each value is a URL pointing to a Dhall generator entry point.
artifacts:
  hasql: https://raw.githubusercontent.com/pgenie-io/haskell-hasql.gen/v0.1.0/gen/Gen.dhall
```

---

## Step 3 - Write Migrations

Migrations define your PostgreSQL schema. Create the `migrations/` directory and add your first migration:

```bash
mkdir migrations
```

**`migrations/1.sql`** - Initial schema:

```sql
create table "genre" (
  "id"   int4 not null generated always as identity primary key,
  "name" text not null unique
);

create table "artist" (
  "id"   int4 not null generated always as identity primary key,
  "name" text not null
);

create table "album" (
  "id"       int4 not null generated always as identity primary key,
  "name"     text not null,
  "released" date null
);

create table "album_genre" (
  "album" int4 not null references "album",
  "genre" int4 not null references "genre"
);

create table "album_artist" (
  "album"   int4 not null references "album",
  "artist"  int4 not null references "artist",
  "primary" bool not null,
  primary key ("album", "artist")
);
```

**`migrations/2.sql`** - Evolve the schema: change album `id` to `int8`:

```sql
alter table album alter column id type int8;
alter table album_genre alter column album type int8;
alter table album_artist alter column album type int8;
```

**`migrations/3.sql`** - Add custom types and columns:

```sql
-- Custom enum type
create type album_format as enum (
  'Vinyl', 'CD', 'Cassette', 'Digital', 'DVD-Audio', 'SACD'
);

-- Custom composite type
create type recording_info as (
  studio_name  text,
  city         text,
  country      text,
  recorded_date date
);

alter table album
  add column format    album_format   null,
  add column recording recording_info null;

-- Index added in anticipation of filtering by recording studio;
-- we will revisit this later.
create index album_recording_idx on album (recording);
```

Key points:

- Files are applied in **natural sort order**, so `1.sql` before `2.sql` before `3.sql` (and `10.sql` after `9.sql`, not before it).
- You can use any valid PostgreSQL DDL: tables, types, indexes, constraints, etc.
- Migrations are **append-only**: add new files rather than editing existing ones.

---

## Step 4 - Write Queries

Queries are parameterized SQL statements. Each query lives in its own file inside `queries/`. The filename (without `.sql`) determines the name in generated code.

```bash
mkdir queries
```

**`queries/insert_album.sql`** - Insert a new album and return its generated ID:

```sql
insert into album (name, released, format, recording)
values ($name, $released, $format, $recording)
returning id
```

**`queries/select_album_by_name.sql`** - Find albums by name (nullable parameter):

```sql
select id, name, released, format, recording
from album
where name = $name
```

**`queries/select_album_by_format.sql`** - Filter by enum column:

```sql
select id, name, released, format, recording
from album
where format = $format
```

**`queries/update_album_released.sql`** - Update a column, no result:

```sql
update album
set released = $released
where id = $id
```

Key points:

- **Parameters** use `$snake_case` syntax - types are inferred from the schema.
- **Filenames** use `snake_case` - these become function/method/class/data-type names in the generated code.
- Any query type is supported: `SELECT`, `INSERT … RETURNING`, `UPDATE`, `DELETE`, etc.

---

## Step 5 - Generate Code

```bash
pgn generate
```

!!! note "First run"
    The first time you run `pgn generate`, it pulls a PostgreSQL Docker image and caches the Dhall generators. This takes upto **3 minutes**. Subsequent runs complete in a few seconds.

What happened:

1. pGenie started a temporary PostgreSQL container.
2. It applied `migrations/1.sql`, `2.sql`, and `3.sql` in order, building up the schema.
3. It analyzed each query in `queries/` against the live schema.
4. It wrote **signature files** recording the resolved types for each query (since none existed yet).
5. It ran the `hasql` generator and wrote the output to `artifacts/hasql/`.
6. It wrote `freeze1.pgn.yaml` recording the generator's content hash for reproducibility.

---

## Step 6 - Inspect the Results

Your project directory now looks like:

```
music-catalogue/
├── project1.pgn.yaml
├── freeze1.pgn.yaml                          ← new: lock file
├── migrations/
│   ├── 1.sql
│   ├── 2.sql
│   └── 3.sql
├── queries/
│   ├── insert_album.sql
│   ├── insert_album.sig1.pgn.yaml            ← new: type signature
│   ├── select_album_by_name.sql
│   ├── select_album_by_name.sig1.pgn.yaml    ← new: type signature
│   ├── select_album_by_format.sql
│   ├── select_album_by_format.sig1.pgn.yaml  ← new: type signature
│   ├── update_album_released.sql
│   └── update_album_released.sig1.pgn.yaml   ← new: type signature
└── artifacts/
    └── hasql/                                ← new: generated Haskell library
```

### The signature file

Open `queries/select_album_by_name.sig1.pgn.yaml`:

```yaml
parameters:
  name:
    type: text
    not_null: false
result:
  cardinality: many
  columns:
    id:
      type: int8
      not_null: true
    name:
      type: text
      not_null: true
    released:
      type: date
      not_null: false
    format:
      type: album_format
      not_null: false
    recording:
      type: recording_info
      not_null: false
```

This is the resolved type contract for the query. Notice:

- `$name` is nullable (`not_null: false`) because pGenie cannot statically prove the parameter is non-null from the query context alone - there is no `NOT NULL` constraint explicitly applied to the parameter in the SQL.
- `id` and `name` columns are `not_null: true` because they are defined with `NOT NULL` in the schema.
- `released`, `format`, and `recording` are nullable because they were defined as `null` columns.
- `format` has type `album_format` and `recording` has type `recording_info` - the custom types you defined.

Commit signature files to version control. They make type changes visible in pull request reviews.

### The freeze file

Open `freeze1.pgn.yaml`:

```yaml
https://raw.githubusercontent.com/pgenie-io/haskell-hasql.gen/v0.1.0/gen/Gen.dhall: sha256:fcc51fe6ae2f774bcb13684b680aae1a9b827451c3f56c1ae2875f1e64fe78e5
```

This pins the generator to a specific content hash. Commit this file too - it ensures anyone running `pgn generate` on this project will get identical output.

---

## Step 7 - Refine a Query Signature

Open `queries/select_album_by_name.sig1.pgn.yaml`. It will look like:

```yaml
parameters:
  name:
    type: text
    not_null: false
result:
  cardinality: many
  columns:
    id:
      type: int8
      not_null: true
    name:
      type: text
      not_null: true
    released:
      type: date
      not_null: false
    format:
      type: album_format
      not_null: false
    recording:
      type: recording_info
      not_null: false
```

Notice that `$name` is inferred as nullable (`not_null: false`). pGenie cannot statically prove from the SQL alone that the caller will never pass `NULL` for `name`. However, in practice we always search for a concrete album name — passing `NULL` would be meaningless.

Edit the file and change `name.not_null` to `true`:

```yaml
parameters:
  name:
    type: text
    not_null: true   # ← changed
result:
  cardinality: many
  columns:
    ...
```

Run `pgn generate` again. pGenie will **reuse your edited signature file** and generate a **non-nullable** parameter type for `$name` in the output library.

**Why this matters:** pGenie never silently overwrites a signature file. Once a sig file exists, pGenie always re-resolves the signature from the database and validates it against your committed file. By changing `not_null` to `true`, you are documenting an explicit contract that callers must supply a non-null `name`. Code generators, reviewers, and future maintainers all see this intent clearly in version control.

---

## Step 8 - Add a Non-Breaking Migration

Suppose you want to track individual album tracks and disc information:

**`migrations/4.sql`**:

```sql
create type track_info as (
  title            text,
  duration_seconds int4,
  tags             text[]
);

alter table album
  add column tracks track_info[] null,
  add column disc   text         null;
```

Run `pgn generate` again. pGenie will:

- Re-apply all migrations (including the new one) to a fresh container.
- Re-analyze all queries against the updated schema.
- **Compare each query's freshly-resolved signature against the existing sig file.** If they match, generation proceeds; if they differ, the build fails.
- Re-run the generator with the updated schema.

**In this case the build succeeds.** Both new columns are nullable, so adding them doesn't break any existing query — including `insert_album`, which inserts into `album` without mentioning `tracks` or `disc`. Because those columns are nullable, PostgreSQL accepts the insert with `NULL` in those positions. The existing signature files remain valid.

This is the key insight about non-breaking schema changes: **a nullable column can always be added without breaking existing queries**, regardless of whether those queries reference it.

!!! note
    If you had added a `SELECT *` style query, its signature would need updating whenever new columns are added to the schema, because the result columns would change.

---

## Step 9 - Detect a Breaking Migration

Now suppose you want to make the `disc` column mandatory:

**`migrations/5.sql`**:

```sql
alter table album
  alter column disc set not null;
```

Run `pgn generate` again. This time the build **fails** with an error like:

```
Error: null value in column "disc" of relation "album" violates not-null constraint
Stage: Analysing > Queries > insert_album > Inferring
```

**Why this error appears:** During analysis, pGenie probes the nullability of each query parameter by attempting to run the query with `NULL` supplied to each parameter in turn. After migration `5.sql`, the `disc` column is `NOT NULL` with no default. When pGenie tries to infer the type of `insert_album`, it attempts to insert a row into `album` and the database rejects it because `disc` is not provided and cannot be `NULL`.

This is pGenie's schema drift protection in action. `insert_album` doesn't mention `disc`, yet the new NOT NULL constraint breaks it at the database level. pGenie catches this before you can accidentally generate and ship a library that would fail at runtime.

**How to proceed safely:**

The safest deployment strategy for this kind of change is:

1. **Deploy migration `4.sql` now** — adding nullable `tracks` and `disc` columns is non-breaking. Existing app code continues to work without any changes.
2. **Update your queries** to populate `disc` (and optionally `tracks`) as needed, then run `pgn generate`. Update the affected signature files to reflect the new contracts.
3. **Release updated SDKs** to all consuming applications and ensure they are deployed.
4. **Only then deploy migration `5.sql`** — by this point every application has been updated to supply a value for `disc`, so the NOT NULL constraint is safe.

This two-phase approach is the standard pattern for zero-downtime schema migrations. pGenie's build failure is your safety net: it prevents you from generating and releasing SDKs that are silently incompatible with the new schema.

---

## Step 10 - Validate Only (CI Check)

To check your schema and queries without running any generators and without producing any generated code, use the `analyse` command:

```bash
pgn analyse
```

`pgn analyse` is a lightweight CI check. It spins up the same ephemeral PostgreSQL container, applies all migrations, and validates every query against the live schema - but it stops there and produces no artifacts. This makes it ideal for pull request CI pipelines where you only need to confirm that the schema and queries are consistent.

!!! tip
    If `pgn analyse` passes, your schema and queries are self-consistent. If it fails, you have a mismatch between a migration, a query, and/or a signature file that must be resolved before the build can proceed.

---

## Step 11 - Manage Indexes

You may have noticed that both `pgn analyse` and `pgn generate` print warning messages like the following:

```
Warning: Sequential scan detected in query 'update_album_released': table 'album' scanned without index on (id)
Suggestion: Run 'manage-indexes' to generate index migration
Details:
  query: update_album_released
  table: album
```

These warnings tell you that one or more queries are performing full-table sequential scans because the relevant columns have no index. pGenie is suggesting you run `manage-indexes` to address this.

Run the index manager now:

```bash
pgn manage-indexes
```

You will see output like:

```sql
-- Auto-generated migration to optimize indexes

-- Drop redundant/excessive indexes
-- album_recording_idx on (recording) is not used by observed query needs
DROP INDEX "public"."album_recording_idx";

-- Create missing indexes
CREATE INDEX ON album (format);

CREATE INDEX ON album (name);
```

There are two types of changes here:

- **Drop `album_recording_idx`** — This index was created in migration 3 with the idea that queries might filter by recording studio. In practice, none of the queries in `queries/` filter on the `recording` column, so the index is unused overhead. pGenie proposes removing it to keep the schema clean and avoid unnecessary write overhead.
- **Create indexes on `format` and `name`** — The queries `select_album_by_format` and `select_album_by_name` filter by these columns respectively, triggering the sequential-scan warnings. Adding these indexes will eliminate the sequential scans.

This is the two-sided nature of `pgn manage-indexes`: as the application evolves and query patterns change, it not only suggests new indexes to cover new access patterns but also identifies indexes that have become redundant or unused, helping you keep the database schema clean and performant over time.

To write this migration directly to `migrations/6.sql`, run:

```bash
pgn manage-indexes --add-migration
```

pGenie determines the next available migration number automatically and writes the file. You can then commit it as part of your normal workflow.

!!! warning "Review before committing"
    Index management is a complex topic and pGenie's suggestions are heuristic — they are based solely on the query patterns in your `queries/` directory. Always review the generated migration before applying it. You may need to manually adjust or omit suggestions depending on your actual data distribution, write throughput, and access patterns that pGenie cannot observe (for example, queries issued by external tools or administrative scripts).

---

## What You've Learned

- A pGenie project has `migrations/`, `queries/`, and `project1.pgn.yaml`.
- Migrations are plain SQL applied in natural sort order.
- Queries use `$snake_case` parameter syntax; types are inferred from the schema.
- `pgn generate` analyzes queries against a real PostgreSQL instance and generates typed client code.
- Signature files (`.sig1.pgn.yaml`) are **written once** by pGenie and then owned by you. On every subsequent run pGenie re-resolves the signature from the database and validates it against your committed file. Edit them by hand to tighten constraints (e.g. nullability). pGenie never silently overwrites them.
- If a migration changes a column type that a query references, pGenie will fail the build until you update the signature file, making schema drift impossible.
- Non-breaking migrations (adding nullable columns) do not invalidate existing signature files and do not break queries that don't mention those columns.
- Breaking migrations (e.g. adding a NOT NULL column without a default) will fail the build during analysis, giving you a chance to update queries, regenerate SDKs, and deploy safely.
- The freeze file (`freeze1.pgn.yaml`) pins generator hashes for reproducible builds. Both sig files and the freeze file should be committed to version control.
- `pgn analyse` validates schema and queries without running generators — useful as a lightweight CI check.
- `pgn manage-indexes` suggests both new indexes for sequential scans and DROP statements for indexes that are no longer used by any query, keeping the database schema clean as the application evolves.

---

## Next Steps

- Read the [Reference](../reference/project-structure.md) for detailed documentation on every file format.
- Browse the [demo project](https://github.com/pgenie-io/demo) for a complete working example with generated output.
- Check out the [Codegens reference](../reference/codegens/index.md) for available generators.
- Write your own generator by following the [Implementing Custom Generators](../guides/implementing-custom-generators.md) guide.
