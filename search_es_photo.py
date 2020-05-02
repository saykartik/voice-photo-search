"""
Committed through code pipeline
"""
import json
import os
from botocore.vendored import requests


def lambda_handler(event, context):
    # TODO implement
    print("Event was:", event)
    print("context was", context)

    things = event['body']
    es_url = 'https://search-photo-index-auto-iiwufwhfvifoyriogwcioz2ewu.us-east-1.es.amazonaws.com/photos/_search'
    s3_url = 'https://ppkbphotos-auto.s3.amazonaws.com/'

    photo_list = []
    url_list = []
    for thing in things:
        query = "{}?q=labels:*{}*".format(es_url, thing)
        print(query)
        res = requests.get(query).json()['hits']['hits']
        print(res)
        this_photo_list = [a["_source"]["objectKey"] for a in res]
        photo_list = photo_list + this_photo_list
        url_list = url_list + [s3_url + item for item in this_photo_list]

    photo_list = list(set(photo_list))
    url_list = list(set(url_list))
    return {
        'statusCode': 200,
        'body': url_list
    }
