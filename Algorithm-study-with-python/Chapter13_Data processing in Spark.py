from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('cloudanum').getOrCreate()

df = spark.read.csv('taxi2.csv', inferSchema=True, header=True)

print(df.columns)

df.createOrReplaceTempView("main")

data = spark.sql("SELECT payment_type, Count(*) AS COUNT, AVG(fare_amount), AVG(tip_amount) AS AverageFare from main GROUP BY payment_type")

data.show()
