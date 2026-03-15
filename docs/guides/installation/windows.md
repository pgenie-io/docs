# Installing pGenie on Windows

pGenie is installed from source on Windows. See the [From Source](from-source.md) guide for detailed instructions on building with Stack or Cabal.

---

## Docker Requirement

Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) and ensure the Docker daemon is running before invoking `pgn`.

The `~/.cabal/bin` directory is typically `%APPDATA%\cabal\bin` (or `%APPDATA%\stack\bin` for Stack); add it to your `PATH` via the System Properties dialog or your PowerShell profile.
