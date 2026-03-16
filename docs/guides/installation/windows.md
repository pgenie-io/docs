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

Building from source gives you full control.

### Stack

[Stack](https://docs.haskellstack.org/) manages the compiler and dependencies entirely on its own, making it the fastest path to building pGenie from source. No separate toolchain installation is required.

#### Install Stack

Download and run the Stack installer for Windows from the [official Stack installation guide](https://docs.haskellstack.org/en/stable/#how-to-install-stack), or use [Scoop](https://scoop.sh/):

```powershell
scoop install stack
```

#### Build and install pGenie

1. Clone the repository:

    ```powershell
    git clone https://github.com/pgenie-io/pgenie.git
    cd pgenie
    ```

2. Install the `pgn` executable:

    ```powershell
    stack install
    ```

    Stack will download the required GHC version automatically if needed, compile pGenie, and install the `pgn` binary into `%APPDATA%\stack\bin`.

3. Ensure `%APPDATA%\stack\bin` is on your `PATH`. Add it via the System Properties dialog or your PowerShell profile:

    ```powershell
    [System.Environment]::SetEnvironmentVariable(
      "Path",
      "$([System.Environment]::GetEnvironmentVariable('Path','User'));$env:APPDATA\stack\bin",
      "User"
    )
    ```

4. Verify the installation (open a new terminal after updating `PATH`):

    ```powershell
    pgn --help
    ```

### Cabal

[Cabal](https://www.haskell.org/cabal/) is the standard Haskell build tool. It requires a GHC compiler to be installed separately, which you can obtain via [GHCup](https://www.haskell.org/ghcup/).

#### Prerequisites

Download and run the GHCup installer for Windows from [get-ghcup.haskell.org](https://www.haskell.org/ghcup/). The installer will set up GHC and Cabal.

#### Build and install pGenie

1. Clone the repository:

    ```powershell
    git clone https://github.com/pgenie-io/pgenie.git
    cd pgenie
    ```

2. Install the `pgn` executable:

    ```powershell
    cabal install
    ```

    Cabal will compile pGenie and install the `pgn` binary into `%APPDATA%\cabal\bin`.

3. Ensure `%APPDATA%\cabal\bin` is on your `PATH`. Add it via the System Properties dialog or your PowerShell profile:

    ```powershell
    [System.Environment]::SetEnvironmentVariable(
      "Path",
      "$([System.Environment]::GetEnvironmentVariable('Path','User'));$env:APPDATA\cabal\bin",
      "User"
    )
    ```

4. Verify the installation (open a new terminal after updating `PATH`):

    ```powershell
    pgn --help
    ```

---

## Docker Requirement

Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) and ensure the Docker daemon is running before invoking `pgn`.
