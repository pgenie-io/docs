# Configuring Generators

Generators are configured in your project file (`project1.pgn.yaml`). Each generator is a [Dhall](https://dhall-lang.org/) program referenced by a URL.

---

## Adding a Generator

Open your `project1.pgn.yaml` and add an entry under the `artifacts` key:

```yaml
space: my_space
name: music_catalogue
version: 1.0.0

artifacts:
  hasql: https://raw.githubusercontent.com/pgenie-io/haskell-hasql.gen/v0.1.0/gen/Gen.dhall
```

The key (`hasql` in the example) is the name pGenie uses for the output directory under `artifacts/`. The value is a URL pointing to the generator's entry-point Dhall file.

You can add multiple generators:

```yaml
artifacts:
  hasql: https://raw.githubusercontent.com/pgenie-io/haskell-hasql.gen/v0.1.0/gen/Gen.dhall
  my-custom-gen: https://example.com/my-gen/Gen.dhall
```

Each generator produces a separate subdirectory under `artifacts/`.

---

## Pinning Generator Versions

Always reference a specific **tagged version** of a generator URL (e.g. `/v0.1.0/` in the URL above) rather than a mutable branch like `main`. This ensures your generated code is reproducible. You can also reference a specific commit hash instead of a tag — this is equally reproducible, but a named tag is usually more convenient for users.

After the first run, pGenie records the content hash of each generator in `freeze1.pgn.yaml`:

```yaml
https://raw.githubusercontent.com/pgenie-io/haskell-hasql.gen/v0.1.0/gen/Gen.dhall: sha256:fcc51fe6ae2f774bcb13684b680aae1a9b827451c3f56c1ae2875f1e64fe78e5
```

Commit `freeze1.pgn.yaml` to version control. On subsequent runs, pGenie verifies that every downloaded generator matches its recorded hash, making generation fully reproducible across machines.

---

## Upgrading a Generator

To upgrade to a new version:

1. Update the URL in `project1.pgn.yaml` to point to the new version tag.
2. (Optional) Delete the corresponding line from `freeze1.pgn.yaml` (or delete the whole freeze file).
3. Run `pgn generate`. The new generator will be fetched and a new hash recorded in `freeze1.pgn.yaml`.

---

## Available Generators

See the [Codegens reference](../reference/codegens/index.md) for the list and details on each generator.

---

## Generator Configuration

Generators may accept configuration. The configuration schema is defined by the generator itself. Refer to the individual generator's documentation for details.

The short form (a bare URL) is equivalent to the long form with an empty `config`:

```yaml
# Short form (URL only)
artifacts:
  hasql: https://raw.githubusercontent.com/pgenie-io/haskell-hasql.gen/v0.1.0/gen/Gen.dhall
```

```yaml
# Equivalent long form
artifacts:
  hasql:
    gen: https://raw.githubusercontent.com/pgenie-io/haskell-hasql.gen/v0.1.0/gen/Gen.dhall
    config:
```

Use the long form when you need to supply additional configuration values that the generator accepts.
