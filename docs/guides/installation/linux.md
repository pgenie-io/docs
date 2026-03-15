# Installing pGenie on Linux

pGenie is installed from source on Linux. See the [From Source](from-source.md) guide for detailed instructions on building with Stack or Cabal.

---

## Docker Requirement

Docker must be running as a daemon before invoking `pgn`:

```bash
systemctl start docker
# or
sudo service docker start
```

Your user should be in the `docker` group to avoid requiring `sudo`:

```bash
sudo usermod -aG docker $USER
newgrp docker
```
