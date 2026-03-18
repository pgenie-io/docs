# Installing pGenie on macOS

There are three ways to install pGenie on macOS: using Homebrew, downloading a pre-built binary manually, or building from source.

---

## Option 1 — Homebrew (Recommended)

The [Homebrew](https://brew.sh/) tap provides two installation modes.

### Install pre-built binary (fastest)

```bash
brew install pgenie-io/tap/pgn
```

This installs a pre-built binary for your Mac architecture (Apple Silicon or Intel) with no additional dependencies.

### Build from source via Homebrew

```bash
brew install --HEAD pgenie-io/tap/pgn
```

This builds from the latest `master` branch and can take several minutes during the first build.

---

## Option 2 — Pre-built Binary (Manual)

Pre-built binaries for macOS (Intel and Apple Silicon) are available on the [pGenie releases page](https://github.com/pgenie-io/pgenie/releases).

1. Download the latest archive for your architecture from the releases page:

    ```bash
    # Apple Silicon (M1/M2/M3)
    curl -fsSL https://github.com/pgenie-io/pgenie/releases/latest/download/pgn-macos-arm64.tar.gz \
      -o pgn-macos-arm64.tar.gz

    # Intel
    curl -fsSL https://github.com/pgenie-io/pgenie/releases/latest/download/pgn-macos-x86_64.tar.gz \
      -o pgn-macos-x86_64.tar.gz
    ```

2. Extract the binary:

    ```bash
    # Apple Silicon
    tar -xzf pgn-macos-arm64.tar.gz

    # Intel
    tar -xzf pgn-macos-x86_64.tar.gz
    ```

3. Move the binary to a directory on your `PATH`:

    ```bash
    # Apple Silicon
    sudo mv pgn-macos-arm64 /usr/local/bin/pgn

    # Intel
    sudo mv pgn-macos-x86_64 /usr/local/bin/pgn
    ```

4. Remove the macOS quarantine attribute from the installed binary:

    ```bash
    xattr -dr com.apple.quarantine /usr/local/bin/pgn
    ```

    This removes the Gatekeeper quarantine metadata so macOS can execute the binary without blocking it on first run.

    Alternative GUI method: in Finder, right-click (or Control-click) `pgn`, choose **Open**, then confirm.

5. Verify the installation:

    ```bash
    pgn --help
    ```

---

## Option 3 — From Source

Building from source gives you full control and avoids the Gatekeeper warning.

### Stack

[Stack](https://docs.haskellstack.org/) manages the compiler and dependencies entirely on its own, making it the fastest path to building pGenie from source. No separate toolchain installation is required.

1. Install Stack

    Run the official one-line installer:

    ```bash
    curl -sSL https://get.haskellstack.org/ | sh
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

4. Ensure `~/.local/bin` is on your `PATH`. Add the following to your shell profile (`.zshrc`, `.bashrc`, etc.):

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

4. Ensure `~/.cabal/bin` is on your `PATH`. Add the following to your shell profile (`.zshrc`, `.bashrc`, etc.):

    ```bash
    export PATH="$HOME/.cabal/bin:$PATH"
    ```

5. Verify the installation:

    ```bash
    pgn --help
    ```

---

## Docker Requirement

Docker must be running before invoking `pgn`. With Docker Desktop, the Docker icon should appear in the macOS menu bar. With Colima, ensure you have run `colima start`.
