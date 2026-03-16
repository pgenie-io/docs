# Integrating pGenie with Liquibase

[Liquibase](https://www.liquibase.com/) manages database changes through a **changelog** file that lists individual changesets. Changesets can be written in XML, YAML, JSON, or plain SQL format.

---

## How Liquibase works

A Liquibase changelog (`changelog.xml`, `changelog.yaml`, or `db.changelog-master.xml`) references a sequence of changesets. Each changeset can contain inline DDL or reference an external SQL file via `sqlFile`:

```xml
<databaseChangeLog>
  <changeSet id="1" author="dev">
    <sqlFile path="sql/1_initial_schema.sql"/>
  </changeSet>
  <changeSet id="2" author="dev">
    <sqlFile path="sql/2_add_format.sql"/>
  </changeSet>
</databaseChangeLog>
```

Liquibase tracks applied changesets in a `DATABASECHANGELOG` table in your production database.

---

## Sharing SQL files with pGenie

If your Liquibase changesets reference external SQL files (via `sqlFile` or `includeAll`), you can point pGenie's `migrations/` directory at the same SQL files.

**Recommended project layout:**

```
my-project/
├── project1.pgn.yaml
├── migrations/              ← pGenie reads from here
│   ├── 1_initial_schema.sql
│   ├── 2_add_format.sql
│   └── 3_add_tracks.sql
├── liquibase/
│   └── changelog.xml        ← references files in migrations/
└── queries/
    └── ...
```

In your `changelog.xml`:

```xml
<databaseChangeLog>
  <changeSet id="1" author="dev">
    <sqlFile path="../migrations/1_initial_schema.sql"/>
  </changeSet>
  <changeSet id="2" author="dev">
    <sqlFile path="../migrations/2_add_format.sql"/>
  </changeSet>
</databaseChangeLog>
```

Both pGenie and Liquibase now read the same SQL files. pGenie never writes to the `DATABASECHANGELOG` table or interacts with Liquibase in any way.

---

## Using Liquibase SQL-format changelogs

Liquibase also supports a plain SQL changelog format that embeds changesets directly:

```sql
-- liquibase formatted sql

-- changeset dev:1
create table artist (
  id   int4 not null generated always as identity primary key,
  name text not null
);

-- changeset dev:2
alter table artist add column bio text null;
```

You can share this file with pGenie by placing it in `migrations/`:

```
migrations/
├── 1_schema.sql   ← Liquibase SQL-format changelog, also used by pGenie
```

pGenie ignores Liquibase's `--liquibase formatted sql` and `--changeset` comment directives and applies the entire file as plain SQL. This works correctly as long as the SQL statements are valid PostgreSQL in the order they appear.

---

## Inline XML changesets

If your changesets use Liquibase's built-in change types (e.g. `<createTable>`, `<addColumn>`) rather than raw SQL, pGenie cannot use the changelog directly. In this case, maintain a parallel `migrations/` directory with equivalent plain SQL files that pGenie can use for analysis.

Many teams adopt the `sqlFile` approach described above for this reason: it keeps the authoritative SQL in plain files and uses Liquibase only for change tracking and deployment orchestration.

---

## Checklist

- [ ] Liquibase changesets reference external SQL files that are also present in pGenie's `migrations/` directory.
- [ ] SQL files sort in the correct schema-application order under natural sort.
- [ ] pGenie's `migrations/` directory contains all SQL that defines the schema, in order.
- [ ] pGenie is run for analysis only (`pgn analyse`) or code generation (`pgn generate`); it never writes to the `DATABASECHANGELOG` table.
