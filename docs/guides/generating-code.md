# Generating Code

This guide explains how to run pGenie and what it produces.

---

## Running the Generator

From the root of your project (the directory containing `project1.pgn.yaml`), run:

```bash
pgn generate
```

pGenie will:

1. Start a temporary PostgreSQL Docker container.
2. Apply all migrations in `migrations/` in filename order.
3. Analyze all queries in `queries/`.
4. Write or update signature files (`*.sig1.pgn.yaml`) in `queries/`.
5. Run each configured code generator.
6. Write the generated artifacts to `artifacts/<generator-name>/`.
7. Shut down the container.

---

## Output Structure

After a successful run, your project directory will look like this:

```
my-project/
├── project1.pgn.yaml
├── freeze1.pgn.yaml          ← created/updated after first run
├── migrations/
│   ├── 1.sql
│   └── 2.sql
├── queries/
│   ├── insert_album.sql
│   ├── insert_album.sig1.pgn.yaml      ← created/updated
│   ├── select_album_by_name.sql
│   └── select_album_by_name.sig1.pgn.yaml  ← created/updated
└── artifacts/
    └── hasql/                ← generated Haskell library
        └── ...
```

---

## Validation Only

If you do not configure any `artifacts` in `project1.pgn.yaml`, pGenie will still analyze your schema and queries and report any errors - without generating any code. This is useful as a CI step to catch schema/query mismatches early:

```yaml
space: my_space
name: my_project
version: 1.0.0

artifacts: {}
```

---

## Continuous Integration

Add pGenie as a CI check to catch schema drift and query errors before they reach production. A minimal GitHub Actions step:

```yaml
- name: Validate schema and queries
  run: pgn generate
```

Make sure Docker is available in your CI runner (most hosted runners include Docker by default).

---

## Committing Generated Artifacts

Whether to commit the `artifacts/` directory to version control is a matter of preference:

- **Commit artifacts** if you want the generated library available without running pGenie (e.g. for consumers who don't have pGenie installed).
- **Exclude artifacts** (via `.gitignore`) if you prefer to generate them on demand or in CI.

Signature files (`*.sig1.pgn.yaml`) and the freeze file (`freeze1.pgn.yaml`) should **always** be committed - they record the type contracts of your queries and ensure reproducible generation.

---

## Troubleshooting

**Docker not found / not running**

Ensure Docker is installed and the daemon is running:

```bash
docker info
```

**First run hangs at "Loading"**

The first run downloads the PostgreSQL Docker image and caches Dhall generators. This can take 2–3 minutes. Subsequent runs are fast.

**Query analysis error**

If a query references a column that does not exist in the current schema, pGenie will report an error. Check that:

- All referenced tables and columns exist after applying the migrations.
- Parameters and column names are spelled correctly.
- The parameter syntax uses `$snake_case` names.
