# Installing pGenie from Source

pGenie is written in Haskell. You can build it with either **Stack** or **Cabal**. Both approaches produce the same `pgn` binary.

---

## Prerequisites

Install the Haskell toolchain via [GHCup](https://www.haskell.org/ghcup/):

```bash
curl --proto '=https' --tlsv1.2 -sSf https://get-ghcup.haskell.org | sh
```

Follow the prompts. GHCup will offer to install GHC, Cabal, and Stack. Install whichever build tool you prefer (or both).

---

## Option 1 — Stack

[Stack](https://docs.haskellstack.org/) manages the compiler and dependencies for you, making it a good choice if you are new to Haskell.

1. Clone the repository:

    ```bash
    git clone https://github.com/pgenie-io/pgenie.git
    cd pgenie
    ```

2. Install the `pgn` executable:

    ```bash
    stack install
    ```

    Stack will download the required GHC version if necessary, compile pGenie, and install the `pgn` binary into `~/.local/bin/`.

3. Ensure `~/.local/bin` is on your `PATH`. Add the following to your shell profile (`.bashrc`, `.zshrc`, etc.):

    ```bash
    export PATH="$HOME/.local/bin:$PATH"
    ```

4. Verify the installation:

    ```bash
    pgn --help
    ```

---

## Option 2 — Cabal

[Cabal](https://www.haskell.org/cabal/) is the standard Haskell build tool and is included with GHCup by default.

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
