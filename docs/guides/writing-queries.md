# Writing Queries

Queries are parameterized SQL statements that pGenie analyzes and includes in the generated client libraries.

---

## Directory

All query files live in the `queries/` directory at the root of your project.

```
my-project/
├── project1.pgn.yaml
├── migrations/
└── queries/
    ├── insert_album.sql
    ├── select_album_by_name.sql
    └── select_album_with_tracks.sql
```

---

## File Format

Each query file contains a single SQL statement. The filename (without extension) becomes the query's name in generated code.

**Filename conventions:**

- Use **snake_case** (e.g. `select_album_by_name.sql`).
- Filenames must end in `.sql` or `.psql`.
- pGenie translates the name to the convention of each target language. For example, `select_album_by_name` becomes `SelectAlbumByName` in Haskell (PascalCase).

---

## Parameters

Named parameters are declared using the `$param_name` syntax, where the name is written in **snake_case**.

```sql
-- queries/select_album_by_name.sql

select id, name, released, format, recording
from album
where name = $name
```

```sql
-- queries/insert_album.sql

insert into album (name, released, format, recording)
values ($name, $released, $format, $recording)
returning id
```

- A parameter may be used more than once in the same query.
- Types and nullability are inferred automatically by pGenie from the database schema, query context and [signature files](../reference/query-signature-file.md).
- Parameter names are mapped to appropriate types in each generated language.

---

## Result Sets

Any `SELECT` statement (or `INSERT … RETURNING`, `UPDATE … RETURNING`, `DELETE … RETURNING`) produces a result set. pGenie infers the column names, types, and nullability from the query and the schema.

```sql
-- queries/select_album_with_tracks.sql

select id, name, tracks, disc
from album
where id = $id
```

---

## Supported Query Types

Since pGenie uses Postgres itself for analysis, it supports the full range of PostgreSQL query types including CTEs, window functions and subqueries. No exceptions or limitations. If it runs in Postgres, pGenie can analyze it.

---

## Complex Types

Queries can reference composite types, enumerations, and arrays defined in your migrations:

```sql
-- queries/select_album_by_format.sql

select id, name, released, format, recording
from album
where format = $format
```

Here `$format` is of type `album_format` (a custom enum), and `recording` in the result is of type `recording_info` (a composite type). pGenie resolves these automatically and generates the appropriate data types in each target language.

---

## Signature Files

After each successful analysis run, pGenie writes a **signature file** alongside each query file:

```
queries/
├── select_album_by_name.sql
├── select_album_by_name.sig1.pgn.yaml   ← generated
```

The signature file records the resolved parameter types, result column types, and cardinality. Example:

```yaml
parameters:
  name:
    type: text
    not_null: false
result:
  cardinality: many
  columns:
    id:
      type: int8
      not_null: true
    name:
      type: text
      not_null: true
    released:
      type: date
      not_null: false
```

Signature files should be **committed to version control**. They serve as a stable, reviewable record of each query's type contract and enable reproducible code generation. See [Query Signature File](../reference/query-signature-file.md) for the full format.

---

## Tips

- **One query per file**: each `.sql` file should contain exactly one statement.
- **Use `RETURNING`** on write queries when you need the generated IDs or affected column values.
- **Descriptive names matter**: the filename is used as the function name in generated code, so prefer `select_active_users_by_organization` over `q1`.
