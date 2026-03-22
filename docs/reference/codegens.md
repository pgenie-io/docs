# Code Generators

Code generators are the plugins that turn pGenie's analysis output into idiomatic client libraries for specific programming languages and libraries.

---

## How Generators Work

Each generator is a [Dhall](https://dhall-lang.org/) program hosted at a URL. pGenie downloads the generator, evaluates it with the project model (schema + queries + configuration), and writes the resulting files to `artifacts/<name>/`.

Generators are versioned and pinned via `freeze1.pgn.yaml` to ensure reproducible output. See [Configuring Generators](../guides/configuring-generators.md) for setup instructions.

---

## Available Generators

### `haskell.gen`

| | |
|---|---|
| **Language** | Haskell |
| **Library** | [hasql](https://hackage.haskell.org/package/hasql) |
| **Repository** | [pgenie-io/haskell.gen](https://github.com/pgenie-io/haskell.gen) |

Generates a Haskell library that exposes each SQL query as a typed [`Statement`](https://hackage.haskell.org/package/hasql/docs/Hasql-Statement.html) value. Output includes a ready-to-use Cabal package, one module per query, and data types for your custom PostgreSQL enumerations and composite types. Nullability is faithfully represented using `Maybe`.

For full documentation — including complete type mappings, generated output examples, configuration options, and the changelog — visit the [haskell.gen repository](https://github.com/pgenie-io/haskell.gen).

```yaml
# project1.pgn.yaml
artifacts:
  haskell: https://raw.githubusercontent.com/pgenie-io/haskell.gen/v0.2.1/gen/Gen.dhall
```

---

## Writing Your Own Generator

Anyone can write and distribute a pGenie generator. Generators are plain Dhall programs - no special permissions or registration required. See [Implementing Custom Generators](../guides/implementing-custom-generators.md) for a guide.
