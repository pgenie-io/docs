# Installation

This section explains how to install pGenie on your system and how to choose the right execution mode for it.

- **[Linux](linux.md)**
- **[macOS](macos.md)**
- **[Windows](windows.md)**

!!! note "Windows currently uses live instance mode"
    On Windows, pGenie's Docker execution mode is not supported yet. Use [live instance mode](../live-instance-mode.md) with `--database-url` instead.

---

## Prerequisites

### PostgreSQL Access

pGenie always analyses your project against a real PostgreSQL server. You can provide that server in one of two ways:

- **Docker execution mode** (default): pGenie starts a temporary PostgreSQL container for the run.
- **Live instance mode**: you pass `--database-url` and pGenie connects to an already running PostgreSQL server instead.

See [Using a Live PostgreSQL Instance](../live-instance-mode.md) for the full live-mode workflow.

### Docker (Optional)

Docker is required only for the default Docker execution mode.

- **Linux**: Install the [Docker Engine](https://docs.docker.com/engine/install/) for your distribution.
- **macOS**: Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) or use [Colima](https://github.com/abiosoft/colima), a lightweight Docker host for macOS (`brew install colima docker` then `colima start`).
- **Windows**: Docker execution mode is not supported yet. Use live instance mode instead.

If you plan to use Docker execution mode, verify Docker is running:

```bash
docker info
```

---

## First Run

The very first time you run `pgn generate`, pGenie may perform setup that can take **up to 3 minutes**:

1. **PostgreSQL Docker image download** — only in Docker execution mode, pGenie pulls the PostgreSQL image it needs.
2. **Code generator caching** — Dhall generator programs are downloaded from their URLs and their bytecode is cached locally.

You may notice pGenie appears to pause at the "Loading" stage during this first run. This is normal. Subsequent runs complete in a few seconds.

Next, create a `project1.pgn.yaml` file in the root of your project. See the [Initializing Project guide](../initializing-project.md) for a minimal example and a short explanation of the required fields.

If you plan to use live instance mode, set the `postgres` field in `project1.pgn.yaml` to the **major version of the live PostgreSQL server** you connect to.
