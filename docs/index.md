# pGenie

**pGenie** is a type-safe PostgreSQL client code generator. It analyzes your SQL migrations and parameterized queries against a real PostgreSQL instance, then produces idiomatic, fully-typed client libraries for your target language.

---

## Why pGenie?

Working with relational databases from application code has always involved an uncomfortable tradeoff:

- **ORMs** are expressive but hide SQL behind an abstraction layer that makes complex queries awkward and performance hard to reason about.
- **Query builders** keep you closer to SQL but still add a layer of abstraction and library-specific syntax to learn.
- **Raw SQL** with a simple driver is honest and efficient, but leaves type safety and correctness entirely up to you - parameter types, result shapes, and nullability are unchecked until runtime.

pGenie takes a different path: **write plain SQL, get type-safe code**. There is no ORM magic, no query builder DSL, no code annotations. You write standard PostgreSQL SQL in `.sql` files, and pGenie generates the boilerplate so your application code gains compile-time guarantees about every query's parameters and results.

### Goals

1. **SQL-first**: The database schema and queries are the single source of truth. The generated code always reflects exactly what the database expects.
2. **Zero runtime overhead**: Generated code is static - no reflection, no dynamic type mapping at runtime.
3. **Correctness over convenience**: pGenie runs your queries against an actual PostgreSQL server (via Docker) during generation. If a query is wrong, you find out at generation time, not in production.
4. **Language-idiomatic output**: Each code generator produces code that feels natural in its target language - proper type names, naming conventions, and library idioms.
5. **Extensibility**: Code generators are plain [Dhall](https://dhall-lang.org/) programs. Anyone can write a generator for a new target language or framework or fork an existing one, tweak it and immediately use it by referencing its URL in the project configuration.

---

## How pGenie Compares

The table below highlights the most important differentiators. "Partial" means the feature exists but comes with significant caveats (e.g. limited type coverage, annotation-heavy setup, or no enforcement at build time).

| | pGenie | ORM | Query builder | Raw SQL |
|---|---|---|---|---|
| SQL is the source of truth | ✅ | ❌ | ❌ | ✅ |
| Static type safety — no annotations | ✅ | ❌ | ❌ | ❌ |
| Verified against real PostgreSQL | ✅ | ❌ | ❌ | ❌ |
| Build fails on schema/query mismatch | ✅ | ❌ | ❌ | ❌ |
| Multi-language output from one project | ✅ | ❌ | ❌ | ❌ |
| Zero runtime abstraction overhead | ✅ | ❌ | Partial | ✅ |
| Automatic index management | ✅ | Partial | ❌ | ❌ |

### Key differentiators

**SQL is the source of truth.** You write standard PostgreSQL SQL — no ORM model classes, no DSL. The generated code follows exactly what the database schema and your SQL say.

**Type safety without annotations.** Parameter types and result-column types are inferred by preparing each statement against a real PostgreSQL instance. There is nothing to annotate and nothing to keep in sync manually.

**Build-time schema drift protection.** Every query is validated against the current schema at generation time. If a migration changes a column type that a query uses, pGenie fails the build and tells you exactly what changed — before the mismatch can reach production.

**Multi-language from one project.** A single `pgn generate` run can produce typed client libraries for multiple languages simultaneously. Each target language gets idiomatic code from its own [Dhall](https://dhall-lang.org/) generator, and anyone can write a new generator without touching pGenie itself.

---

## Getting Started

Install pGenie by following the [Installation guide](guides/installation/index.md), then work through the [Tutorials](tutorials/learn-pgenie-in-y-minutes.md) for a hands-on introduction.
