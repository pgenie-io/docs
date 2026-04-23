# Project File

The project file (`project1.pgn.yaml`) configures a pGenie project. It must be placed in the root of your project directory.

---

## Format

```yaml
# Namespace.
# For personal projects, use your username.
# For organizational projects, use the organization name.
# Affects the top-level namespace in generated artifacts.
space: my_space

# Project name.
# Affects the second-level namespace and library names in generated artifacts.
name: music_catalogue

# Version for generated artifacts.
# Must follow SemVer (https://semver.org/).
# Individual generators may adapt this to their ecosystem's conventions
# (e.g. the haskell generator prepends "0." to comply with Haskell's PVP).
version: 1.0.0

# Major PostgreSQL version to use for SQL analysis.
# When using --database-url, this must match the live server's major version.
# If omitted, pGenie defaults to 18.
postgres: 18

# Code generators to run.
# Each key is the name of the output directory under artifacts/.
# Each value is a URL pointing to a Dhall generator entry point.
# If this map is empty, pGenie only validates your schema and queries.
artifacts:
  haskell: https://raw.githubusercontent.com/pgenie-io/haskell.gen/v0.2.3/gen/Gen.dhall
```

---

## Fields

### `space`

**Type:** string  
**Required:** yes

The top-level namespace for generated artifacts. Typically your GitHub username or organization name. Use **snake_case**.

### `name`

**Type:** string  
**Required:** yes

The project name. Used as the second-level namespace and as the library name in generated packages. Use **snake_case**.

### `version`

**Type:** string (SemVer)  
**Required:** yes

The version to embed in generated artifacts. Must be a valid [Semantic Version](https://semver.org/) string (e.g. `1.0.0`, `0.3.1`).

Individual generators may transform this version to comply with their ecosystem's conventions. For example, the haskell generator prepends `0.` to produce a PVP-compatible version for Haskell (`1.0.0` → `0.1.0.0`).

### `postgres`

**Type:** integer  
**Required:** no  
**Default:** `18`

The major PostgreSQL version pGenie uses for SQL analysis.

In the default Docker execution mode, pGenie starts a temporary PostgreSQL instance of this version.

In live instance mode (`--database-url`), the connected PostgreSQL server must already be running at this same **major version**.

If you omit this field, pGenie analyses your SQL against PostgreSQL 18.

### `artifacts`

**Type:** map of string → generator entry  
**Required:** no

A map from output directory names to generator configurations. Add it only when you want pGenie to generate code. Each value can be:

- A **URL string** pointing directly to the generator's entry-point Dhall file (short form):

    ```yaml
    artifacts:
      haskell: https://raw.githubusercontent.com/pgenie-io/haskell.gen/v0.2.3/gen/Gen.dhall
    ```

- An **object** with `gen` and `config` fields, for generators that accept configuration (long form):

    ```yaml
    artifacts:
      haskell:
        gen: https://raw.githubusercontent.com/pgenie-io/haskell.gen/v0.2.3/gen/Gen.dhall
        config:
    ```

The short form (bare URL) is equivalent to the long form with an empty `config`.

- Keys become subdirectory names under `artifacts/`.
- Generator URLs should reference a specific tagged version (e.g. `.../v0.1.0/gen/Gen.dhall`) to ensure reproducibility.

If you omit `artifacts` entirely, pGenie validates your schema and queries without generating any code.

---

## Versioning

The filename includes a version suffix (`project1.pgn.yaml`). This `1` refers to the version of the project file **format** itself, not your project's version. Future breaking changes to the format would introduce `project2.pgn.yaml`.
