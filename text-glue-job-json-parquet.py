import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

# Create SparkContext and GlueContext
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Get job name from command-line arguments
args = getResolvedOptions(sys.argv, ["JOB_NAME"])
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node S3 bucket
S3bucket_node1 = glueContext.create_dynamic_frame.from_catalog(
    database="input", table_name="texttext_json", transformation_ctx="S3bucket_node1"
)

# Data preprocessing
normalized_data = S3bucket_node1.toDF().select(
    lower(col("source")).alias("source"),
    col("source_labels"),
    col("rouge_scores"),
    col("paper_id"),
    col("target"),
    col("title")
)

# Feature engineering
# Example: Adding a feature based on the length of the source text
normalized_data = normalized_data.withColumn("source_length", length(col("source")))

# Data enrichment
# Example: Adding a feature based on the count of unique words in the source text
tokenizer = Tokenizer(inputCol="source", outputCol="tokens")
tokenized_data = tokenizer.transform(normalized_data)
word_count = udf(lambda x: len(set(x)), IntegerType())
enriched_data = tokenized_data.withColumn("unique_word_count", word_count(col("tokens")))

# Script generated for node Amazon S3
AmazonS3_node1687108745304 = glueContext.write_dynamic_frame.from_options(
    frame=enriched_data,
    connection_type="s3",
    format="glueparquet",
    connection_options={
        "path": "s3://scitdlr-project-glue/output/text-parquet/",
        "partitionKeys": [],
    },
    format_options={"compression": "gzip"},
    transformation_ctx="AmazonS3_node1687108745304",
)

# Commit the job
job.commit()
