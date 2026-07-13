# Reusing a Docker Container Across Runs

By default, each Docker execution mode run starts a fresh PostgreSQL container and throws it away afterwards, which means paying the container's startup cost every time. Pass `--reuse-container` to keep the container running between invocations instead:

```bash
pgn --reuse-container analyse
pgn --reuse-container generate
```

The first `--reuse-container` run starts a container as usual. Subsequent `--reuse-container` runs (with the same project's PostgreSQL image tag) find and reuse that same still-running container rather than starting a new one, cutting cold-start time out of the loop. Each run still gets its own throwaway database inside the container, so runs don't interfere with each other's schema objects.

This flag is only meaningful in Docker execution mode; it has no effect together with `--database-url`.

## Manual Cleanup

Reused containers are **never automatically cleaned up** — this mirrors Testcontainers-Java's own reuse feature, which is explicitly not intended for CI. Find and remove them manually when you're done:

```bash
docker ps --filter label=org.testcontainers.hs.reuse=true
docker rm -f <container-id>
```
