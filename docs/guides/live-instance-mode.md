# Using a Live PostgreSQL Instance

By default, pGenie runs in **Docker execution mode**: it starts a temporary PostgreSQL container, applies your migrations there, and analyses your queries against that disposable instance.

When you pass `--database-url`, pGenie switches to **live instance mode** instead. In this mode it connects to an already running PostgreSQL server, creates a temporary database on that server for the analysis run, and drops it afterwards.

---

## When to Use This Mode

Live instance mode is useful when:

- Docker is unavailable or undesirable on the machine running `pgn`.
- You already have a PostgreSQL server running locally or in CI.
- You are working on Windows, where Docker execution mode is **not supported yet**. On Windows, use live instance mode.

---

## Commands

Pass `--database-url` before the subcommand:

```bash
pgn --database-url "postgresql://user:password@localhost:5432/postgres" analyse
pgn --database-url "postgresql://user:password@localhost:5432/postgres" generate
pgn --database-url "host=localhost port=5432 user=postgres password=postgres dbname=postgres" manage-indexes
```

Both URI form (`postgresql://...`) and libpq keyword/value form (`host=... port=...`) are accepted.

---

## Requirements

### `postgres` Must Match the Live Server

The `postgres` field in `project1.pgn.yaml` must match the **major PostgreSQL version** of the live instance you connect to.

For example, if your live server is PostgreSQL 17:

```yaml
postgres: 17
```

If the versions do not match, pGenie fails the run instead of analysing against the wrong server version.

### The User Must Be Able to Create Databases

pGenie creates a temporary database on the live server for each run and deletes it afterwards. The connected user therefore needs the PostgreSQL `CREATEDB` privilege, or superuser access.

---

## Security Note

Be careful when passing credentials directly on the command line: they can appear in shell history and process listings.

For shared or production-like environments, prefer PostgreSQL connection management features such as:
 
- Connection service files (`~/.pg_service.conf`) — see the PostgreSQL docs: [Connection service files](https://www.postgresql.org/docs/current/libpq-pgservice.html)
- Client password file (`.pgpass`) / `PGPASSFILE` — see the PostgreSQL docs: [Client password file](https://www.postgresql.org/docs/current/libpq-pgpass.html)
- `PGPASSWORD` (environment variable) — see the PostgreSQL docs: [libpq environment variables](https://www.postgresql.org/docs/current/libpq-envars.html)

That lets you keep the connection string passed to `--database-url` free of embedded secrets.
