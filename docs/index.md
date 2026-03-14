# pGenie

**pGenie** is a type-safe PostgreSQL client code generator. It analyzes your SQL migrations and parameterized queries against a real PostgreSQL instance, then produces idiomatic, fully-typed client libraries for your target language.

---

## Why pGenie?

Working with relational databases from application code has always involved an uncomfortable tradeoff:

- **ORMs** are expressive but hide SQL behind an abstraction layer that makes complex queries awkward and performance hard to reason about.
- **Query builders** keep you closer to SQL but still add a layer of abstraction and library-specific syntax to learn.
- **Raw SQL** with a simple driver is honest and efficient, but leaves type safety and correctness entirely up to you—parameter types, result shapes, and nullability are unchecked until runtime.

pGenie takes a different path: **write plain SQL, get type-safe code**. There is no ORM magic, no query builder DSL, no code annotations. You write standard PostgreSQL SQL in `.sql` files, and pGenie generates the boilerplate so your application code gains compile-time guarantees about every query's parameters and results.

### Goals

1. **SQL-first**: The database schema and queries are the single source of truth. The generated code always reflects exactly what the database expects.
2. **Zero runtime overhead**: Generated code is static and inlined at compile time—no reflection, no dynamic type mapping at runtime.
3. **Correctness over convenience**: pGenie runs your queries against an actual PostgreSQL server (via Docker) during generation. If a query is wrong, you find out at generation time, not in production.
4. **Language-idiomatic output**: Each code generator produces code that feels natural in its target language—proper type names, naming conventions, and library idioms.
5. **Extensibility**: Code generators are plain [Dhall](https://dhall-lang.org/) programs. Anyone can write a generator for a new target language or framework.

---

## How pGenie Compares

| | pGenie | ORM | Query builder | Raw SQL |
|---|---|---|---|---|
| Write plain SQL | ✅ | ❌ | Partial | ✅ |
| Compile-time type safety | ✅ | Partial | Partial | ❌ |
| No runtime abstraction layer | ✅ | ❌ | ❌ | ✅ |
| Detects errors at generation time | ✅ | ❌ | ❌ | ❌ |
| Works with arbitrary SQL | ✅ | ❌ | ❌ | ✅ |
| Extensible code generation | ✅ | ❌ | ❌ | N/A |

### vs. sqlc

[sqlc](https://sqlc.dev/) is the closest conceptual peer to pGenie. Both parse SQL and generate typed client code. The key differences are:

- pGenie uses a **real PostgreSQL instance** (via Docker) to analyze queries, which means it supports the full PostgreSQL type system—including composite types, custom enumerations, and complex expressions—without maintaining a bespoke SQL parser.
- pGenie's code generators are **user-extensible Dhall programs** distributed as URLs, not compiled plugins.
- pGenie currently targets Haskell; sqlc targets Go, Kotlin, and Python.

---

## Getting Started

Install pGenie by following the [Installation guide](guides/installation.md), then work through the [Tutorials](tutorials/learn-pgenie-in-y-minutes.md) for a hands-on introduction.
