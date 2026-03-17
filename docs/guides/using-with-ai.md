# Using pGenie with AI

LLMs are excellent at drafting SQL. pGenie is how you verify it.

This guide explains how to integrate an AI assistant (ChatGPT, Claude, Cursor, Copilot, etc.) into your pGenie workflow so you can move fast without sacrificing correctness.

---

## The Core Idea

AI can generate a migration, a query, or a whole schema in seconds. The problem is that output is probabilistic — column types might be wrong, nullability guessed, indexes omitted, or a later migration can silently invalidate an earlier AI-written query.

pGenie's role in an AI-assisted workflow is simple: **run it after every AI change**. If the SQL is wrong, you find out before anything ships.

```
AI drafts SQL  ──▶  pGenie verifies  ──▶  Ship with confidence
```

---

## Prompting for Migrations

When asking an AI to write or extend a schema, give it the context it needs to produce valid PostgreSQL DDL that pGenie can apply.

### What to include in your prompt

- The existing migration files (or a description of the current schema).
- The naming conventions you use (e.g. snake_case identifiers, `not null` everywhere except documented exceptions).
- The target change — as a precise requirement, not a vague "add user stuff".

**Example prompt:**

```
I'm using pGenie. My current schema is defined by these migrations:

-- migrations/1.sql
create table "user" (
  "id"   int4 not null generated always as identity primary key,
  "name" text not null
);

Write the next migration to add an "email" column (text, not null, unique)
and a Boolean "is_active" column (not null, default true).
Filename: migrations/2.sql
Use plain PostgreSQL DDL. No ORM extensions.
```

### After you receive the output

1. Save the migration file.
2. Run `pgn generate` (or `pgn analyse` if you do not want to regenerate artifacts yet).
3. pGenie applies all migrations against a temporary database. If the DDL is invalid it fails immediately and tells you what is wrong.

---

## Prompting for Queries

When asking an AI to write a query, paste any relevant table definitions so the model can get column names, types, and nullability right.

**Example prompt:**

```
Write a PostgreSQL query for pGenie that returns all active users
with their email and the number of orders they have placed.

Schema (from my migrations):
- user(id int4, name text, email text, is_active bool)
- order(id int4, user_id int4 references user(id), placed_at timestamptz)

Requirements:
- Named parameters use $param_name syntax (snake_case).
- Filter by $is_active (bool).
- Include a lateral join or subquery to count orders per user.
- Return: user_id, name, email, order_count.
Filename: queries/active_users_with_order_count.sql
```

### After you receive the output

1. Save the query file (delete its `.sig1.pgn.yaml` if one existed, so pGenie regenerates it fresh).
2. Run `pgn generate`.
3. pGenie prepares the statement against the real schema and infers parameter and result types. If the query references a non-existent column, uses the wrong type, or is syntactically invalid, the build fails.
4. Inspect the generated signature file (`queries/active_users_with_order_count.sig1.pgn.yaml`) and confirm the inferred types match your expectations.

!!! tip
    Commit the signature file. It acts as a human-readable diff target in pull requests — reviewers can see exactly how an AI change affected query types.

---

## Prompting for Refactors

AI is useful for proposing performance rewrites, joins, or CTE restructurings. pGenie ensures the refactor does not silently change the result type.

**Workflow:**

1. Ask the AI to rewrite a query (paste the original SQL and the schema).
2. Replace the existing `.sql` file with the new version.
3. **Do not delete the`.sig1.pgn.yaml` file.** Leave it in place.
4. Run `pgn generate`.
   - If the rewrite produces the **same type signature**, generation succeeds.
   - If the rewrite changes a result column type or nullability, pGenie **fails the build** and shows the diff. You can then choose to update the sig file (acknowledging the deliberate change) or fix the query.

This makes the impact of AI-driven refactors explicit and reviewable, not silent.

---

## Schema Drift Protection

Over time, migrations evolve. An AI-drafted query written against last month's schema may no longer be valid after a new migration.

pGenie catches this for you automatically:

1. A developer adds a new migration (human- or AI-written) that changes a column type.
2. CI runs `pgn analyse`.
3. pGenie re-validates every query in `queries/` against the updated schema.
4. If the migration invalidates a query whose signature file is already committed, the build fails with a clear message identifying the query and the type mismatch.

**The fix:** update the query (or the migration) and regenerate the signature file.

---

## Recommended AI-Assisted Workflow

```
1.  Describe your requirement to an AI assistant.
2.  Receive draft SQL (migration or query).
3.  Save the file(s) to the appropriate directory.
4.  Run `pgn generate` locally.
     ├── PASS → commit the SQL + sig file(s) + freeze file.
     └── FAIL → share the error with the AI, iterate.
5.  Open a pull request.
6.  CI runs `pgn analyse` automatically.
     ├── PASS → merge with confidence.
     └── FAIL → fix before merging.
```

This loop keeps AI output honest without slowing you down. Each iteration is fast (a few seconds on a laptop) and the feedback is precise.

---

## Tips for Better AI Output

| Do | Avoid |
|---|---|
| Paste your existing migrations as context | Describing the schema in prose only |
| Specify `not null` policy explicitly | Letting the model decide nullability |
| Ask for a single file at a time | Asking for a whole project in one prompt |
| Request `$param_name` syntax for parameters | Asking for `$1`, `$2` positional parameters |
| Verify with `pgn generate` before committing | Committing unverified AI output directly |

---

## Related Guides

- [Writing Migrations](writing-migrations.md) — Migration file format and naming conventions.
- [Writing Queries](writing-queries.md) — Query file format and parameter syntax.
- [Using pGenie in CI/CD](cicd.md) — Adding `pgn analyse` as a pull-request gate.
- [Generating Code](generating-code.md) — What `pgn generate` produces and how sig files work.
