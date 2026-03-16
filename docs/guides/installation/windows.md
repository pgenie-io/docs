# Installing pGenie on Windows

There are two ways to install pGenie on Windows: downloading a pre-built binary or building from source.

---

## Option 1 — Pre-built Binary

A pre-built binary for Windows (x86-64) is available on the [pGenie releases page](https://github.com/pgenie-io/pgenie/releases). The binary is a standalone `.exe` file.

1. Download the latest binary from the releases page:

    ```powershell
    Invoke-WebRequest -Uri "https://github.com/pgenie-io/pgenie/releases/latest/download/pgn-windows-x86_64.exe" `
      -OutFile pgn.exe
    ```

2. Move `pgn.exe` to a directory on your `PATH`. A common choice is `C:\tools\` or any directory you have already added to your user `PATH`. You can also add its current location to your `PATH` via the System Properties dialog or your PowerShell profile:

    ```powershell
    # Add the current directory to PATH permanently (current user)
    [System.Environment]::SetEnvironmentVariable(
      "Path",
      "$([System.Environment]::GetEnvironmentVariable('Path','User'));$PWD",
      "User"
    )
    ```

3. Verify the installation (open a new terminal after updating `PATH`):

    ```powershell
    pgn --help
    ```

---

## Option 2 — From Source

Building from source gives you full control. See the [From Source](from-source.md) guide for detailed instructions on building with Stack or Cabal.

The `~/.cabal/bin` directory is typically `%APPDATA%\cabal\bin` (or `%APPDATA%\stack\bin` for Stack); add it to your `PATH` via the System Properties dialog or your PowerShell profile.

---

## Docker Requirement

Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) and ensure the Docker daemon is running before invoking `pgn`.
