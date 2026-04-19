# Project Structure

A pGenie project is a directory with the following layout:

```
my-project/
├── project1.pgn.yaml         # Project configuration (required)
├── freeze1.pgn.yaml          # Generator lock file (auto-generated)
├── migrations/               # SQL migration files
│   ├── 1.sql
│   ├── 2.sql
│   └── ...
├── queries/                  # Parameterized SQL query files
│   ├── my_query.sql
│   ├── my_query.sig1.pgn.yaml   # Query signature (auto-generated)
│   └── ...
└── artifacts/                # Generated client libraries (output)
    └── haskell/
        └── ...
    └── rust/
        └── ...
```

---

## `migrations/`

Contains SQL migration files that define your database schema. Files are applied to a temporary PostgreSQL instance in **natural sort order** by filename (so `10.sql` correctly follows `9.sql`). See [Writing Migrations](../guides/writing-migrations.md) for details.

---

## `queries/`

Contains parameterized SQL query files (one query per file). After the first analysis, pGenie writes a `.sig1.pgn.yaml` signature file alongside each `.sql` file. On subsequent runs pGenie validates the existing signature against the live schema rather than overwriting it. See [Writing Queries](../guides/writing-queries.md) and the [Query Signature File](query-signature-file.md) reference for details.

---

## `project1.pgn.yaml`

The project configuration file. It specifies the project's namespace, name, version, PostgreSQL major version for analysis, and any configured code generators. See the [Project File](project-file.md) reference for details.

---

## `freeze1.pgn.yaml`

Auto-generated lock file that records the content hash of each configured generator URL. Ensures reproducible code generation. Commit this file to version control. See the [Freeze File](freeze-file.md) reference for details.

---

## `artifacts/`

The output directory. Each configured generator produces a subdirectory here named after its key in `project1.pgn.yaml`. The contents depend on the generator; for `haskell.gen` this is a Haskell Cabal library.

Whether to commit `artifacts/` is a project choice - see [Generating Code](../guides/generating-code.md).
