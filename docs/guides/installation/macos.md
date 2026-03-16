# Installing pGenie on macOS

There are two ways to install pGenie on macOS: downloading a pre-built binary or building from source.

---

## Option 1 — Pre-built Binary

Pre-built binaries for macOS (Intel and Apple Silicon) are available on the [pGenie releases page](https://github.com/pgenie-io/pgenie/releases).

1. Download the latest binary for your architecture from the releases page and unpack it.

2. Move the binary to a directory on your `PATH`:

    ```bash
    sudo mv pgn /usr/local/bin/pgn
    ```

3. Verify the installation:

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

If you prefer to verify the binary yourself before running it, see the [From Source](from-source.md) guide below.

---

## Option 2 — From Source

Building from source gives you full control and avoids the Gatekeeper warning. See the [From Source](from-source.md) guide for detailed instructions.

---

## Docker Requirement

Docker must be running before invoking `pgn`. With Docker Desktop, the Docker icon should appear in the macOS menu bar. With Colima, ensure you have run `colima start`.
