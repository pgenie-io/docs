# Using pGenie with AI

AI agents (Copilot, Cursor, Claude, etc. in agent mode) are excellent at drafting SQL. pGenie is how you verify it.

---

## How It Works

In agent mode, the AI can read your project files directly — it already knows your full schema from the migrations and your existing query conventions from the query files. You just describe what you want.

The agent writes the SQL, saves the file, and then you run pGenie to verify:

```
Describe requirement  ──▶  Agent writes SQL  ──▶  pgn generate  ──▶  Ship
```

If the SQL is wrong — bad column reference, type mismatch, invalid DDL — `pgn generate` fails with a precise error. Share it with the agent and iterate.

---

## Workflow

```
1.  Describe your requirement to the agent.
2.  Agent writes and saves the migration or query file.
3.  Run `pgn generate` locally.
     ├── PASS → commit the SQL + sig file(s) + freeze file.
     └── FAIL → share the error with the agent, iterate.
4.  Open a pull request.
5.  CI runs `pgn analyse` automatically.
     ├── PASS → merge with confidence.
     └── FAIL → fix before merging.
```

---

## Migrations

Ask the agent to add the next migration file. Since it can read the existing migrations, it knows the current schema and will number the file correctly.

After the agent saves the file, run `pgn generate`. pGenie applies all migrations in sequence against a temporary database and fails immediately if the DDL is invalid.

---

## Queries

Ask the agent to write a query. It reads the migrations to get exact column names, types, and nullability — no need to paste a schema summary.

Remind it to use `$param_name` syntax (snake_case) for named parameters.

After the agent saves the file, run `pgn generate`. pGenie prepares the statement against the live schema and infers parameter and result types. Inspect the generated `.sig1.pgn.yaml` file to confirm the types look right.

!!! tip
    Commit the signature file. It acts as a diff target in pull requests — reviewers can see exactly how a change affected query types.

---

## Refactoring Queries

Ask the agent to rewrite a query for performance or clarity. Tell it to leave the `.sig1.pgn.yaml` file in place.

Run `pgn generate`:

- Same result types → succeeds silently.
- Changed types or nullability → build fails, showing the diff. Decide whether to accept the change (update the sig file) or fix the query.

This makes the impact of AI-driven refactors explicit rather than silent.

---

## Schema Drift

When a new migration changes a column, `pgn analyse` re-validates every query against the updated schema. If an existing query is now invalid, the build fails with a clear message. Update the query and regenerate its signature file.

---

## Related Guides

- [Writing Migrations](writing-migrations.md)
- [Writing Queries](writing-queries.md)
- [Using pGenie in CI/CD](cicd.md)
- [Generating Code](generating-code.md)
