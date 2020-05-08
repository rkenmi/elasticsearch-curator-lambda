import boto3
from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch, RequestsHttpConnection
import curator
import os

service = 'es'
credentials = boto3.Session().get_credentials()

ES_HOST = os.environ['ES_HOST']
ES_REGION = os.environ['ES_REGION']

awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, ES_REGION, service, session_token=credentials.token)

# Lambda execution starts here.
def lambda_handler(event, context):
    # Build the Elasticsearch client.
    es = Elasticsearch(
        hosts=[{'host': ES_HOST, 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )

    index_list = curator.IndexList(es)

    # Filters by age, anything created more than 30 minutes ago.
    index_list.filter_by_age(source='creation_date', direction='older', unit='minutes', unit_count=30)

    print("Found %s indices to delete" % len(index_list.indices))

    # If our filtered list contains any indices, delete them.
    if index_list.indices:
        curator.DeleteIndices(index_list).do_action()