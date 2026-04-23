# Managing Indexes

pGenie can analyze your queries and existing database indexes to keep your index set lean and effective. It both suggests new indexes to cover sequential scans and identifies existing indexes that are no longer used by any query and can be safely removed.

---

## Running the Index Manager

From the root of your project, run:

```bash
pgn manage-indexes
```

Or, in live instance mode:

```bash
pgn --database-url "postgresql://user:password@localhost:5432/postgres" manage-indexes
```

pGenie will:

1. Prepare a temporary PostgreSQL analysis environment.
2. Apply all migrations in `migrations/`.
3. Query the database catalog to read all existing non-primary indexes.
4. Run `EXPLAIN` on each query in `queries/` to detect sequential scans.
5. Compare the set of existing indexes against the observed query needs.
6. Print a ready-to-use SQL migration to stdout that drops redundant or unused indexes and creates missing ones.

---

## Interpreting the Output

The command outputs a SQL migration combining all recommended changes. For example:

```sql
-- Auto-generated migration to optimize indexes

-- Drop redundant/excessive indexes
-- album_recording_idx on (recording) is not used by observed query needs
DROP INDEX "public"."album_recording_idx";

-- Create missing indexes
CREATE INDEX ON album (format);

CREATE INDEX ON album (name);
```

Each section explains what is being done and why:

- **Drop redundant/excessive indexes** — indexes that are not used by any observed query on the same table, exact duplicates of another index, or composite indexes whose trailing columns are never needed.
- **Create missing indexes** — new indexes for columns that appear in `WHERE` clauses but have no covering index, causing sequential scans.

---

## Writing the Migration to a File

To have pGenie write the migration directly to a numbered file in `migrations/` instead of just printing it, pass `--add-migration`:

```bash
pgn manage-indexes --add-migration
```

pGenie will determine the next available migration number (e.g. `5.sql`) and write the migration there automatically. This requires that all existing migration files follow the `N.sql` naming convention.

---

## Notes

- Index management is heuristic. pGenie reasons from the observed query patterns in your `queries/` directory — it cannot know about queries issued by other clients or future access patterns. Always review the suggested migration before applying it.
- `pgn manage-indexes` on its own only prints the migration to stdout and does not modify any project files. To persist it either use `--add-migration` or pipe its stdout to a file.
- The command uses the same temporary analysis environment as `pgn generate`: Docker by default, or a live PostgreSQL instance when `--database-url` is provided.
- In live instance mode, the `postgres` field in `project1.pgn.yaml` must match the connected server's major version, and the connected user must be able to create databases.
- If you want to keep a redundant index for any reason (e.g. it is used by external tools), you can pass `--allow-redundant-indexes` to emit warnings instead of drop statements for those cases.
