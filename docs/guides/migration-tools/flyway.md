# Integrating pGenie with Flyway

[Flyway](https://flywaydb.org/) manages database schema changes using versioned SQL migration files named with a `V<version>__<description>.sql` convention. pGenie can reuse the same files without any conflicts.

---

## How Flyway names migration files

Flyway expects versioned migrations in the form:

```
V1__Initial_schema.sql
V2__Add_format_column.sql
V10__Add_tracks_table.sql
```

Flyway sorts these by version number, not by filename alphabetical order.

---

## Sharing migration files with pGenie

pGenie applies files in **natural sort order** by filename. Flyway's `V<N>__` prefix is compatible with natural sort order as long as version numbers are the leading component (e.g. `V1__...` before `V2__...` before `V10__...`).

The easiest setup is to point pGenie's `migrations/` directory at the same directory Flyway uses:

```
my-project/
├── project1.pgn.yaml
├── migrations/                  ← pGenie reads from here
│   ├── V1__Initial_schema.sql
│   ├── V2__Add_format.sql
│   └── V3__Add_tracks.sql
└── queries/
    └── ...
```

If Flyway is configured with `flyway.locations=filesystem:migrations` (or the equivalent), both tools will read the same files from the same directory.

!!! note "Repeatable and undo migrations"
    pGenie ignores Flyway's repeatable migrations (`R__<description>.sql`) and undo migrations (`U<version>__<description>.sql`) — only `.sql` and `.psql` files that sort before a given point are applied. If you use repeatable migrations, add them to your `migrations/` directory but be aware that pGenie will apply them in filename sort order, which may differ from Flyway's execution order. Review the resulting schema carefully.

---

## Flyway migrations in a different directory

If your Flyway migrations live elsewhere (for example, `src/main/resources/db/migration/` in a Java project), you have two options:

**Option A — Configure pGenie to use the Flyway directory directly:**

Move your `project1.pgn.yaml` so that `migrations/` resolves to the Flyway directory, or create a symlink:

```bash
ln -s src/main/resources/db/migration migrations
```

**Option B — Maintain a `migrations/` directory with symlinks to each file:**

```bash
mkdir -p migrations
ln -s ../src/main/resources/db/migration/V1__Initial_schema.sql migrations/
ln -s ../src/main/resources/db/migration/V2__Add_format.sql migrations/
```

---

## Checklist

- [ ] Flyway migration files are plain `.sql` files.
- [ ] pGenie's `migrations/` directory contains (or links to) the same files.
- [ ] Files sort in the correct schema-application order under natural sort.
- [ ] `queries/` and `project1.pgn.yaml` are in the same directory as `migrations/`.
- [ ] pGenie is run for analysis only (`pgn analyse`) or code generation (`pgn generate`); it never applies migrations to your production database.
