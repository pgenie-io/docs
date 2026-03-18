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

Building from source gives you full control.

### Stack

[Stack](https://docs.haskellstack.org/) manages the compiler and dependencies entirely on its own, making it the fastest path to building pGenie from source. No other toolchain installation is required.

1. Install Stack

    Run the official one-line installer:

    ```bash
    curl -sSL https://get.haskellstack.org/ | sh
    ```

    or
    ```bash
    wget -qO- https://get.haskellstack.org/ | sh
    ```

    For platform-specific instructions and alternative install methods, see the [official Stack installation guide](https://docs.haskellstack.org/en/stable/#how-to-install-stack).

2. Clone the repository:

    ```bash
    git clone https://github.com/pgenie-io/pgenie.git
    cd pgenie
    ```

3. Install the `pgn` executable:

    ```bash
    stack install
    ```

    Stack will download the required GHC version automatically if needed, compile pGenie, and install the `pgn` binary into `~/.local/bin/`.

4. Ensure `~/.local/bin` is on your `PATH`. Add the following to your shell profile (`.bashrc`, `.zshrc`, etc.):

    ```bash
    export PATH="$HOME/.local/bin:$PATH"
    ```

5. Verify the installation:

    ```bash
    pgn --help
    ```

### Cabal

[Cabal](https://www.haskell.org/cabal/) is the standard Haskell build tool. It requires a GHC compiler to be installed separately, which you can obtain via [GHCup](https://www.haskell.org/ghcup/).

1. Install the Haskell toolchain via [GHCup](https://www.haskell.org/ghcup/):

    ```bash
    curl --proto '=https' --tlsv1.2 -sSf https://get-ghcup.haskell.org | sh
    ```

    Follow the prompts. GHCup will install GHC and Cabal.

2. Clone the repository:

    ```bash
    git clone https://github.com/pgenie-io/pgenie.git
    cd pgenie
    ```

3. Install the `pgn` executable:

    ```bash
    cabal install
    ```

    Cabal will compile pGenie and install the `pgn` binary into `~/.cabal/bin/`.

4. Ensure `~/.cabal/bin` is on your `PATH`. Add the following to your shell profile (`.bashrc`, `.zshrc`, etc.):

    ```bash
    export PATH="$HOME/.cabal/bin:$PATH"
    ```

5. Verify the installation:

    ```bash
    pgn --help
    ```

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
