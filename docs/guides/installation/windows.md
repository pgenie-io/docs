# Installing pGenie on Windows

Windows support is available through **live instance mode**. On this platform, pGenie's Docker execution mode is **not supported yet**.

Use a running PostgreSQL server together with `--database-url`. See [Using a Live PostgreSQL Instance](../live-instance-mode.md) for the execution model.

---

## Install the Pre-built Binary

Pre-built Windows binaries are available on the [pGenie releases page](https://github.com/pgenie-io/pgenie/releases).

1. Download the latest archive:

    ```powershell
    curl.exe -L https://github.com/pgenie-io/pgenie/releases/latest/download/pgn-windows-x64.tar.gz -o pgn-windows-x64.tar.gz
    ```

2. Extract it:

    ```powershell
    tar -xzf .\pgn-windows-x64.tar.gz
    ```

3. Move `pgn.exe` into a directory on your `PATH`, for example:

    ```powershell
    New-Item -ItemType Directory -Force "$HOME\bin" | Out-Null
    Move-Item .\pgn.exe "$HOME\bin\pgn.exe"
    ```

4. Ensure that directory is on your `PATH`.

5. Verify the installation:

    ```powershell
    pgn.exe --help
    ```

---

## PostgreSQL Requirement

Because Docker execution mode is not supported on Windows yet, you should run pGenie against a **live PostgreSQL instance**.

That PostgreSQL server can be:

- installed directly on Windows
- provided by your development environment
- provided by CI

Invoke pGenie with `--database-url`:

```powershell
pgn.exe --database-url "postgresql://postgres:postgres@localhost:5432/postgres" analyse
pgn.exe --database-url "postgresql://postgres:postgres@localhost:5432/postgres" generate
pgn.exe --database-url "host=localhost port=5432 user=postgres password=postgres dbname=postgres" manage-indexes
```

---

## Match the Project PostgreSQL Version

When you use live instance mode, the `postgres` field in `project1.pgn.yaml` must match the **major version** of the PostgreSQL server you connect to.

For example, if your local PostgreSQL instance is version 17:

```yaml
postgres: 17
```

The project's own `version` field is unrelated. It versions generated artifacts, while `postgres` selects the PostgreSQL major version used for analysis.

---

## Current Limitation

Docker execution mode is **not supported yet on Windows**. Even if Docker is installed, use live instance mode for now.