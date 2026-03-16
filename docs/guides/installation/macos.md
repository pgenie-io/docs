# Installing pGenie on macOS

There are two ways to install pGenie on macOS: downloading a pre-built binary or building from source.

---

## Option 1 — Pre-built Binary

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

4. Verify the installation:

    ```bash
    pgn --help
    ```

### Gatekeeper warning

On first launch, macOS may show a dialog:

> **"pgn" can't be opened because Apple cannot check it for malicious software.**

**Why this appears:** macOS Gatekeeper requires applications to be notarized by Apple. Pre-built binaries distributed outside the Mac App Store or without Apple notarization trigger this warning. The warning is a security feature of macOS, not evidence that the binary is malicious. You can inspect the source code at [github.com/pgenie-io/pgenie](https://github.com/pgenie-io/pgenie) and build from source if you prefer not to trust the binary distribution.

**To bypass the warning:**

- Right-click (or Control-click) the `pgn` binary in Finder and choose **Open**, then confirm in the dialog that appears. After doing this once, macOS remembers the exception.

  *Or*, run the following in your terminal to remove the quarantine attribute:

  ```bash
  xattr -dr com.apple.quarantine /usr/local/bin/pgn
  ```

If you prefer to verify the binary yourself before running it, build from source (see below).

---

## Option 2 — From Source

Building from source gives you full control and avoids the Gatekeeper warning.

### Stack

[Stack](https://docs.haskellstack.org/) manages the compiler and dependencies entirely on its own, making it the fastest path to building pGenie from source. No separate toolchain installation is required.

#### Install Stack

Run the official one-line installer:

```bash
curl -sSL https://get.haskellstack.org/ | sh
```

For platform-specific instructions and alternative install methods, see the [official Stack installation guide](https://docs.haskellstack.org/en/stable/#how-to-install-stack).

#### Build and install pGenie

1. Clone the repository:

    ```bash
    git clone https://github.com/pgenie-io/pgenie.git
    cd pgenie
    ```

2. Install the `pgn` executable:

    ```bash
    stack install
    ```

    Stack will download the required GHC version automatically if needed, compile pGenie, and install the `pgn` binary into `~/.local/bin/`.

3. Ensure `~/.local/bin` is on your `PATH`. Add the following to your shell profile (`.zshrc`, `.bashrc`, etc.):

    ```bash
    export PATH="$HOME/.local/bin:$PATH"
    ```

4. Verify the installation:

    ```bash
    pgn --help
    ```

### Cabal

[Cabal](https://www.haskell.org/cabal/) is the standard Haskell build tool. It requires a GHC compiler to be installed separately, which you can obtain via [GHCup](https://www.haskell.org/ghcup/).

#### Prerequisites

Install the Haskell toolchain via [GHCup](https://www.haskell.org/ghcup/):

```bash
curl --proto '=https' --tlsv1.2 -sSf https://get-ghcup.haskell.org | sh
```

Follow the prompts. GHCup will install GHC and Cabal.

#### Build and install pGenie

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

3. Ensure `~/.cabal/bin` is on your `PATH`. Add the following to your shell profile (`.zshrc`, `.bashrc`, etc.):

    ```bash
    export PATH="$HOME/.cabal/bin:$PATH"
    ```

4. Verify the installation:

    ```bash
    pgn --help
    ```

---

## Docker Requirement

Docker must be running before invoking `pgn`. With Docker Desktop, the Docker icon should appear in the macOS menu bar. With Colima, ensure you have run `colima start`.
