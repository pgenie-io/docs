# Managing Indexes

pGenie can analyze your queries for sequential scan patterns and suggest PostgreSQL indexes that could improve performance.

---

## Running the Index Manager

From the root of your project, run:

```bash
pgn manage-indexes
```

pGenie will:

1. Start a temporary PostgreSQL Docker container.
2. Apply all migrations in `migrations/`.
3. Run `EXPLAIN` on each query in `queries/`.
4. Identify queries that produce sequential scans on large tables where an index could help.
5. Print suggested `CREATE INDEX` statements.

---

## Interpreting the Output

The command outputs suggested index definitions for any queries where a sequential scan was detected on a predicate column. For example:

```
Suggested indexes:

  CREATE INDEX ON album (name);
  CREATE INDEX ON album (format);
```

These are suggestions based on the query patterns in your `queries/` directory. Review them and decide which to add.

---

## Adding Suggested Indexes

To apply a suggestion, add a migration:

```sql
-- migrations/5.sql

CREATE INDEX ON album (name);
CREATE INDEX ON album (format);
```

After adding the migration, run `pgn generate` (or `pgn manage-indexes` again) to verify the index is recognized.

---

## Notes

- Index suggestions are heuristic. Always review them in the context of your actual data distribution and access patterns.
- `pgn manage-indexes` does not modify your project files—it only prints suggestions.
- The command uses the same ephemeral Docker container approach as `pgn generate`, so Docker must be running.
