# Code Generators

Code generators are the plugins that turn pGenie's analysis output into idiomatic client libraries for specific programming languages and libraries.

---

## How Generators Work

Each generator is a [Dhall](https://dhall-lang.org/) program hosted at a URL. pGenie downloads the generator, evaluates it with the project model (schema + queries + configuration), and writes the resulting files to `artifacts/<NAME>/`.

Generators are versioned and pinned via `freeze1.pgn.yaml` to ensure reproducible output. See [Configuring Generators](../guides/configuring-generators.md) for setup instructions.

---

## Available Generators

| Language | Library | Generator Repo & Docs | Generator URL |
|---|---|---|---|
| Haskell | [hasql](https://hackage.haskell.org/package/hasql) | [haskell.gen](https://github.com/pgenie-io/haskell.gen) | `https://github.com/pgenie-io/haskell.gen/releases/download/v1.0.0/resolved.dhall` |
| Java | [pgJDBC](https://jdbc.postgresql.org/) | [java.gen](https://github.com/pgenie-io/java.gen) | `https://github.com/pgenie-io/java.gen/releases/download/v1.1.0/resolved.dhall` |
| Rust | [tokio-postgres](https://crates.io/crates/tokio-postgres) | [rust.gen](https://github.com/pgenie-io/rust.gen) | `https://github.com/pgenie-io/rust.gen/releases/download/v1.0.0/resolved.dhall` |

Use them by specifying the latest generator URL either in the short form:

```yaml
# project1.pgn.yaml
artifacts:
  <NAME>: <GENERATOR_URL>
```

Or the long form:

```yaml
# project1.pgn.yaml
artifacts:
  <NAME>:
    gen: <GENERATOR_URL>
    config: <GENERATOR_CONFIG>
```

For detailed documentation on each generator, refer to the links in the "Generator Repo" column from the table above.

## Writing Your Own Generator

Anyone can write and distribute a pGenie generator. Generators are plain Dhall programs - no special permissions or registration required. See [Implementing Custom Generators](../guides/implementing-custom-generators.md) for a guide.
