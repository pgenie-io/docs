# pGenie vs sqlc

pGenie and sqlc both turn SQL into typed application code, but they optimize for different priorities.

## Short Answer

Choose **pGenie** if you're set on PostgreSQL and care about fidelity, schema-drift protection, and automated index guidance.

Choose **sqlc** if you need a broader database matrix, a larger ecosystem, and its existing feature set.

---

## At a Glance

| Question | pGenie | sqlc |
|---|---|---|
| Database scope | PostgreSQL only | PostgreSQL, MySQL, SQLite |
| Language story | Haskell, Rust, Java today; new generators via Dhall | Go is the most mature target; Kotlin, Python and TypeScript are documented; more languages via official and community plugins |
| Query analysis | Always against a live PostgreSQL instance started for the run | Static parsing and analysis by default; optional database-backed checks in `vet`; cross-version schema checks in `verify` |
| Schema drift protection | Committed `.sig1.pgn.yaml` files are checked on every run | `verify` checks schema changes against previously pushed queries via sqlc Cloud |
| Type-contract artifact | Per-query signature files live in your repo and show up in diffs | No equivalent committed per-query signature artifact, nullability control is limited |
| PostgreSQL-specific depth | Optimized for PostgreSQL modeling; supports all possible queries and advanced types like composites and multiranges | Docs cover arrays, enums, UUID, JSON, geometry, but some deeper PostgreSQL features like composites are not supported |
| Performance tooling | `pgn manage-indexes` can suggest and generate index migrations | `vet` can inspect `EXPLAIN` output and enforce custom rules, but sqlc does not manage indexes for you |
| SQL surface | One query per file, plain SQL, signature file beside the query | Query-name annotations plus optional macros such as `sqlc.arg`, `sqlc.embed`, `sqlc.narg`, `sqlc.slice` |
| Ecosystem and resources | Smaller and younger | Larger community, more tutorials, more existing integrations |

## Why pGenie Feels Different

pGenie applies migrations to a fresh PostgreSQL instance and prepares each query against that live server. That makes PostgreSQL the analysis engine, not an approximation of it, letting you express queries of any complexity and get precise type information.

Each query gets a `.sig1.pgn.yaml` file beside it. That file records the inferred contract in a form that can be reviewed and versioned with the query itself. It is also the instrument for tightening constraints such as parameter nullability.

pGenie also treats index analysis as part of the workflow. `pgn manage-indexes` can suggest new indexes and remove stale ones based on the queries already in the project.

## When sqlc May Be a Better Fit

sqlc is a better fit if you need more than PostgreSQL or if you want a tool with a larger community, more documentation, and more language targets.

It is also a good fit if you mostly use simple SQL with extras such as query annotations, macros, `vet`, and `verify`.

## Bottom Line

If you want a tool that extracts the most out of PostgreSQL, validates against the real server, and keeps explicit query contracts in the repo, pGenie is the better fit.

If you want the broader and more established tool with multiple databases and a larger ecosystem, sqlc is the safer default.
