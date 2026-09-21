# Databricks notebook source
# MAGIC %sql
# MAGIC
# MAGIC Create catalog if not exists fmcg;
# MAGIC use catalog fmcg;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE SCHEMA IF NOT EXISTS FMCG.gold;
# MAGIC
# MAGIC CREATE SCHEMA IF NOT EXISTS FMCG.silver;
# MAGIC
# MAGIC CREATE SCHEMA IF NOT EXISTS FMCG.bronze;

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*) from fmcg.gold.fact_orders;