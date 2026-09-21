# Databricks notebook source
from pyspark.sql import functions as F
from delta.tables import DeltaTable



# COMMAND ----------

# MAGIC %run /Workspace/consolidated_pipeline/utilities

# COMMAND ----------

print(bronze_schema, silver_schema, gold_schema)

# COMMAND ----------

dbutils.widgets.text("catalog", "fmcg", "catalog")
dbutils.widgets.text("data_source", "customers", "Data Source")

# COMMAND ----------

catalog = dbutils.widgets.get("catalog")
data_source = dbutils.widgets.get("data_source")

base_path = f's3://sports-dp/customers/customers.csv'
print(base_path)

# COMMAND ----------

df = (
    spark.read.format("csv")
    .option("header", True)
    .option("inferSchema", True)
    .load(base_path)
    .withColumn("read_timestamp", F.current_timestamp())
    .select("*", "_metadata.file_name","_metadata.file_size")
)
display(df.limit(10))

# COMMAND ----------

df.printSchema()

# COMMAND ----------

df.write \
    .format("delta") \
    .option("delta.enableChangeDataFeed", "true") \
    .mode("overwrite") \
    .saveAsTable(f"{catalog}.{bronze_schema}.{data_source}")

# COMMAND ----------

# MAGIC %md
# MAGIC ###silver processing
# MAGIC

# COMMAND ----------

df_bronze = spark.sql(f"SELECT * FROM {catalog}.{bronze_schema}.{data_source};")
df_bronze.show(10)

# COMMAND ----------

df_bronze.printSchema()

# COMMAND ----------

df_bronze \
    .groupBy("customer_id") \
    .count() \
    .filter(F.col("count") > 1) \
    .show()

# COMMAND ----------

print("Before:", df_bronze.count())

df_silver = df_bronze.dropDuplicates(["customer_id"])

print("After:", df_silver.count())

# COMMAND ----------

df_silver \
    .filter(F.trim(F.col("customer_name")) != F.col("customer_name")) \
    .show()

# COMMAND ----------

df_silver = df_silver.withColumn(
    "customer_name",
    F.trim(F.col("customer_name"))
)

# COMMAND ----------

df_silver.select("city").distinct().show()

# COMMAND ----------

# typos -> correct names
city_mapping = {
    'Bengaluruu': 'Bengaluru',
    'Bengalore': 'Bengaluru',

    'Hyderabadd': 'Hyderabad',
    'Hyderbad': 'Hyderabad',

    'NewDelhi': 'New Delhi',
    'NewDheli': 'New Delhi',
    'NewDelhee': 'New Delhi'
}

allowed = ["Bengaluru", "Hyderabad", "New Delhi"]

df_silver = (
    df_silver
    .replace(city_mapping, subset=["city"])
    .withColumn(
        "city",
        F.when(F.col("city").isNull(), None)
         .when(F.col("city").isin(allowed), F.col("city"))
         .otherwise(None)
    )
)



# COMMAND ----------

df_silver = df_silver.withColumn(
    "customer_name",
    F.when(
        F.col("customer_name").isNull(),
        F.col("customer_name")
    ).otherwise(
        F.initcap(F.col("customer_name"))
    )
)

# COMMAND ----------

df_silver.select("customer_name").distinct().show()

# COMMAND ----------

df_silver \
    .filter(F.col("city").isNull()) \
    .show()

# COMMAND ----------

# Business Confirmation Note: City corrections
customer_city_fix = {
    # SprintX Nutrition
    789403: "New Delhi",

    # Zenathlete Foods
    789420: "Bengaluru",

    # Primefuel Nutrition
    789521: "Hyderabad",

    # Recovery Lane
    789603: "Hyderabad"
}

df_fix = spark.createDataFrame(
    [(k, v) for k, v in customer_city_fix.items()],
    ["customer_id", "fixed_city"]
)

# COMMAND ----------

df_silver = (
    df_silver
    .join(df_fix, on="customer_id", how="left")
    .withColumn(
        "city",
        F.coalesce(F.col("city"), F.col("fixed_city"))
    )
    .drop("fixed_city")
)


display(df_silver)

# COMMAND ----------

df_silver = df_silver.withColumn(
    "customer_id",
    F.col("customer_id").cast("string")
)

print(df_silver.printSchema())

# COMMAND ----------

df_silver = (
    df_silver
    .withColumn("market", F.lit("India"))
    .withColumn("platform", F.lit("Sports Bar"))
    .withColumn("channel", F.lit("Acquisition"))
    .withColumn(
        "customer",
        F.concat_ws(
            " - ",
            F.coalesce(F.col("customer_name"), F.lit("Unknown")),
            F.coalesce(F.col("city"), F.lit("Unknown"))
        )
    )
)

display(df_silver)

# COMMAND ----------

df_silver.write \
    .format("delta") \
    .option("delta.enableChangeDataFeed", "true")\
    .option("mergeSchema", "true")\
    .mode("overwrite") \
    .saveAsTable(f"{catalog}.{silver_schema}.{data_source}")

# COMMAND ----------

# MAGIC %md
# MAGIC Gold Processing
# MAGIC

# COMMAND ----------

df_gold = spark.sql(f"""
    SELECT
        customer_id,
        customer,
        market,
        platform,
        channel
    FROM {catalog}.{silver_schema}.{data_source}
""")

display(df_gold)

# COMMAND ----------

catalog = dbutils.widgets.get("catalog")
data_source = dbutils.widgets.get("data_source")

print(catalog)
print(data_source)

# COMMAND ----------

# MAGIC %run /Workspace/consolidated_pipeline/utilities

# COMMAND ----------

print(bronze_schema)
print(silver_schema)
print(gold_schema)

# COMMAND ----------

df_gold.write \
    .format("delta") \
    .option("delta.enableChangeDataFeed", "true")\
    .mode("overwrite") \
    .saveAsTable(f"{catalog}.{gold_schema}.sb_dim_customers")

# COMMAND ----------

df_gold = spark.sql(f"""
    SELECT
        customer_id,
        customer_name,
        city,
        customer,
        market,
        platform,
        channel
    FROM {catalog}.{silver_schema}.{data_source}
""")

display(df_gold)

# COMMAND ----------

df_gold.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable(f"{catalog}.{gold_schema}.sb_dim_customers")

# COMMAND ----------

df_child_customers = spark.table("fmcg.gold.sb_dim_customers").select(
    F.col("customer_id").alias("customer_code"),
    F.col("customer"),
    F.col("market"),
    F.col("platform"),
    F.col("channel")
)

display(df_child_customers)

# COMMAND ----------

from delta.tables import DeltaTable

delta_table = DeltaTable.forName(
    spark,
    "fmcg.gold.dim_customers"
)

# COMMAND ----------

delta_table.alias("target").merge(
    source=df_child_customers.alias("source"),
    condition="target.customer_code = source.customer_code"
) \
.whenMatchedUpdateAll() \
.whenNotMatchedInsertAll() \
.execute()