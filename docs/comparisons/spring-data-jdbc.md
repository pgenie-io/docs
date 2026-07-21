# pGenie vs Spring Data JDBC

pGenie and Spring Data JDBC both give you typed access to a relational database from Java, but they do it differently and fit different project contexts.

## Short Answer

Choose **pGenie** if you want SQL files as the source of truth, full build-time type checking validated against a real PostgreSQL instance, and generated clients for multiple languages without a framework dependency.

Choose **Spring Data JDBC** if you are building a Spring application, want method-name-derived queries and entity mapping with minimal boilerplate, or need reactive non-blocking database access via Spring Data R2DBC.

---

## At a Glance

| Question | pGenie | Spring Data JDBC |
|---|---|---|
| Query authoring | Plain PostgreSQL SQL in `.sql` files | Method-name derivation (`findByEmailAndStatus`) plus `@Query` for custom SQL |
| Source of truth | SQL migrations and query files | Annotated Java entity classes |
| Type safety | Full compile-time: parameters and result shapes inferred at generation time | Compile-time for entity fields; `@Query` SQL strings are checked at runtime |
| Schema drift protection | Build fails if a migration changes a column a query uses | No equivalent build-time protection for `@Query` strings |
| Analysis model | Validates each query against a live PostgreSQL instance at generation time | Executes against the database at runtime |
| Database scope | PostgreSQL only | PostgreSQL, MySQL, MariaDB, Oracle, SQL Server, H2, and others |
| Framework requirement | None | Spring Framework and its dependency injection container |
| Method-name-derived queries | Not supported | Yes — `findByEmailAndStatus`, `countByActiveTrue`, `deleteByExpiredBefore`, etc. |
| Dynamic queries | Not supported | Via Specifications or QueryDSL integration |
| Multi-language support | Java, Haskell, Rust; extensible via Dhall generators | Java only |
| Reactive support | No — blocking JDBC only | Yes — Spring Data R2DBC provides reactive access via Project Reactor |
| Index management | `pgn manage-indexes` can suggest and generate index migrations | None built-in |

## What Spring Data JDBC Is

Spring Data JDBC is worth distinguishing from JPA/Hibernate. It deliberately omits lazy loading, dirty tracking, and L1/L2 caches. Each query loads data explicitly, and entities do not carry hidden state. That makes it simpler and more predictable than a full ORM while still providing entity mapping, the repository pattern, and method-name-derived queries.

## What Is Different About pGenie

pGenie does not model entities. Instead, each query lives in a `.sql` file and is validated against a live PostgreSQL instance at generation time. The generated Java code is a typed wrapper around those queries — no annotations, no repository interfaces, no framework.

Each query also gets a `.sig1.pgn.yaml` signature file alongside it. That file records the inferred parameter types, result column types, and nullability. It is committed to the repository and shows up in diffs, making the contract of every query explicit and reviewable.

Because type information is extracted by running the query against a real PostgreSQL instance, pGenie reflects the actual behavior of the database rather than an approximation of it. This also means it supports the full PostgreSQL feature set, including composite types, multiranges, and other types that annotation-based tools may not handle.

## When Spring Data JDBC May Be a Better Fit

Spring Data JDBC fits naturally when:

- The application is already built on Spring and the framework dependency is expected.
- Method-name-derived queries (`findByX`, `countByX`, `deleteByX`) cover most of the query surface without needing custom SQL.
- The project needs to run against more than one database engine.
- Dynamic query construction is required.
- You want to avoid a separate code generation step in the build pipeline.

## The Reactive Variant (Spring Data R2DBC)

Spring Data R2DBC replaces the JDBC driver with R2DBC and returns `Mono<T>` and `Flux<T>` types from Project Reactor. The entity model, repository pattern, and method-name derivation carry over from Spring Data JDBC; the difference is non-blocking I/O and integration with reactive pipelines.

pGenie's Java codegen uses JDBC and produces blocking call signatures. If your application requires reactive or non-blocking database access, Spring Data R2DBC is a better fit. The rest of the Spring Data JDBC comparison — entity annotations, `@Query` strings, framework dependency, and runtime type checking of custom SQL — applies equally to the R2DBC variant.

## Bottom Line

Spring Data JDBC fits Spring applications that want entity mapping, method-name-derived queries, and the Spring ecosystem, with an optional reactive variant via R2DBC.

pGenie fits projects where SQL files are the primary artifact, build-time type validation against a real PostgreSQL instance matters, and the generated client needs to work across multiple languages without a framework dependency.
