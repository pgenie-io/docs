# Initializing Project

pGenie reads its project settings from `project1.pgn.yaml` in the root of your project. Create this file first, before adding migrations or queries.

---

## Minimal Example

```yaml
space: my_space
name: music_catalogue
version: 1.0.0
postgres: 18
```

This is enough to initialize a project. `space`, `name`, and `version` identify the project. `postgres` is optional; if you omit it, pGenie defaults to PostgreSQL 18.

If you use live instance mode (`--database-url`), set `postgres` to the **major version of the PostgreSQL server** you connect to. For example, use `postgres: 17` with a PostgreSQL 17 server. The project `version` field is unrelated.

You can leave out `artifacts` entirely until you are ready to generate code. When you do want generators, see the [Project File reference](../reference/project-file.md) and the [Configuring Generators](configuring-generators.md) guide.