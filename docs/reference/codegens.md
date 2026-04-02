# Code Generators

Code generators are the plugins that turn pGenie's analysis output into idiomatic client libraries for specific programming languages and libraries.

---

## How Generators Work

Each generator is a [Dhall](https://dhall-lang.org/) program hosted at a URL. pGenie downloads the generator, evaluates it with the project model (schema + queries + configuration), and writes the resulting files to `artifacts/<name>/`.

Generators are versioned and pinned via `freeze1.pgn.yaml` to ensure reproducible output. See [Configuring Generators](../guides/configuring-generators.md) for setup instructions.

---

## Available Generators

### haskell

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

### rust

| | |
|---|---|
| **Language** | Rust |
| **Library** | [tokio-postgres](https://crates.io/crates/tokio-postgres) |
| **Repository** | [pgenie-io/rust.gen](https://github.com/pgenie-io/rust.gen) |

Generates a Rust crate that exposes each SQL query as a typed statement implementation. Output includes a ready-to-build Cargo package, one module per query, and Rust data types for your custom PostgreSQL enumerations and composite types.

For full documentation — including complete type mappings, generated output examples, configuration options, and the changelog — visit the [rust.gen repository](https://github.com/pgenie-io/rust.gen).

```yaml
# project1.pgn.yaml
artifacts:
  rust: https://raw.githubusercontent.com/pgenie-io/rust.gen/v0.1.0/gen/Gen.dhall
```

---

### java

| | |
|---|---|
| **Language** | Java |
| **Library** | [pgJDBC](https://jdbc.postgresql.org/) |
| **Repository** | [pgenie-io/java.gen](https://github.com/pgenie-io/java.gen) |

Generates a Java library that exposes each SQL query as a typed statement implementation. Output includes a ready-to-build Maven project, one class per query, and Java data types for your custom PostgreSQL enumerations and composite types.

For full documentation — including complete type mappings, generated output examples, configuration options, and the changelog — visit the [java.gen repository](https://github.com/pgenie-io/java.gen).

```yaml
# project1.pgn.yaml
artifacts:
  java: https://raw.githubusercontent.com/pgenie-io/java.gen/v0.1.1/gen/Gen.dhall
```

---

## Writing Your Own Generator

Anyone can write and distribute a pGenie generator. Generators are plain Dhall programs - no special permissions or registration required. See [Implementing Custom Generators](../guides/implementing-custom-generators.md) for a guide.
