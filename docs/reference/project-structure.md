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
    └── hasql/
        └── ...
```

---

## `migrations/`

Contains SQL migration files that define your database schema. Files are applied to a temporary PostgreSQL instance in **lexicographic sort order** by filename. See [Writing Migrations](../guides/writing-migrations.md) for details.

---

## `queries/`

Contains parameterized SQL query files (one query per file). After analysis, pGenie writes a `.sig1.pgn.yaml` signature file alongside each `.sql` file. See [Writing Queries](../guides/writing-queries.md) and the [Query Signature File](query-signature-file.md) reference for details.

---

## `project1.pgn.yaml`

The project configuration file. It specifies the project's namespace, name, version, and the list of code generators to run. See the [Project File](project-file.md) reference for details.

---

## `freeze1.pgn.yaml`

Auto-generated lock file that records the content hash of each generator URL. Ensures reproducible code generation. Commit this file to version control. See [How pGenie Works](../how-it-works.md) for details.

---

## `artifacts/`

The output directory. Each configured generator produces a subdirectory here named after its key in `project1.pgn.yaml`. The contents depend on the generator; for `haskell-hasql.gen` this is a Haskell Cabal library.

Whether to commit `artifacts/` is a project choice—see [Generating Code](../guides/generating-code.md).
