---
title: sqlc Alternative for Java, Haskell & Rust — pGenie vs sqlc
description: Comparing pGenie and sqlc for type-safe PostgreSQL codegen. pGenie targets Java, Haskell, and Rust instead of Go, validates queries against a live PostgreSQL instance, and tracks schema drift with committed signature files.
---

# pGenie vs sqlc

pGenie is a **sqlc alternative** for teams working in Java, Haskell, or Rust rather than Go. Both tools turn SQL into typed application code, but they optimize for different priorities. If you landed here because sqlc doesn't support a PostgreSQL type you need, its static analysis got a nullability check wrong, or you'd rather not depend on sqlc Cloud for schema-drift checks, the FAQ below covers those specifics directly.

## Short Answer

Choose **pGenie** if you're set on PostgreSQL and care about fidelity, schema-drift protection, and automated index guidance.

Choose **sqlc** if you need a broader database matrix, a larger ecosystem, and its existing feature set.

---

## At a Glance

| Question | pGenie | sqlc |
|---|---|---|
| Database scope | PostgreSQL only | PostgreSQL, MySQL, SQLite |
| Language story | Java, Haskell, Rust today — no Go target; new generators via Dhall | Go is the most mature target; Kotlin, Python and TypeScript are documented; more languages via official and community plugins |
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

## FAQ

**Can I use pGenie as a sqlc alternative for Java?**
Yes — pGenie's Java generator produces typed client code (via pgJDBC) from plain SQL, validated against a live PostgreSQL instance rather than static parsing.

**Can I use pGenie as a sqlc alternative for Rust?**
Yes — pGenie's Rust generator produces typed client code on top of tokio-postgres.

**Does pGenie support Go?**
Not as an official generator today. pGenie ships official generators for Java, Haskell, and Rust; anyone can write a new one, including a Go target, as a Dhall program.

**Why choose pGenie over sqlc if you're not using Go?**
sqlc is database-agnostic by design, which limits it to a subset of PostgreSQL's features. pGenie is PostgreSQL-only, so it can support the full depth of PostgreSQL's type system and advanced features (like composites and multiranges), with Java, Haskell, and Rust as equally first-class generator targets.

**Does sqlc support PostgreSQL composite types?**
No — composite types remain an [open, unresolved feature request](https://github.com/sqlc-dev/sqlc/issues/2760) in sqlc. pGenie validates every query against a live PostgreSQL instance, so composites are supported the same way any other type is — there's no separate "supported types" list to check against.

**Why are `sqlc.embed()` fields wrong or non-nullable after a `LEFT JOIN`?**
This is one of the highest-reaction [open bug clusters](https://github.com/sqlc-dev/sqlc/issues/2997) in sqlc: `sqlc.embed()` doesn't reliably infer nullability for the outer side of a `LEFT JOIN`, which can surface as a runtime scan failure or silently wrong generated types. pGenie has no embed macro to reach for — nullability for every column, including `LEFT JOIN` results, is inferred by running the query against a real PostgreSQL instance.

**Does sqlc support dynamic query building?**
Not natively — [it's one of the most requested and longest-open feature gaps](https://github.com/sqlc-dev/sqlc/issues/3414) in the project. Neither tool solves this the way a query builder does: both sqlc and pGenie are built around static, pre-written SQL. If your query structure is assembled at runtime, look at a query builder such as jOOQ instead of either one.

**Is `sqlc verify` free to run locally?**
No — [`sqlc verify` works by uploading your schema and queries to sqlc Cloud](https://docs.sqlc.dev/en/latest/howto/verify.html), a hosted service that requires an account and auth token. pGenie's equivalent — committed `.sig1.pgn.yaml` signature files, checked on every local run — needs no external service or account.

**Does sqlc's type-override system work the same for Java as it does for Go?**
No — sqlc's own docs describe its [`db_type`/`column` override mechanism](https://docs.sqlc.dev/en/latest/howto/overrides.html), the escape hatch for types sqlc doesn't natively understand, as only fully supported for Go. pGenie has no such asymmetry: Java, Haskell, and Rust are equally first-class generator targets, and because types come from a live PostgreSQL instance rather than static overrides, there's no override table to keep in sync per language.

## Bottom Line

If you're building on PostgreSQL and want a tool that extracts the most out of it — validating every query against the real server, catching schema drift at build time, and keeping explicit query contracts in the repo — pGenie is the obvious choice.

If your project spans multiple database engines, or you're already invested in sqlc's larger ecosystem, sqlc remains the safer default there.
