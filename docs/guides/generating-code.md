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
2. Apply all migrations in `migrations/` in natural sort order by filename.
3. Analyze all queries in `queries/`.
4. For each query: write a signature file (`*.sig1.pgn.yaml`) if none exists, or compare the freshly-resolved signature against the existing one and fail if they differ.
5. Run each configured code generator.
6. Write the generated artifacts to `artifacts/<generator-name>/`.
7. Shut down the container.

---

## Output Structure

After a successful run, your project directory will look like this:

```
my-project/
├── project1.pgn.yaml
├── freeze1.pgn.yaml          ← created and updated on first use of a generator
├── migrations/
│   ├── 1.sql
│   └── 2.sql
├── queries/
│   ├── insert_album.sql
│   ├── insert_album.sig1.pgn.yaml      ← created on first run (not overwritten)
│   ├── select_album_by_name.sql
│   └── select_album_by_name.sig1.pgn.yaml  ← created on first run (not overwritten)
└── artifacts/
    └── hasql/                ← generated Haskell library
        └── ...
```

---

## Committing Generated Artifacts

Whether to commit the `artifacts/` directory to version control is a matter of preference:

- **Commit artifacts** if you want the generated library available without running pGenie (e.g. for consumers who don't have pGenie installed).
- **Exclude artifacts** (via `.gitignore`) if you prefer to generate them in CI and distribute as uploaded packages (e.g., via a package registry or by attaching to a release via [GitHub Actions](https://github.com/actions/upload-artifact)).

Signature files (`*.sig1.pgn.yaml`) and the freeze file (`freeze1.pgn.yaml`) should **always** be committed - they record the type contracts of your queries and pin the generator versions for reproducible builds.

---

## Working with Signature Files

Signature files (`.sig1.pgn.yaml`) record the resolved type contract for each query. Understanding how pGenie handles them is important for day-to-day use.

### Lifecycle

| Event | What pGenie does |
|---|---|
| First run (no sig file) | Writes the sig file with the types resolved from the database |
| Subsequent run (sig file present) | Compares resolved types against the sig file; **fails the build** if they differ |
| Sig file deleted | Treated as "first run" — pGenie regenerates it |

pGenie **never silently overwrites** an existing signature file.

### Editing a signature file

You can edit a signature file by hand to tighten constraints. The most common edit is marking a parameter as non-nullable when you know callers will always pass a concrete value:

```yaml
parameters:
  id:
    type: int8
    not_null: true   # ← set to true manually; pGenie defaulted to false
```

After editing, commit the file. On the next run pGenie will use your edited version as the expected signature.

### Regenerating a signature file

To regenerate a signature file from scratch (for example, after a schema change that you want pGenie to re-resolve):

1. Delete the existing `.sig1.pgn.yaml` file.
2. Run `pgn generate` (or `pgn analyse`). pGenie will write a fresh sig file with the types from the current schema.

### Schema drift detection

If a migration changes a column type that a query references, the next `pgn generate` run will detect that the freshly-resolved signature no longer matches the committed sig file and will **fail the build**. To resolve the failure, either:

- Update the sig file to reflect the new reality (acknowledging the breaking change), or
- Revert the migration so it no longer affects the query's type signature.

This design ensures that every schema change that affects a query's API is an explicit, reviewable commit in version control.

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
