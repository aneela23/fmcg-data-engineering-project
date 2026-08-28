# FMCG Data Engineering Platform

An end-to-end data engineering project that integrates FMCG sales data from a parent company and an acquired child company.

The project demonstrates data ingestion, data quality, transformation, dimensional modeling, incremental processing, data consolidation, and analytics using modern data engineering technologies.

---

## 📌 Project Overview

This project simulates an FMCG (Fast-Moving Consumer Goods) business scenario where a parent company acquires a child company.

The parent company already has an established analytical data platform, while the child company has data coming from separate source files with different structures and data-quality issues.

The goal is to build a scalable data pipeline that:

- Ingests child-company source data
- Preserves raw data
- Cleans and standardizes data
- Transforms data into business-ready datasets
- Aligns child-company data with the parent-company data model
- Consolidates parent and child data
- Supports analytical and BI workloads

---

## 🎯 Project Objectives

- Build an end-to-end data engineering pipeline
- Implement a Medallion Architecture
- Practice PySpark and SQL transformations
- Implement data-quality rules
- Work with fact and dimension tables
- Implement incremental data processing
- Consolidate data from parent and child companies
- Create analytics-ready datasets
- Build a foundation for BI reporting
- Practice Databricks concepts relevant to the Databricks Data Engineer certification

---

## 🏗️ Technology Stack

| Technology | Purpose |
|---|---|
| PostgreSQL | Relational source database |
| DBeaver | Database development and ER diagrams |
| Python | Data engineering and utility logic |
| SQL | Data modeling, validation and analytics |
| AWS S3 | Data lake / file storage |
| Databricks | Data engineering platform |
| PySpark | Large-scale data transformation |
| Delta Lake | Transactional data storage |
| Airflow / Databricks Workflows | Pipeline orchestration |
| GitHub | Source control and documentation |
| Power BI | Analytics and visualization |

---

## 🏛️ Architecture

The project follows a Medallion Architecture for the child-company pipeline.

                    PARENT COMPANY
                       PostgreSQL
                           |
                           v
                    Parent Gold Data
                           |
                           v
                    +-------------+
                    |             |
                    | Consolidated|
                    |    Gold     |
                    |             |
                    +-------------+
                           ^
                           |
                    CHILD COMPANY
                           |
                           v
                          S3
                           |
                           v
                       BRONZE
                           |
                           v
                        SILVER
                   Data Cleaning
                   & Standardization
                           |
                           v
                         GOLD
                           |
                           v
                    Child Gold Data
                           |
                           v
                  Parent + Child
                    Consolidation

<img width="1024" height="1536" alt="image" src="https://github.com/user-attachments/assets/1d4ff860-04ad-44b8-a280-8ae49352a6dc" />

