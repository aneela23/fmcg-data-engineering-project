# Architecture

## End-to-End Architecture

The project consists of two data paths:

1. Parent company data
2. Child company data

The parent company already has structured analytical data.

The child company data goes through the Medallion Architecture before being consolidated with the parent company.

---

## Parent Company

```text
PostgreSQL
    |
    v
Parent Company Data
    |
    v
Analytical / Gold Structure
