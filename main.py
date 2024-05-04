import boto3
import json
def process_data(s3_bucket, data_key, rds_host, rds_database, rds_username, rds_password, glue_database):
    s3_client = boto3.client('s3')
    response = s3_client.get_object(Bucket=s3_bucket, Key=data_key)
    data = json.loads(response['Body'].read().decode('utf-8')) 
    try:
        rds_client = boto3.client('rds')
        connection = rds_client.connect_to_database(
            DBInstanceIdentifier=rds_host,
            Database=rds_database,
            Username=rds_username,
            Password=rds_password
        )
        cursor = connection.cursor()
        cursor.execute("INSERT INTO your_table (column1, column2, ...) VALUES (%s, %s, ...)", (data['value1'], data['value2'], ...))
        connection.commit()
    except Exception as e:
        print(f"Error connecting to RDS: {e}")
    if glue_database:
        try:
            glue_client = boto3.client('glue')
            
            glue_client.put_database_records(
                DatabaseName=glue_database,
                TableName="your_table",
                Records=[{"record": data}]
            )
        except Exception as e:
            print(f"Error writing to Glue database: {e}")
if _name_ == "_main_":
    s3_bucket = os.environ['S3_BUCKET']
    data_key = os.environ['DATA_KEY']
    process_data(s3_bucket, data_key, ...) 
