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

## Step 7 - Add a Migration

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
- Re-analyze all queries.
- Update signature files where the schema change affects a query's result.
- Re-run the generator with the updated schema.

---

## Step 8 - Validate Only (no generators)

To check your schema and queries without running any generators, set `artifacts` to an empty map:

```yaml
artifacts: {}
```

Then run `pgn generate`. This is useful as a lightweight CI check.

---

## Step 9 - Manage Indexes

Run the index manager to detect sequential scans:

```bash
pgn manage-indexes
```

If any queries produce sequential scans, pGenie will suggest index definitions you can add as a new migration.

---

## What You've Learned

- A pGenie project has `migrations/`, `queries/`, and `project1.pgn.yaml`.
- Migrations are plain SQL applied in sort order.
- Queries use `$snake_case` parameter syntax; types are inferred from the schema.
- `pgn generate` analyzes queries against a real PostgreSQL instance and generates typed client code.
- Signature files (`.sig1.pgn.yaml`) and the freeze file (`freeze1.pgn.yaml`) should be committed.
- Adding a migration and re-running `pgn generate` updates all signatures and artifacts automatically.
- `pgn manage-indexes` suggests indexes based on query patterns.

---

## Next Steps

- Read the [Reference](../reference/project-structure.md) for detailed documentation on every file format.
- Browse the [demo project](https://github.com/pgenie-io/demo) for a complete working example with generated output.
- Check out the [hasql generator](../reference/codegens/hasql.md) reference.
- Write your own generator by following the [Implementing Custom Generators](../guides/implementing-custom-generators.md) guide.
