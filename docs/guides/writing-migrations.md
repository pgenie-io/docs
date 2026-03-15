# Writing Migrations

Migrations define your PostgreSQL schema. pGenie applies them in order to a temporary database before analyzing your queries.

---

## Directory

All migration files live in the `migrations/` directory at the root of your project.

```
my-project/
├── project1.pgn.yaml
├── migrations/
│   ├── 1.sql
│   ├── 2.sql
│   └── 3.sql
└── queries/
```

---

## File Format

Migration files are plain SQL files. They can contain any valid PostgreSQL DDL or DML statements.

```sql
-- migrations/1.sql

create table "artist" (
  "id"   int4 not null generated always as identity primary key,
  "name" text not null
);

create table "album" (
  "id"       int4 not null generated always as identity primary key,
  "name"     text not null,
  "released" date null
);
```

Accepted file extensions are `.sql` and `.psql`. Files with any other extension are ignored.

---

## Execution Order

Migration files are applied to the database in **natural sort order** of their filenames. Natural sorting handles embedded numbers intuitively: `migration-10.sql` is applied *after* `migration-9.sql`, not before it. It is your responsibility to name files so that this order matches the intended execution sequence.

Common naming strategies:

| Strategy | Example filenames |
|---|---|
| Simple integers | `1.sql`, `2.sql`, `10.sql` |
| Zero-padded integers | `001.sql`, `002.sql`, `010.sql` |
| Timestamps | `20240101_initial.sql`, `20240215_add_format.sql` |

!!! note
    Because pGenie uses natural sorting, `10.sql` is correctly applied *after* `9.sql`. Zero-padding is still a good practice for readability and compatibility with tools that do not implement natural sorting.

---

## Supported DDL

You can use any PostgreSQL DDL in your migrations. Common patterns:

### Tables

```sql
create table "genre" (
  "id"   int4 not null generated always as identity primary key,
  "name" text not null unique
);
```

### Enumerations

```sql
create type "album_format" as enum (
  'Vinyl',
  'CD',
  'Cassette',
  'Digital'
);
```

### Composite Types

```sql
create type "recording_info" as (
  "studio_name"    text,
  "city"           text,
  "country"        text,
  "recorded_date"  date
);
```

### Altering Tables

```sql
alter table "album"
add column "format"    album_format   null,
add column "recording" recording_info null;
```

### Indexes

```sql
create index "artist_name_idx" on "artist" ("name");
```

---

## Tips

- **Keep migrations additive**: avoid modifying or dropping columns that existing queries reference. Prefer new migrations that `ALTER` or `ADD` rather than re-creating tables.
- **Comment your migrations**: SQL comments (`--`) are preserved in the file and help reviewers understand the intent of a change.
- **Commit migrations**: migration files should always be committed to version control. They are the authoritative record of your schema history.
