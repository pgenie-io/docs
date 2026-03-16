# Integrating pGenie with Sqitch

[Sqitch](https://sqitch.org/) is a database change management tool that uses a **plan file** listing named changes, each with corresponding `deploy/`, `revert/`, and `verify/` SQL scripts.

---

## How Sqitch works

A Sqitch project has the following structure:

```
sqitch.conf
sqitch.plan
deploy/
  initial_schema.sql
  add_format.sql
  add_tracks.sql
revert/
  initial_schema.sql
  add_format.sql
  add_tracks.sql
verify/
  initial_schema.sql
  add_format.sql
  add_tracks.sql
```

The `sqitch.plan` file lists changes in the order they should be applied:

```
%syntax-version=1.0.0
%project=music_catalogue

initial_schema 2024-01-01T00:00:00Z Dev <dev@example.com> # Initial schema
add_format 2024-01-15T00:00:00Z Dev <dev@example.com> # Add album format
add_tracks 2024-02-01T00:00:00Z Dev <dev@example.com> # Add tracks
```

When you run `sqitch deploy`, it applies the `deploy/<name>.sql` scripts in plan order and tracks them in the database.

---

## Sharing deploy scripts with pGenie

pGenie needs SQL files in a single `migrations/` directory, sorted in the correct application order. The `deploy/` directory in a Sqitch project contains exactly these files, but without an explicit ordering prefix — Sqitch uses the plan file to determine order.

**Recommended approach: prefix your deploy scripts with a sequence number.**

Name deploy scripts with a numeric prefix that matches their order in `sqitch.plan`:

```
deploy/
  001_initial_schema.sql
  002_add_format.sql
  003_add_tracks.sql
```

Then symlink or copy the `deploy/` directory to `migrations/`:

```bash
ln -s deploy migrations
```

Or configure `project1.pgn.yaml` to sit alongside `deploy/` and name the migrations directory `deploy`:

```
my-project/
├── project1.pgn.yaml        ← project root
├── sqitch.conf
├── sqitch.plan
├── deploy/                  ← also used as pGenie migrations/
│   ├── 001_initial_schema.sql
│   ├── 002_add_format.sql
│   └── 003_add_tracks.sql
├── revert/
├── verify/
└── queries/
```

Since pGenie looks for a directory named `migrations/` by default, create a symlink:

```bash
ln -s deploy migrations
```

!!! tip
    Numeric prefixes (e.g. `001_`, `002_`) are natural-sort friendly and ensure pGenie applies scripts in the same order Sqitch does, as long as the plan order matches the numeric order.

---

## Without numeric prefixes

If your deploy scripts are not numerically prefixed, you can maintain a separate `migrations/` directory and symlink each file with an explicit prefix:

```bash
mkdir -p migrations
ln -s ../deploy/initial_schema.sql migrations/001_initial_schema.sql
ln -s ../deploy/add_format.sql     migrations/002_add_format.sql
ln -s ../deploy/add_tracks.sql     migrations/003_add_tracks.sql
```

This decouples pGenie's ordering from Sqitch's plan without duplicating file content.

---

## Sqitch `deploy` scripts and idempotency

Sqitch deploy scripts are plain SQL. pGenie applies them as-is against a fresh database container, so any DDL that is valid PostgreSQL will work. You do not need to use any Sqitch-specific syntax; just keep your deploy scripts as plain SQL.

---

## Checklist

- [ ] Sqitch deploy scripts are plain SQL (no Sqitch-specific syntax required by pGenie).
- [ ] Deploy scripts are available to pGenie as numbered files in `migrations/`, in the same order as `sqitch.plan`.
- [ ] Files sort in the correct schema-application order under natural sort.
- [ ] pGenie is run for analysis only (`pgn analyse`) or code generation (`pgn generate`); it never interacts with Sqitch's change-tracking tables.
