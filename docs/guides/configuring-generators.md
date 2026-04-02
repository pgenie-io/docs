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
  haskell: https://raw.githubusercontent.com/pgenie-io/haskell.gen/v0.2.1/gen/Gen.dhall
```

The key (`haskell` in the example) is the name pGenie uses for the output directory under `artifacts/`. The value is a URL pointing to the generator's entry-point Dhall file.

You can add multiple generators:

```yaml
artifacts:
  haskell: https://raw.githubusercontent.com/pgenie-io/haskell.gen/v0.2.1/gen/Gen.dhall
  java: https://raw.githubusercontent.com/pgenie-io/java.gen/v0.1.1/gen/Gen.dhall
  rust: https://raw.githubusercontent.com/pgenie-io/rust.gen/v0.1.0/gen/Gen.dhall
```

Each generator produces a separate subdirectory under `artifacts/`.

---

## Pinning Generator Versions

Always reference a specific **tagged version** of a generator URL (e.g. `/v0.1.0/` in the URL above) rather than a mutable branch like `main`. This ensures your generated code is reproducible. You can also reference a specific commit hash instead of a tag — this is equally reproducible, but a named tag is usually more convenient for users.

After the first run, pGenie records the content hash of each generator in `freeze1.pgn.yaml`:

```yaml
# Map of generator hashes by url
https://raw.githubusercontent.com/pgenie-io/haskell.gen/v0.2.1/gen/Gen.dhall: sha256:5bed6d6b5a047e1f908c6432fca54a0e9c66c188257756b1b8a8fcbd7b1eace3
https://raw.githubusercontent.com/pgenie-io/java.gen/v0.1.1/gen/Gen.dhall: sha256:97a8309ac0536d17f41ae5cb39a4e365aa4a04845074ff6635e292fe6c1ca8ee
https://raw.githubusercontent.com/pgenie-io/rust.gen/v0.1.0/gen/Gen.dhall: sha256:38d40d5d55a60f0fb6a131a30cb7c4fb417e50710c6344df401b2e424b586a66
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

See the [Codegens reference](../reference/codegens.md) for the list and details on each generator.

---

## Generator Configuration

Generators may accept configuration. The configuration schema is defined by the generator itself. Refer to the individual generator's documentation for details.

The short form (a bare URL) is equivalent to the long form with an empty `config`:

```yaml
# Short form (URL only)
artifacts:
  haskell: https://raw.githubusercontent.com/pgenie-io/haskell.gen/v0.2.1/gen/Gen.dhall
```

```yaml
# Equivalent long form
artifacts:
  haskell:
    gen: https://raw.githubusercontent.com/pgenie-io/haskell.gen/v0.2.1/gen/Gen.dhall
    config:
```

Use the long form when you need to supply additional configuration values that the generator accepts.
