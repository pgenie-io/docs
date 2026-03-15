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

- Files are applied in **lexicographic sort order**, so `1.sql` before `2.sql` before `3.sql`.
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
4. It wrote **signature files** recording the resolved types for each query.
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

Open `queries/update_album_released.sig1.pgn.yaml`. It will look something like:

```yaml
parameters:
  id:
    type: int8
    not_null: false
  released:
    type: date
    not_null: false
result:
  cardinality: zero_or_one
  columns: {}
```

Notice that `$id` is inferred as nullable (`not_null: false`). pGenie cannot statically prove from the SQL alone that the caller will never pass `NULL` for `id`, so it defaults to nullable. However, we know that an `UPDATE … WHERE id = $id` with a `NULL` id is meaningless - we always intend to pass a concrete album ID.

Edit the file and change `id.not_null` to `true`:

```yaml
parameters:
  id:
    type: int8
    not_null: true   # ← changed
  released:
    type: date
    not_null: false
result:
  cardinality: zero_or_one
  columns: {}
```

Run `pgn generate` again. The generator will now produce a **non-nullable** parameter type for `$id` in the generated code.

**Why this matters:** The signature file is the source of truth for the query's type contract - not the SQL alone, and not the database schema alone. By committing this change, you are documenting an explicit contract that callers must supply a non-null `id`. Code generators, reviewers, and future maintainers all see this intent clearly.

---

## Step 8 - Add a Migration

Suppose you want to track individual album tracks:

**`migrations/4.sql`**:

```sql
create type track_info as (
  title            text,
  duration_seconds int4,
  tags             text[]
);

alter table album
  add column tracks track_info[] null;
```

Run `pgn generate` again. pGenie will:

- Re-apply all migrations (including the new one) to a fresh container.
- Re-analyze all queries against the updated schema.
- **Check that each query's actual signature still matches its signature file.** If a migration changes the type of a column referenced by a query, pGenie will detect that the existing signature file no longer matches and will **fail the build**, forcing you to either update the signature file to reflect the new reality or fix the migration.
- Re-run the generator with the updated schema.

**Why the build fails instead of silently updating:** Signature files are the declared source of truth for each query's type contract. An automatic silent update would mean a schema change could alter the generated API without any explicit acknowledgment. By requiring you to update the signature file manually, pGenie makes every type-level change visible and intentional in your version history. This design makes schema drift impossible — any database change that affects a query's parameter or result types will cause a build failure until the signature file is updated to reflect the new reality.

!!! note
    In this particular example, adding the `tracks` column does not affect the result of `select_album_by_name` unless that query's SQL selects `tracks` explicitly. If you add a `SELECT *` style query, its signature will need updating whenever the schema changes.

---

## Step 9 - Validate Only (CI Check)

To check your schema and queries without running any generators and without producing any generated code, use the `analyse` command:

```bash
pgn analyse
```

`pgn analyse` is a lightweight CI check. It spins up the same ephemeral PostgreSQL container, applies all migrations, and validates every query against the live schema - but it stops there and produces no artifacts. This makes it ideal for pull request CI pipelines where you only need to confirm that the schema and queries are consistent.

!!! tip
    If `pgn analyse` passes, your schema and queries are self-consistent. If it fails, you have a mismatch between a migration, a query, and/or a signature file that must be resolved before the build can proceed.

---

## Step 10 - Manage Indexes

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

To write this migration directly to `migrations/5.sql`, run:

```bash
pgn manage-indexes --add-migration
```

pGenie determines the next available migration number automatically and writes the file. You can then commit it as part of your normal workflow.

!!! warning "Review before committing"
    Index management is a complex topic and pGenie's suggestions are heuristic — they are based solely on the query patterns in your `queries/` directory. Always review the generated migration before applying it. You may need to manually adjust or omit suggestions depending on your actual data distribution, write throughput, and access patterns that pGenie cannot observe (for example, queries issued by external tools or administrative scripts).

---

## What You've Learned

- A pGenie project has `migrations/`, `queries/`, and `project1.pgn.yaml`.
- Migrations are plain SQL applied in sort order.
- Queries use `$snake_case` parameter syntax; types are inferred from the schema.
- `pgn generate` analyzes queries against a real PostgreSQL instance and generates typed client code.
- Signature files (`.sig1.pgn.yaml`) are the source of truth for each query's type contract. You can edit them by hand (e.g. to tighten nullability) and pGenie will use your edits in subsequent code generation runs.
- If a migration changes a column type that a query references, pGenie will fail the build until the signature file is updated, making schema drift impossible.
- The freeze file (`freeze1.pgn.yaml`) pins generator hashes for reproducible builds. Both should be committed to version control.
- `pgn analyse` validates schema and queries without running generators — useful as a lightweight CI check.
- `pgn manage-indexes` suggests both new indexes for sequential scans and DROP statements for indexes that are no longer used by any query, keeping the database schema clean as the application evolves.

---

## Next Steps

- Read the [Reference](../reference/project-structure.md) for detailed documentation on every file format.
- Browse the [demo project](https://github.com/pgenie-io/demo) for a complete working example with generated output.
- Check out the [hasql generator](../reference/codegens/hasql.md) reference.
- Write your own generator by following the [Implementing Custom Generators](../guides/implementing-custom-generators.md) guide.
