# Installation

This section explains how to install pGenie on your system. Choose the method that best suits your platform:

- **[Linux](linux.md)**
- **[macOS](macos.md)**

!!! note "Windows support is under development"
    It may be possible to run using WSL. Do report about your experience in [the discussions](https://github.com/pgenie-io/pgenie/discussions) and on [the issue tracker](https://github.com/pgenie-io/pgenie/issues).

---

## Prerequisites

### Docker

pGenie requires Docker to be installed and running. During code generation, it starts a temporary PostgreSQL container to analyze your SQL. Without Docker, pGenie cannot function.

- **Linux**: Install the [Docker Engine](https://docs.docker.com/engine/install/) for your distribution.
- **macOS**: Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) or use [Colima](https://github.com/abiosoft/colima), a lightweight Docker host for macOS (`brew install colima docker` then `colima start`).

After installation, verify Docker is running:

```bash
docker info
```

---

## First Run

The very first time you run `pgn generate`, pGenie performs initial setup that can take **up to 3 minutes**:

1. **PostgreSQL Docker image download** — pGenie pulls the PostgreSQL image it needs. This is a one-time download.
2. **Code generator caching** — Dhall generator programs are downloaded from their URLs and their bytecode is cached locally.

You may notice pGenie appears to pause at the "Loading" stage during this first run. This is normal. Subsequent runs complete in a few seconds.

Next, create a `project1.pgn.yaml` file in the root of your project. See the [Initializing Project guide](../initializing-project.md) for a minimal example and a short explanation of the required fields.
