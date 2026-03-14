# Implementing Custom Generators

pGenie's code generation is fully open and extensible. Anyone can implement a generator for a new target language, framework, or output format.

---

## Overview

A generator is a [Dhall](https://dhall-lang.org/) program that receives a structured description of your project and returns a list of output files. Generators are referenced by URL in `project1.pgn.yaml`, so they can be hosted anywhere (GitHub, a personal server, etc.).

---

## The Generator Interface

Every generator must be a Dhall expression of the type provided by the pGenie SDK (`Sdk.module`). The SDK is available as a Dhall package from the pGenie generator dependencies.

The minimal structure of a generator entry point (`Gen.dhall`):

```dhall
let Deps = ./Deps/package.dhall

let Sdk = Deps.Sdk

in  Sdk.module { major = 1, minor = 0 } ./Config.dhall ./compile.dhall
```

Where:

- `{ major = 1, minor = 0 }` declares which version of the pGenie generator SDK this generator targets.
- `./Config.dhall` defines the schema of any user-supplied configuration (use `{} : Type` for no configuration).
- `./compile.dhall` is the main compilation function that receives the project model and returns a list of generated files.

---

## The Compilation Function

`compile.dhall` receives the full project model and returns a list of file paths and contents:

```dhall
\(project : Sdk.ProjectModel) ->
  [ { path = "src/Queries.hs"
    , content = generateHaskellModule project
    }
  ]
```

The `Sdk.ProjectModel` type contains:

- `space` - the project's namespace
- `name` - the project's name
- `version` - the project's version
- `queries` - a list of query descriptors, each containing the query name, parameters, and result columns with their full type information
- `schema` - type declarations (enumerations, composite types) from the schema

---

## Example: The hasql Generator

The official [haskell-hasql.gen](https://github.com/pgenie-io/haskell-hasql.gen) generator is a good reference implementation. Its structure:

```
gen/
├── Gen.dhall          ← entry point
├── Config.dhall       ← configuration schema (empty)
├── compile.dhall      ← main compilation function
├── Deps/              ← SDK and shared utilities
├── Interpreters/      ← type mappers (Postgres → Haskell)
└── Templates/         ← Haskell code templates
```

Browse the source at [github.com/pgenie-io/haskell-hasql.gen](https://github.com/pgenie-io/haskell-hasql.gen).

---

## Distributing Your Generator

1. Host your generator files at a stable URL (e.g. a GitHub repository with tagged releases).
2. Tag each release (e.g. `v1.0.0`) so users can pin the URL.
3. Users reference your generator in their `project1.pgn.yaml`:

    ```yaml
    artifacts:
      my-gen: https://raw.githubusercontent.com/you/my-gen/v1.0.0/gen/Gen.dhall
    ```

---

## Tips

- **Use Dhall's type system**: define explicit types for your templates and intermediate data structures. Dhall's type checker will catch mistakes early.
- **Keep templates small**: break large templates into composable functions. Dhall's import system makes this straightforward.
- **Test with the demo project**: use the [pgenie-io/demo](https://github.com/pgenie-io/demo) project as a test fixture for your generator - it exercises enumerations, composite types, arrays, and various query patterns.
