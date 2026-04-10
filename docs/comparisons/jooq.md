# pGenie vs jOOQ

pGenie and jOOQ both help you write type-safe database code, but they optimize for different workflows.

## Short Answer

Choose **pGenie** if you want to keep SQL in `.sql` files, treat PostgreSQL as the source of truth, and generate a thin typed client around that SQL.

Choose **jOOQ** if you want to build queries directly in Java with a fluent DSL and need dynamic, composable query construction.

---

## At a Glance

| Question | pGenie | jOOQ |
|---|---|---|
| Query authoring | Plain PostgreSQL SQL in `.sql` files | Java DSL over generated schema types |
| Source of truth | SQL migrations and query files | Java query code plus schema metadata |
| Database scope | PostgreSQL only | Multiple SQL dialects |
| Query shape | Static statements checked at generation time | Dynamic and composable queries built in Java |
| Analysis model | Uses a live PostgreSQL instance to validate queries against your migrations | Generates types from schema metadata and runs the DSL at runtime |
| Type contract | Per-query signature files live in your repo | Schema-generated types, but query logic stays in Java |
| Index guidance | `pgn manage-indexes` can suggest and generate index migrations | No equivalent index-management workflow |
| Target languages | Java, Rust, Haskell today; extensible via Dhall | Java-centric |
| Best fit | PostgreSQL-first projects that want SQL-first codegen | Java applications that need fluent, dynamic query construction |

## Why pGenie Feels Different

pGenie keeps the query text in source control and validates it against a live PostgreSQL instance. That means the SQL you review is the SQL that gets analyzed, and the generated client code stays a thin wrapper around it.

Each query also gets a committed signature file beside it. That makes parameter types, result shapes, and nullability visible in diffs instead of hiding them inside generated Java.

pGenie also treats index analysis as part of the workflow. If an existing query pattern needs an index, `pgn manage-indexes` can suggest and generate that change.

## When jOOQ May Be a Better Fit

jOOQ is a better fit when your query structure is determined in Java at runtime. Optional filters, conditional joins, composable fragments, and other dynamic patterns are where a fluent DSL is useful.

It is also a good fit if you want to stay entirely in Java and lean on a long-established ecosystem around the query API itself.

## Bottom Line

If you want SQL-first code generation with PostgreSQL as the analysis engine, pGenie is the better fit.

If you want to assemble queries in Java with a fluent DSL and need dynamic composition, jOOQ is the better fit.
