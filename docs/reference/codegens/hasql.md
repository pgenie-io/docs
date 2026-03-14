# hasql Generator

The `haskell-hasql.gen` generator produces a Haskell library that exposes each SQL query as a typed [`Statement`](https://hackage.haskell.org/package/hasql/docs/Hasql-Statement.html) value from the [hasql](https://hackage.haskell.org/package/hasql) library.

**Repository**: [github.com/pgenie-io/haskell-hasql.gen](https://github.com/pgenie-io/haskell-hasql.gen)

---

## Setup

In your `project1.pgn.yaml`:

```yaml
artifacts:
  hasql: https://raw.githubusercontent.com/pgenie-io/haskell-hasql.gen/v0.1.0/gen/Gen.dhall
```

The output is written to `artifacts/hasql/`.

---

## What is Generated

For each query, the generator produces a `Statement` value with fully typed parameters and results. The generated library includes:

- A Cabal package file (`*.cabal`) ready to add as a dependency.
- One Haskell module per query, plus a top-level module that re-exports everything.
- Data types for composite types and enumerations defined in your schema.
- Proper nullability mapping (`Maybe` for nullable columns, direct types for `NOT NULL`).

### Example

Given the query:

```sql
-- queries/select_album_by_name.sql

select id, name, released, format, recording
from album
where name = $name
```

The generator produces a `Statement` with:

- **Parameter**: `Maybe Text` (nullable `text`)
- **Result row**: a record with `id :: Int64`, `name :: Text`, `released :: Maybe Day`, `format :: Maybe AlbumFormat`, `recording :: Maybe RecordingInfo`

---

## Type Mappings

### Primitive Types

| PostgreSQL | Haskell |
|---|---|
| `bool` | `Bool` |
| `bytea` | `ByteString` |
| `char` | `Char` |
| `cidr` / `inet` | `IPRange` / `IP` |
| `date` | `Day` |
| `float4` | `Float` |
| `float8` | `Double` |
| `int2` | `Int16` |
| `int4` | `Int32` |
| `int8` | `Int64` |
| `interval` | `DiffTime` |
| `json` / `jsonb` | `Value` (aeson) |
| `numeric` | `Scientific` |
| `text` | `Text` |
| `time` | `TimeOfDay` |
| `timestamp` | `LocalTime` |
| `timestamptz` | `UTCTime` |
| `timetz` | `TimeOfDay` |
| `uuid` | `UUID` |

### Composite Types

Composite types are mapped to Haskell record types. Each field in the composite becomes a record field, with nullability respected.

### Enumerations

PostgreSQL enumerations become Haskell `newtype` wrappers or sum types (depending on generator version).

### Arrays

Arrays of supported element types are mapped to `Vector` from the [vector](https://hackage.haskell.org/package/vector) library.

### Nullability

- `NOT NULL` columns / parameters → direct Haskell type (e.g. `Text`)
- Nullable columns / parameters → `Maybe` (e.g. `Maybe Text`)

---

## Versioning

Haskell uses [PVP](https://pvp.haskell.org/) versioning. The generator adapts the `version` field from your `project1.pgn.yaml` (SemVer) to PVP by prepending `0.`:

| SemVer | PVP |
|---|---|
| `1.0.0` | `0.1.0.0` |
| `2.3.1` | `0.2.3.1` |

---

## Further Documentation

Visit the [haskell-hasql.gen repository](https://github.com/pgenie-io/haskell-hasql.gen) for the full documentation, including:

- Complete generated output examples (see `demo-output/`)
- Advanced configuration
- Changelog
