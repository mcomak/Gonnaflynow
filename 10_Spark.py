import findspark
import configparser
from Scraper import Scraper
import time

# /opt/manual/spark: this is SPARK_HOME path
findspark.init("/opt/manual/spark")
from pyspark.sql import SparkSession, functions as F

spark = SparkSession.builder \
    .appName("JDBC and Spark") \
    .master("local[2]") \
    .getOrCreate()

config = configparser.RawConfigParser()

config.read('./db_conn')
user_name = config.get('DB', 'user_name')
password = config.get('DB', 'password')
db_ip = config.get('DB', 'db_ip')

jdbcUrl = f"jdbc:postgresql://{db_ip}:5432/sky?user={user_name}&password={password}"

sc = Scraper(location='frankfurt')
sc.inject_to_df()


spark_df = spark.createDataFrame(sc.df)
# spark_df.show()
# Read the data from PostgreSQL into a Spark dataframe
postgres_df = spark.read.jdbc(url=jdbcUrl,
                              table='frankfurt_departures',
                              properties={"driver": 'org.postgresql.Driver'})


# Keep only the last 50 rows from the PostgreSQL data
postgres_df.createOrReplaceTempView("postgres_table")

postgres_df_50= spark.sql("""
SELECT * 
FROM postgres_table
ORDER BY Date DESC,Planned DESC
LIMIT 50
""")

unique_rows_df = spark_df.subtract(postgres_df_50)
unique_rows_df.write.jdbc(url=jdbcUrl,
                     table='frankfurt_departures',
                     mode="append",
                     properties={"driver": 'org.postgresql.Driver'})

# unique_rows_df.show()
# postgres_df_50.show()
# spark_df.show()
