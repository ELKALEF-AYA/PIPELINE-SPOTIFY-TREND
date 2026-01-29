import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Default ruleset used by all target nodes with data quality enabled
DEFAULT_DATA_QUALITY_RULESET = """
    Rules = [
        ColumnCount > 0
    ]
"""

# Script generated for node Amazon S3
AmazonS3_node1769216687038 = glueContext.create_dynamic_frame.from_options(format_options={"quoteChar": "\"", "withHeader": True, "separator": ",", "optimizePerformance": False}, connection_type="s3", format="csv", connection_options={"paths": ["s3://spotify-pipeline-aya/raw/daily/"], "recurse": True}, transformation_ctx="AmazonS3_node1769216687038")

# Script generated for node Change Schema
ChangeSchema_node1769216799604 = ApplyMapping.apply(frame=AmazonS3_node1769216687038, mappings=[("rank", "string", "rank", "string"), ("uri", "string", "uri", "string"), ("artist_names", "string", "artist_names", "string"), ("track_name", "string", "track_name", "string"), ("source", "string", "source", "string")], transformation_ctx="ChangeSchema_node1769216799604")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=ChangeSchema_node1769216799604, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1769216581644", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1769217279687 = glueContext.getSink(path="s3://spotify-pipeline-aya-clean-v2", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="AmazonS3_node1769217279687")
AmazonS3_node1769217279687.setCatalogInfo(catalogDatabase="spotify_clean_db",catalogTableName="tracks_clean")
AmazonS3_node1769217279687.setFormat("glueparquet", compression="snappy")
AmazonS3_node1769217279687.writeFrame(ChangeSchema_node1769216799604)
job.commit()