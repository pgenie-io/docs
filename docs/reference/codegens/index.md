# Code Generators

Code generators are the plugins that turn pGenie's analysis output into idiomatic client libraries for specific programming languages and libraries.

---

## How Generators Work

Each generator is a [Dhall](https://dhall-lang.org/) program hosted at a URL. pGenie downloads the generator, evaluates it with the project model (schema + queries + configuration), and writes the resulting files to `artifacts/<name>/`.

Generators are versioned and pinned via `freeze1.pgn.yaml` to ensure reproducible output. See [Configuring Generators](../../guides/configuring-generators.md) for setup instructions.

---

## Available Generators

| Generator | Language | Library | Repository |
|---|---|---|---|
| `haskell-hasql.gen` | Haskell | [hasql](https://hackage.haskell.org/package/hasql) | [pgenie-io/haskell-hasql.gen](https://github.com/pgenie-io/haskell-hasql.gen) |

---

## Generator Documentation

Each generator is distributed independently and carries its own documentation. Visit the generator's repository for:

- Full usage instructions
- Supported PostgreSQL types and their language-specific mappings
- Configuration options
- Generated output examples

See the per-generator pages in this section for a brief overview of each generator available in the pGenie ecosystem.

---

## Writing Your Own Generator

Anyone can write and distribute a pGenie generator. Generators are plain Dhall programs - no special permissions or registration required. See [Implementing Custom Generators](../../guides/implementing-custom-generators.md) for a guide.
