import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node S3 bucket
S3bucket_node1 = glueContext.create_dynamic_frame.from_catalog(
    database="input", table_name="texttext_json", transformation_ctx="S3bucket_node1"
)

# Script generated for node Change Schema
ChangeSchema_node1687108655237 = ApplyMapping.apply(
    frame=S3bucket_node1,
    mappings=[
        ("source", "array", "source", "array"),
        ("source_labels", "array", "source_labels", "array"),
        ("rouge_scores", "array", "rouge_scores", "array"),
        ("paper_id", "string", "paper_id", "string"),
        ("target", "array", "target", "array"),
        ("title", "string", "title", "string"),
    ],
    transformation_ctx="ChangeSchema_node1687108655237",
)

# Script generated for node Amazon S3
AmazonS3_node1687108745304 = glueContext.write_dynamic_frame.from_options(
    frame=ChangeSchema_node1687108655237,
    connection_type="s3",
    format="glueparquet",
    connection_options={
        "path": "s3://scitdlr-project-glue/output/text-parquet/",
        "partitionKeys": [],
    },
    format_options={"compression": "gzip"},
    transformation_ctx="AmazonS3_node1687108745304",
)

job.commit()
