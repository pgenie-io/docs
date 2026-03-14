# Installation

This guide explains how to install pGenie on your system.

---

## Prerequisites

### Docker

pGenie requires Docker to be installed and running. During code generation, it starts a temporary PostgreSQL container to analyze your SQL. Without Docker, pGenie cannot function.

- **macOS / Windows**: Install [Docker Desktop](https://www.docker.com/products/docker-desktop/).
- **Linux**: Install the [Docker Engine](https://docs.docker.com/engine/install/) for your distribution.

After installation, verify Docker is running:

```bash
docker info
```

---

## Installing from Source

pGenie is written in Haskell and built with [Cabal](https://www.haskell.org/cabal/).

### Prerequisites

- **GHC** and **Cabal** — Install the Haskell toolchain via [GHCup](https://www.haskell.org/ghcup/):

    ```bash
    curl --proto '=https' --tlsv1.2 -sSf https://get-ghcup.haskell.org | sh
    ```

    Follow the prompts to install GHC and Cabal.

### Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/pgenie-io/pgenie.git
    cd pgenie
    ```

2. Install the `pgn` executable:

    ```bash
    cabal install
    ```

    Cabal will compile pGenie and install the `pgn` binary into `~/.cabal/bin/`.

3. Ensure `~/.cabal/bin` is on your `PATH`. Add the following to your shell profile (`.bashrc`, `.zshrc`, etc.):

    ```bash
    export PATH="$HOME/.cabal/bin:$PATH"
    ```

4. Verify the installation:

    ```bash
    pgn --help
    ```

---

## Platform Notes

### Windows

- Ensure Docker Desktop is installed and the Docker daemon is running before invoking `pgn`.
- The `~/.cabal/bin` directory is typically `%APPDATA%\cabal\bin`; add it to your `PATH` via the System Properties dialog or your PowerShell profile.

### macOS

- Docker Desktop for macOS must be running (the Docker icon should appear in the menu bar).
- GHCup works on both Intel and Apple Silicon Macs.

### Linux

- Docker must be running as a daemon (`systemctl start docker` or `sudo service docker start`).
- Your user should be in the `docker` group to avoid requiring `sudo`:

    ```bash
    sudo usermod -aG docker $USER
    newgrp docker
    ```

---

## First Run

The very first time you run `pgn generate`, pGenie performs initial setup that can take **2–3 minutes**:

1. **PostgreSQL Docker image download** — pGenie pulls the PostgreSQL image it needs. This is a one-time download.
2. **Code generator caching** — Dhall generator programs are downloaded from their URLs and their bytecode is cached locally.

You may notice pGenie appears to pause at the "Loading" stage during this first run. This is normal. Subsequent runs complete in a few seconds.
