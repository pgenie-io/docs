# pGenie vs sqlc

Both pGenie and sqlc start from SQL and generate typed application code. They are similar enough that this comparison comes up often, but they optimize for different priorities.

---

## Short Answer

Choose **pGenie** if you are all-in on PostgreSQL and you care most about PostgreSQL fidelity, local schema-drift protection via committed query contracts, and automated index guidance.

Choose **sqlc** if you need a broader database matrix, a larger ecosystem, and its existing feature set around annotations, macros, linting, and plugins.

---

## At a Glance

| Question | pGenie | sqlc |
|---|---|---|
| Database scope | PostgreSQL only | PostgreSQL, MySQL, SQLite |
| Language story | Haskell, Rust, Java today; new generators via Dhall | Go is the most mature target; Kotlin, Python and TypeScript are documented; more languages via official and community plugins |
| Query analysis | Always against a live PostgreSQL instance started for the run | Static parsing and analysis by default; optional database-backed checks in `vet`; cross-version schema checks in `verify` |
| Schema drift protection | Committed `.sig1.pgn.yaml` files are checked on every run | `verify` checks schema changes against previously pushed queries via sqlc Cloud |
| Type-contract artifact | Per-query signature files live in your repo and show up in diffs | No equivalent committed per-query signature artifact |
| PostgreSQL-specific depth | Optimized for PostgreSQL-only modeling; docs explicitly cover composite types and multiranges | Docs clearly cover arrays, enums, UUID, JSON, geometry, overrides and plugins, but some deeper PostgreSQL features are still open problem areas in the issue tracker |
| Performance tooling | `pgn manage-indexes` can suggest and generate index migrations | `vet` can inspect `EXPLAIN` output and enforce custom rules, but sqlc does not manage indexes for you |
| SQL surface | One query per file, plain SQL, signature file beside the query | Query-name annotations plus optional macros such as `sqlc.arg`, `sqlc.embed`, `sqlc.narg`, `sqlc.slice` |
| Dynamic query ergonomics | Intentionally optimized for static SQL | A few escape hatches exist, but it still works best when the query shape is mostly static |
| Ecosystem and resources | Smaller and younger | Larger community, more tutorials, more existing integrations |

---

## What sqlc Clearly Does Well

The sqlc docs describe a tool that is broader than simple code generation:

- It supports multiple engines and multiple language targets.
- It has first-class query annotations for result cardinality and execution mode.
- It supports overrides, struct embedding, prepared queries, transactions, batch operations and `COPY`-style workflows in the documented language backends.
- It has a real linting story in `vet`, including custom CEL rules and optional `EXPLAIN`-driven checks.
- It has a schema-change verification story in `verify`.

That matters because the comparison is not between pGenie and a toy. sqlc is a capable and mature project.

---

## Where pGenie Is Materially Different

### 1. Query analysis goes through PostgreSQL itself

pGenie applies your migrations to a fresh PostgreSQL instance and prepares every query against that live server. The server is the interpreter.

sqlc also has database-backed checks, but they are optional and live mainly in `vet` and `verify`. Its default workflow still relies on sqlc's own parsing and analysis pipeline.

The practical difference is simple: pGenie is designed so that if PostgreSQL accepts the query and exposes its types, pGenie can derive its contract from PostgreSQL directly.

### 2. Signature files are local, committed query contracts

pGenie writes a `.sig1.pgn.yaml` file next to each query and checks it on every run. That gives you:

- A reviewable type contract for every query.
- Explicit diffs when a migration changes a query's types.
- A place to tighten constraints such as parameter nullability.

sqlc's `verify` addresses a different problem. It checks whether new schema changes are safe against previously pushed queries, but its documented workflow depends on sqlc Cloud, tags, and an auth token. That is useful, but it is not the same thing as committed per-query contract files living in the repo.

### 3. pGenie treats index management as part of the workflow

sqlc's `vet` can look at `EXPLAIN` output and help you enforce rules such as "no sequential scans". pGenie goes further in a different direction: `pgn manage-indexes` inspects observed query usage and existing indexes, then proposes a migration that can both create missing indexes and drop stale or redundant ones.

### 4. pGenie is narrower on purpose

pGenie is PostgreSQL-only. That is a limitation if you need MySQL or SQLite, but it is also how pGenie justifies a richer PostgreSQL-centric model. In the pGenie docs, composite types and multiranges are part of the story, not edge cases.

---

## What sqlc Issues Suggest

The recurring pain points in sqlc's issue tracker are not basic CRUD. They cluster around advanced PostgreSQL behavior, type inference, and deeper engine-specific modeling.

Examples:

- Composite types are still an open proposal: [sqlc-dev/sqlc#2760](https://github.com/sqlc-dev/sqlc/issues/2760).
- Nullability hints are still an open request: [sqlc-dev/sqlc#4340](https://github.com/sqlc-dev/sqlc/issues/4340).
- `ALTER TYPE ... ADD ATTRIBUTE` can still fail analysis in migration-driven workflows: [sqlc-dev/sqlc#3997](https://github.com/sqlc-dev/sqlc/issues/3997).
- Valid PostgreSQL constructs can still hit analyzer edge cases, such as multi-array `UNNEST`: [sqlc-dev/sqlc#3507](https://github.com/sqlc-dev/sqlc/issues/3507).
- Type override edge cases still show up, for example array columns to slices of custom enum types: [sqlc-dev/sqlc#4359](https://github.com/sqlc-dev/sqlc/issues/4359).
- Table-valued JSON functions have also surfaced analyzer blind spots: [sqlc-dev/sqlc#1480](https://github.com/sqlc-dev/sqlc/issues/1480).

This does **not** mean sqlc is weak. It means its rough edges show up exactly where PostgreSQL-specific behavior gets deep. That is the area where pGenie's architecture is trying to be strongest.

---

## Dynamic Queries: The Main Real-World Objection

The strongest reaction to the pGenie announcement threads was about genuinely dynamic query builders: conditional joins, user-selected field sets, and report-style queries assembled at runtime.

pGenie's position is deliberate: optimize for **static SQL**. In practice that means:

- optional filters via nullable parameters,
- optional ordering via `CASE`,
- conditional projections,
- stored procedures for logic that belongs in PostgreSQL,
- or simply splitting behavior into several explicit queries.

If your application truly assembles SQL structure at runtime, pGenie is usually the wrong tool. sqlc offers a few more escape hatches such as `sqlc.slice`, but it is also at its best when the query shape is mostly static. For heavy runtime query construction, a query builder is usually the better fit than either tool.

---

## Why pGenie Is Not "Just a sqlc Plugin"

This question came up in the announcement discussions and the answer is architectural.

pGenie's main differences are upstream of code generation:

- live PostgreSQL analysis,
- committed signature files,
- PostgreSQL-only internal modeling,
- index analysis and migration generation.

Those are not just output-template choices. They are core workflow decisions. A sqlc plugin could change the generated code, but it would not reproduce the parts of pGenie that make pGenie distinct.

---

## Bottom Line

If you want the broader, more established project with multiple databases, multiple language options, macros, linting rules, and a larger community, sqlc is the safer default.

If you want the narrower tool that goes all-in on PostgreSQL, validates queries through PostgreSQL itself, keeps explicit query contracts in your repo, and helps manage indexes, pGenie is solving a different and sharper problem.