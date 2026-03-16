# Installation

This section explains how to install pGenie on your system. Choose the method that best suits your platform:

- **[macOS](macos.md)** — Pre-built binary or from source
- **[Linux](linux.md)** — Pre-built binary or from source
- **[Windows](windows.md)** — Pre-built binary or from source
- **[From Source](from-source.md)** — Build with Stack or Cabal on any platform

---

## Prerequisites

### Docker

pGenie requires Docker to be installed and running. During code generation, it starts a temporary PostgreSQL container to analyze your SQL. Without Docker, pGenie cannot function.

- **macOS**: Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) or use [Colima](https://github.com/abiosoft/colima), a lightweight Docker host for macOS (`brew install colima docker` then `colima start`).
- **Windows**: Install [Docker Desktop](https://www.docker.com/products/docker-desktop/).
- **Linux**: Install the [Docker Engine](https://docs.docker.com/engine/install/) for your distribution.

After installation, verify Docker is running:

```bash
docker info
```

---

## First Run

The very first time you run `pgn generate`, pGenie performs initial setup that can take **2–3 minutes**:

1. **PostgreSQL Docker image download** — pGenie pulls the PostgreSQL image it needs. This is a one-time download.
2. **Code generator caching** — Dhall generator programs are downloaded from their URLs and their bytecode is cached locally.

You may notice pGenie appears to pause at the "Loading" stage during this first run. This is normal. Subsequent runs complete in a few seconds.
