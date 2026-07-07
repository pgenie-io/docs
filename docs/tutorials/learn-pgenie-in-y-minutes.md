# Learn pGenie in Y Minutes

This is a complete walkthrough of pGenie's core loop, inspired by the [Learn X in Y minutes](https://learnxinyminutes.com/) series. You'll define a schema in plain SQL, write parameterized queries, and generate type-safe client libraries for two languages with one command. Then you'll break the schema on purpose — and watch pGenie fail the build before production can.

We'll build a simple **music catalogue** — the same project used in the [pGenie demo](https://github.com/pgenie-io/demo).

---

## Prerequisites

- [pGenie installed](../guides/installation/index.md) (`pgn --help` works)
- Either [Docker installed](https://docs.docker.com/engine/install/) and running (`docker info` succeeds), or a live PostgreSQL server that you can reach with `--database-url`

!!! note
    The examples below use the default Docker execution mode. In live instance mode, run the same commands with `--database-url "..."`, and make sure the `postgres` field in `project1.pgn.yaml` matches the live server's major version. On Windows, use live instance mode because Docker execution mode is not supported there yet.

---

## Step 1 - Set Up the Project

```bash
mkdir music-catalogue
cd music-catalogue
```

Create `project1.pgn.yaml`:

```yaml
# Top-level namespace. Use your username or organization name.
space: my_space

# Project name. Used for library naming in generated artifacts.
name: music_catalogue

# Version for generated artifacts. SemVer format.
version: 1.0.0

# Major PostgreSQL version used for analysis. Defaults to 18.
postgres: 18

# Code generators to run.
# Each key is an output directory name under artifacts/.
# Each value is a URL pointing to a Dhall generator entry point.
artifacts:
  haskell: https://github.com/pgenie-io/haskell.gen/releases/download/v1.0.0/resolved.dhall
  java: https://github.com/pgenie-io/java.gen/releases/download/v1.0.0/resolved.dhall
```

Note the two entries under `artifacts`. One project, two target languages — every query you write below becomes a typed function in both libraries. Generators are plain [Dhall](https://dhall-lang.org/) programs referenced by URL; the [Codegens reference](../reference/codegens.md) lists what's available, and you can [write your own](../guides/implementing-custom-generators.md).

If you use live instance mode, set `postgres` to the major version of the server you connect to.

---

## Step 2 - Write Migrations

Migrations are plain PostgreSQL DDL, applied in natural sort order — `1.sql` before `2.sql`, and `10.sql` after `9.sql`. They are append-only: to change the schema, add a file; don't edit old ones.

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

Any valid PostgreSQL DDL works: tables, types, indexes, constraints.

---

## Step 3 - Write Queries

One file per query in `queries/`. The filename becomes the name in generated code; parameters use `$snake_case` syntax. That is the entire authoring surface — no annotations, no model classes, no DSL. Types are inferred from the schema.

```bash
mkdir queries
```

**`queries/insert_album.sql`** - Insert a new album and return its generated ID:

```sql
insert into album (name, released, format, recording)
values ($name, $released, $format, $recording)
returning id
```

**`queries/select_album_by_name.sql`** - Find albums by name:

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

Any statement type is supported: `SELECT`, `INSERT … RETURNING`, `UPDATE`, `DELETE`, and so on.

---

## Step 4 - Generate

```bash
pgn generate
```

!!! note "First run"
    The first run pulls a PostgreSQL image (in Docker execution mode) and caches the Dhall generators, so it takes a while. Subsequent runs finish in seconds.

In one command, pGenie:

1. Started a temporary PostgreSQL server.
2. Applied the migrations in order.
3. Ran every query against the live schema and recorded its resolved types in **signature files**.
4. Generated the `haskell` and `java` libraries under `artifacts/`.
5. Wrote `freeze1.pgn.yaml`, pinning each generator to a content hash.

No guessing, no SQL parsing heroics — the types come from PostgreSQL itself.

Your project now looks like this:

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
│   ├── insert_album.sig1.pgn.yaml            ← new: query signature
│   ├── select_album_by_name.sql
│   ├── select_album_by_name.sig1.pgn.yaml    ← new
│   ├── select_album_by_format.sql
│   ├── select_album_by_format.sig1.pgn.yaml  ← new
│   ├── update_album_released.sql
│   └── update_album_released.sig1.pgn.yaml   ← new
├── types/
│   └── public/                               ← new: custom type signatures
│       ├── album_format.sig1.pgn.yaml
│       └── recording_info.sig1.pgn.yaml
└── artifacts/
    ├── haskell/                              ← new: generated Haskell library
    └── java/                                 ← new: generated Java library
```

The `types/` directory records signatures for your custom enum and composite types — same idea as query signatures, covered in the [Type Signature File](../reference/type-signature-file.md) reference.

You'll also notice sequential-scan warnings in the output. Hold that thought — Step 9 deals with them.

### The query signature

Open `queries/select_album_by_name.sig1.pgn.yaml`:

```yaml
idempotent: false
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

This is the query's type contract, resolved against the real schema:

- `id` and `name` are `not_null: true` — they carry `NOT NULL` constraints in the schema.
- `format` is your custom enum; `recording` is your custom composite type.
- `$name` is nullable, because nothing in the SQL proves the caller will never pass `NULL`.

Commit signature files to version control — they make type changes visible in pull request review. The [Query Signature File](../reference/query-signature-file.md) reference covers every field, including `idempotent`, which lets generators emit automatic retry logic for queries that are safe to repeat.

### The freeze file

Open `freeze1.pgn.yaml`:

```yaml
# Map of generator hashes by url
https://github.com/pgenie-io/haskell.gen/releases/download/v1.0.0/resolved.dhall: sha256:d25623bc236c7225c35bb39be0e2490b895bfaed9605c2916d6286a073e32a20
https://github.com/pgenie-io/java.gen/releases/download/v1.0.0/resolved.dhall: sha256:72722fab4cfe21476f7011cf2cc8149a15fbe78d8a3200b0efdf8cac08127008
```

Commit this too. Anyone who runs `pgn generate` on this project gets identical output. See the [Freeze File](../reference/freeze-file.md) reference for details.

---

## Step 5 - Own a Signature

pGenie writes each signature file once. After that, the file is yours: on every run pGenie re-resolves the signature from the database and validates it against your committed file. It never silently overwrites it.

That means you can tighten the contract. `$name` was inferred as nullable, but searching for a `NULL` album name is meaningless. Edit `queries/select_album_by_name.sig1.pgn.yaml`:

```yaml
parameters:
  name:
    type: text
    not_null: true   # ← changed
```

(The rest of the file stays as is.)

Run `pgn generate` again. Both generated libraries now take a non-nullable `name` parameter — and the tightened contract lives in version control, visible to every reviewer and future maintainer.

---

## Step 6 - Add a Non-Breaking Migration

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

Run `pgn generate`. Fresh database, all four migrations, every query re-analyzed — and every freshly resolved signature compared against your committed sig files. If they match, generation proceeds; if they differ, the build fails.

The build succeeds. Both new columns are nullable, so no existing query breaks — not even `insert_album`, which doesn't mention them; PostgreSQL fills them with `NULL`. A nullable column can always be added without breaking existing queries. (A `SELECT *` query would be the exception — its result columns would change.)

---

## Step 7 - Watch a Breaking Migration Get Caught

Now make `disc` mandatory:

**`migrations/5.sql`**:

```sql
alter table album
  alter column disc set not null;
```

Run `pgn generate` again. This time the build **fails**:

```
Error: null value in column "disc" of relation "album" violates not-null constraint
Suggestion: Add "disc" to the INSERT column list, or define a DEFAULT value for the column in the schema
Details:
  code: 23502
  sql:
    insert into album (name, released, format, recording)
    values ($1, $2, $3, $4)
    returning id
```

`insert_album` never mentions `disc`. The migration broke it anyway — and pGenie caught it, because it ran the query against the actual migrated schema. This is schema drift protection: an incompatibility between a migration and any query, however indirect, fails the build instead of failing in production.

The failure also points at the safe rollout: ship the nullable columns first (migration 4), update the queries and release the regenerated libraries, and only then make the column mandatory. Two phases, zero downtime.

We're not ready for phase two yet, so drop the migration:

```bash
rm migrations/5.sql
```

---

## Step 8 - Validate in CI

```bash
pgn analyse
```

Same pipeline — ephemeral PostgreSQL, all migrations, every query validated, every signature checked — but no artifacts. This is the lightweight CI check: if `pgn analyse` passes on a pull request, the schema, queries, and signature files are consistent.

---

## Step 9 - Manage Indexes

Remember those warnings from `pgn generate`? `pgn analyse` prints them too:

```
Warning: Sequential scan detected
Suggestion: Run 'manage-indexes' to generate index migration
Details:
  query: select_album_by_name
  table: album
  columns: name
```

Some queries scan whole tables. Ask pGenie what to do about it:

```bash
pgn manage-indexes
```

```sql
-- Auto-generated migration to optimize indexes

-- Drop redundant/excessive indexes
-- album_recording_idx on (recording) is not used by observed query needs
DROP INDEX "public"."album_recording_idx";

-- Create missing indexes
CREATE INDEX ON album (format);

CREATE INDEX ON album (name);
```

It cuts both ways. `select_album_by_name` and `select_album_by_format` filter on unindexed columns, so pGenie proposes indexes for them. Meanwhile `album_recording_idx` — added in migration 3 "just in case" — serves no query at all, so pGenie proposes dropping it. As your queries evolve, the index set follows.

To write this migration to disk (pGenie picks the next free number — `5.sql` here):

```bash
pgn manage-indexes --add-migration
```

!!! warning "Review before committing"
    The suggestions are heuristic, based only on the queries pGenie can see. Review them against your actual data and workload before applying.

---

## What You've Learned

You've now touched every core capability:

- **Plain SQL in, typed libraries out.** Migrations and queries are standard PostgreSQL files — no annotations, no model classes, no DSL. One `pgn generate` produced idiomatic Haskell and Java libraries; adding a language is one line in `project1.pgn.yaml`.
- **Types come from a real PostgreSQL.** Every query is executed against the actual migrated schema at generation time — inference by database, not by parser.
- **Signatures are contracts you own.** pGenie writes each `.sig1.pgn.yaml` once, then validates against it forever. Tighten them by hand; review type changes in pull requests.
- **Schema drift fails the build.** A migration that breaks any query — even one that never mentions the changed column — is caught before deployment and steers you toward a two-phase rollout.
- **Builds are reproducible.** `freeze1.pgn.yaml` pins every generator to a content hash; commit it alongside the sig files.
- **Indexes stay in sync with queries.** `pgn manage-indexes` proposes missing indexes and drops unused ones as the application evolves.
- **`pgn analyse` puts all of this in CI** without generating a byte of code.

---

## Next Steps

- Read the [Reference](../reference/project-structure.md) for detailed documentation on every file format.
- Browse the [demo project](https://github.com/pgenie-io/demo) for a complete working example with generated output.
- Check out the [Codegens reference](../reference/codegens.md) for available generators.
- Write your own generator by following the [Implementing Custom Generators](../guides/implementing-custom-generators.md) guide.
