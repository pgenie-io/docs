# Using pGenie in CI/CD Pipelines

pGenie integrates naturally into CI/CD workflows. This guide shows how to set up pGenie in GitHub Actions for continuous integration (validating schema and queries) and continuous delivery (generating and publishing versioned SDKs).

---

## Continuous Integration

In CI you want to verify that:

1. All migrations are valid PostgreSQL.
2. All queries are valid against the current schema.
3. No signature file has drifted from the current schema (i.e. no uncommitted type changes).
4. (Optionally) no query performs a sequential scan.

Use `pgn analyse` rather than `pgn generate` in CI — it runs the full analysis without invoking any code generators.

### GitHub Actions workflow

```yaml
# .github/workflows/pgenie-ci.yml
name: pGenie CI

on:
  pull_request:
  push:
    branches: [main]

jobs:
  analyse:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Install pGenie
        run: |
          curl -fsSL https://github.com/pgenie-io/pgenie/releases/latest/download/pgn-linux-x64.tar.gz \
            -o pgn-linux-x64.tar.gz
          tar -xzf pgn-linux-x64.tar.gz
          sudo mv pgn /usr/local/bin/pgn

      - name: Analyse schema and queries
        run: pgn analyse
```

`pgn analyse` will:

- Fail if any migration or query contains invalid SQL.
- Fail if any query's signature file (`*.sig1.pgn.yaml`) does not match the schema resolved from the current migrations.
- Print sequential-scan warnings for any query that lacks an appropriate index.

### Using a live PostgreSQL service

If your CI environment already provides PostgreSQL, you can run pGenie in live instance mode instead of Docker execution mode:

```yaml
jobs:
  analyse:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:17
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: postgres
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 5s
          --health-timeout 5s
          --health-retries 10

    steps:
      - uses: actions/checkout@v4

      - name: Install pGenie
        run: |
          curl -fsSL https://github.com/pgenie-io/pgenie/releases/latest/download/pgn-linux-x64.tar.gz \
            -o pgn-linux-x64.tar.gz
          tar -xzf pgn-linux-x64.tar.gz
          sudo mv pgn /usr/local/bin/pgn

      - name: Analyse schema and queries
        run: pgn --database-url "host=localhost port=5432 user=postgres password=postgres dbname=postgres" analyse
```

In this setup, set `postgres` in `project1.pgn.yaml` to `17` so it matches the PostgreSQL service version.

### Fail on sequential scans

If you want to enforce that no query performs a sequential scan, add the `--fail-on-seq-scans` flag:

```yaml
      - name: Analyse schema and queries (strict)
        run: pgn analyse --fail-on-seq-scans
```

With this flag the CI job fails if any query triggers a sequential scan, ensuring that index coverage is maintained as the schema evolves.

---

## Continuous Delivery

In CD you want to:

1. Generate typed client libraries from the current schema and queries.
2. Package the generated artifacts as a versioned release.
3. Publish them for consuming applications to download.

### Generating artifacts

```yaml
# .github/workflows/pgenie-cd.yml
name: pGenie CD

on:
  push:
    tags:
      - 'v*'   # trigger on version tags, e.g. v1.2.0

jobs:
  generate:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Install pGenie
        run: |
          curl -fsSL https://github.com/pgenie-io/pgenie/releases/latest/download/pgn-linux-x64.tar.gz \
            -o pgn-linux-x64.tar.gz
          tar -xzf pgn-linux-x64.tar.gz
          sudo mv pgn /usr/local/bin/pgn

      - name: Generate code
        run: pgn generate

      - name: Upload generated artifacts
        uses: actions/upload-artifact@v4
        with:
          name: sdk-${{ github.ref_name }}
          path: artifacts/
```

### Publishing as a GitHub Release

To attach the generated artifacts to a GitHub Release:

```yaml
      - name: Package artifacts
        run: |
          cd artifacts
          zip -r ../sdk-${{ github.ref_name }}.zip .

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          files: sdk-${{ github.ref_name }}.zip
```

Consuming applications can then download the SDK from the release page or via the GitHub API and include it as a dependency.

---

## Tips

- **Always commit `freeze1.pgn.yaml`** — this ensures that every CI/CD run uses the exact same generator version and produces identical output.
- **Always commit `*.sig1.pgn.yaml` files** — both query signature files and custom-type signature files are part of the reviewed contract that CI validates.
- **Use `pgn analyse` in PR checks and `pgn generate` in release pipelines** — analysis is fast and does not require generator access, making it ideal for pull request feedback.
- **Live instance mode is especially useful on Windows runners** — Docker execution mode is not supported there yet.
