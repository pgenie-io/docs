# Installing pGenie on Linux

There are two ways to install pGenie on Linux: downloading a pre-built binary or building from source.

---

## Option 1 — Pre-built Binary

Pre-built binaries for Linux (x86-64) are available on the [pGenie releases page](https://github.com/pgenie-io/pgenie/releases). The binary is distributed as a `.tar.gz` archive.

1. Download the latest archive from the releases page:

    ```bash
    curl -fsSL https://github.com/pgenie-io/pgenie/releases/latest/download/pgn-linux-x86_64.tar.gz \
      -o pgn-linux-x86_64.tar.gz
    ```

2. Extract the binary:

    ```bash
    tar -xzf pgn-linux-x86_64.tar.gz
    ```

3. Move the binary to a directory on your `PATH`:

    ```bash
    sudo mv pgn-linux-x86_64 /usr/local/bin/pgn
    ```

4. Verify the installation:

    ```bash
    pgn --help
    ```

---

## Option 2 — From Source

Building from source gives you full control. See the [From Source](from-source.md) guide for detailed instructions on building with Stack or Cabal.

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
