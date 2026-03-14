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
# (e.g. the hasql generator prepends "0." to comply with Haskell's PVP).
version: 1.0.0

# Code generators to run.
# Each key is the name of the output directory under artifacts/.
# Each value is a URL pointing to a Dhall generator entry point.
# If this map is empty, pGenie only validates your schema and queries.
artifacts:
  hasql: https://raw.githubusercontent.com/pgenie-io/haskell-hasql.gen/v0.1.0/gen/Gen.dhall
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

Individual generators may transform this version to comply with their ecosystem's conventions. For example, the hasql generator prepends `0.` to produce a PVP-compatible version for Haskell (`1.0.0` → `0.1.0.0`).

### `artifacts`

**Type:** map of string → URL  
**Required:** yes (but may be empty)

A map from output directory names to generator entry-point URLs. Each generator is a Dhall program hosted at a URL.

- Keys become subdirectory names under `artifacts/`.
- Values must be URLs pointing to a `Gen.dhall` entry point.
- Use tagged URLs (e.g. `.../v0.1.0/gen/Gen.dhall`) to ensure reproducibility.

If the map is empty (`artifacts: {}`), pGenie validates your schema and queries without generating any code.

---

## Versioning

The filename includes a version suffix (`project1.pgn.yaml`). This `1` refers to the version of the project file **format** itself, not your project's version. Future breaking changes to the format would introduce `project2.pgn.yaml`.
