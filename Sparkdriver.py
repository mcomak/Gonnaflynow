import findspark
import configparser
from Scraper import Scraper
import time

# /opt/manual/spark: this is SPARK_HOME path
findspark.init("/opt/manual/spark")
from pyspark.sql import SparkSession, functions as F

class Captain_Spark:

    def __init__(self,location='frankfurt'):
        self.location = location
    # Spark building
    def Spark_builder(self):
        self.spark = SparkSession.builder \
            .appName("JDBC and Spark") \
            .master("local[2]") \
            .getOrCreate()
        return self.spark

    def call_scraper(self):
        sc = Scraper(location=self.location)
        sc.inject_to_df()
        self.spark_df = self.spark.createDataFrame(sc.df)
        return self.spark_df

    def read_postgres(self):
        # Postgresql Credentials
        config = configparser.RawConfigParser()
        config.read('./db_conn')
        user_name = config.get('DB', 'user_name')
        password = config.get('DB', 'password')
        db_ip = config.get('DB', 'db_ip')

        #jdbc adress
        self.jdbcUrl = f"jdbc:postgresql://{db_ip}:5432/sky?user={user_name}&password={password}"

        # Read the data from PostgreSQL into a Spark dataframe
        postgres_df = self.spark.read.jdbc(url=self.jdbcUrl,
                                      table='frankfurt_departures',
                                      properties={"driver": 'org.postgresql.Driver'})
        # Keep only the last 50 rows from the PostgreSQL data
        postgres_df.createOrReplaceTempView("postgres_table")

        self.postgres_df_50= self.spark.sql("""
        SELECT * 
        FROM postgres_table
        ORDER BY Date DESC,Planned DESC
        LIMIT 50
        """)
        return self.postgres_df_50

    def write_postgres(self):
        unique_rows_df = self.spark_df.subtract(self.postgres_df_50)
        unique_rows_df.write.jdbc(url=self.jdbcUrl,
                             table='frankfurt_departures',
                             mode="append",
                             properties={"driver": 'org.postgresql.Driver'})


    def stoper(self):
        self.sc.quit_driver()
        self.spark.stop()


sp = Captain_Spark()
sp.Spark_builder()
sp.call_scraper()
# sp.read_postgres()
# sp.duplicate_detector()
# sp.stoper()