# Integrating pGenie with Migration Management Tools

pGenie uses your SQL migration files **locally** — it applies them to a temporary PostgreSQL container to analyse your queries and generate code. It never touches your production database. This makes it straightforward to use pGenie alongside any SQL migration management tool.

---

## How pGenie uses migrations

When you run `pgn generate` or `pgn analyse`, pGenie:

1. Starts a disposable PostgreSQL container.
2. Applies every `.sql` file in your `migrations/` directory, in **natural sort order** by filename.
3. Analyses your queries against the resulting schema.
4. Tears down the container.

Your production database is never involved. The migration files in `migrations/` are purely an input to pGenie's analysis pipeline.

---

## General integration approach

The simplest integration strategy is to **share the same SQL files** between pGenie and your migration tool:

- If your migration tool already stores plain SQL files on disk (e.g. Flyway, Sqitch), configure pGenie's `migrations/` to point at the same files (or copy/symlink them).
- If your migration tool uses a proprietary format (e.g. Liquibase XML changesets), maintain a parallel set of plain SQL files in `migrations/` that pGenie can use for analysis. Many Liquibase projects already include SQL file includes that can be reused.

The sections below give tool-specific guidance.

---

## Supported tools

- [Flyway](flyway.md) — Versioned SQL migration files
- [Liquibase](liquibase.md) — Changelog-based migrations
- [Sqitch](sqitch.md) — Plan-based SQL change management
