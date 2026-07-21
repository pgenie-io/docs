# Implementing Custom Generators

pGenie's code generation is designed to be extensible. You can implement a generator for a new target language, framework, or output format and distribute it simply via a URL. No need for PRs or approval from the pGenie maintainers.

---

## Overview

A generator is a [Dhall](https://dhall-lang.org/) program that receives a structured description of your project and returns a list of output files. Generators are referenced by URL in `project1.pgn.yaml`, so they can be hosted anywhere (GitHub, a personal server, etc.).

You don't need to learn Dhall or Haskell to write one. The recommended path is to use the [`maintain-pgenie-gen` skill](https://github.com/pgenie-io/maintain-pgenie-gen.skill): you create a small reference project showing exactly what the generator should produce, and the skill converges a working generator from that design artifact.

---

## Quick Start

1. Install the skill into your agent's skills directory:

    ```bash
    git clone https://github.com/pgenie-io/maintain-pgenie-gen.skill <your-agent-skills-dir>/maintain-pgenie-gen
    ```

    See the [skill repository](https://github.com/pgenie-io/maintain-pgenie-gen.skill) for the full install instructions and agent-specific details.

2. Create a design artifact: a hand-written project showing what the generator should output for the [`demo`](https://github.com/pgenie-io/demo) project (`./queries`, `./migrations`, `./project1.pgn.yaml`). Browse the [`./artifacts`](https://github.com/pgenie-io/demo/tree/master/artifacts) directory in that repo for examples produced by other generators.

3. Ask your agent to implement a pGenie generator from your design artifact.

4. Iterate on the design artifact and re-invoke the skill until the generator's output matches it.

---

## Step-by-Step Workflow

### 1. Pick your target

Decide which language, framework, or format you want to generate. Existing pGenie generators include [java.gen](https://github.com/pgenie-io/java.gen), [haskell.gen](https://github.com/pgenie-io/haskell.gen), and [rust.gen](https://github.com/pgenie-io/rust.gen); their design artifacts ([java.gen-design](https://github.com/pgenie-io/java.gen-design), [haskell.gen-design](https://github.com/pgenie-io/haskell.gen-design), etc.) are good models for how a reference output can look.

### 2. Create the design artifact

Clone the [`demo`](https://github.com/pgenie-io/demo) project and manually author the files you wish the generator produced for it. There is no required structure — any layout that clearly shows the expected output works. Make sure it:

- covers the demo queries, including parameters and result columns;
- shows how schema types (enumerations, composites, arrays) map to your target;
- demonstrates naming conventions and file organization.

### 3. Invoke the skill

Open your agent and point it at your design artifact and a path for the generator repo. For example:

```text
Implement a pGenie generator from the design artifact at ./my-design that targets Kotlin with Exposed.
Write the generator into ./my-gen and keep running it against the demo project until its output matches the design artifact.
```

The skill will study the [generator architecture](https://github.com/pgenie-io/gen-sdk/blob/master/docs/generator-architecture.md), validate the design artifact, ask you about anything it doesn't pin down (type mappings, how patterns extrapolate beyond the demo, etc.), and implement the generator in focused tasks.

### 4. Iterate on the design

The design artifact is the living spec. If the generated output is not quite right, change the artifact to say what you want, then tell your agent to re-converge the generator. Repeat until the diff between the generator's output and your design artifact is empty.

---

## Validating the Generator

Once the skill reports convergence, validate the generator yourself:

1. Point a `project1.pgn.yaml` at the generator's entry point URL (local `file://` or hosted).
2. Run pGenie's generation command for the demo project.
3. Compare the generated files against your design artifact with your preferred diff tool.
4. If anything is off, update the design artifact and re-invoke the skill.

When the diff is empty, the generator is ready to use and publish.

---

## Distributing Your Generator

1. Host your generator files at a stable URL (e.g. a GitHub repository with tagged releases).
2. Tag each release (e.g. `v1.0.0`) so users can pin the URL. You can also reference a specific commit hash instead of a tag — both are equally reproducible, but a named tag is usually more convenient for users.
3. Users reference your generator in their `project1.pgn.yaml`:

    ```yaml
    artifacts:
      my-gen: https://raw.githubusercontent.com/you/my-gen/v1.0.0/gen/Gen.dhall
    ```

---

## The Generator Interface

If you prefer to write a generator by hand, every generator must be a Dhall expression of the type provided by the pGenie SDK (`Sdk.module`). The SDK is available as a Dhall package from the pGenie generator dependencies.

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

### The Compilation Function

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

### Example: The hasql Generator

The official [haskell.gen](https://github.com/pgenie-io/haskell.gen) generator is a good reference implementation. Its structure:

```
gen/
├── Gen.dhall          ← entry point
├── Config.dhall       ← configuration schema (empty)
├── compile.dhall      ← main compilation function
├── Deps/              ← SDK and shared utilities
├── Interpreters/      ← type mappers (Postgres → Haskell)
└── Templates/         ← Haskell code templates
```

Browse the source at [github.com/pgenie-io/haskell.gen](https://github.com/pgenie-io/haskell.gen).

---

## Tips

- **Start with the demo project**: the [`demo`](https://github.com/pgenie-io/demo) project exercises enumerations, composite types, arrays, and various query patterns. A design artifact that covers the demo is usually enough to bootstrap a production-quality generator.
- **Make the design artifact explicit**: pin down type mappings, naming conventions, and file layout in the artifact itself. The more concrete the artifact, the fewer questions the skill needs to ask.
- **Treat the artifact as the spec**: when the generator drifts, update the design artifact first and re-converge. The acceptance test is a diff.
- **Reuse existing design artifacts**: study [java.gen-design](https://github.com/pgenie-io/java.gen-design), [rust.gen-design](https://github.com/pgenie-io/rust.gen-design), [c-sharp.gen-design](https://github.com/pgenie-io/c-sharp.gen-design), and [ts.gen-design](https://github.com/pgenie-io/ts.gen-design) for conventions that match your target ecosystem.
- **If writing Dhall by hand**, use Dhall's type system: define explicit types for your templates and intermediate data structures. Dhall's type checker will catch mistakes early.
