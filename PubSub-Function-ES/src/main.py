import base64
from elasticsearch import Elasticsearch#, RequestsHttpConnection
import datetime, time
import json,os
from google.cloud import logging as cloudlogging
import logging

lg_client = cloudlogging.Client()
lg_handler = lg_client.get_default_handler()
cloud_logger = logging.getLogger("cloudLogger")
cloud_logger.setLevel(logging.INFO)
cloud_logger.addHandler(lg_handler)

esendpoint = os.environ.get('ELASTICSEARCH_IP' ,'localhost')
OFFSET = int(os.environ.get('OFFSET_FROM_TODAY','0'))
es = Elasticsearch(
    [{'host':esendpoint,'port':9200}],
    # hosts=[{'host': esendpoint, 'port': 443}],
    # http_auth=awsauth,
    # use_ssl=True,
    # verify_certs=True,
    # ca_certs=certifi.where(),
    # connection_class=RequestsHttpConnection
)
esinfo = es.info()
cloud_logger.info(esinfo)
TODAY = str(datetime.datetime.utcnow()).split(' ')[0]   # date only
es.indices.create(index='acme', ignore=400)  # create index - ignore if already created

def updateInventory(items, date = TODAY):
    for item in items:
        # res=es.get(index='acme',doc_type='inventory',id=i)
        # print(res['_source'])
        #print(date, item['key'])
        # res = es.search(index='acme',body={'query':{'match':{'key':'9f7bba2f-51df-48fc-9da4-9bf5da67b152'}}})

        res = es.search(index='acme',body={'query':{'match':{'_id':item['key']}}})
        cloud_logger.info(res)
        #print(res)
        if res['hits']['total']['value'] > 0:  # output each element
            for x in res['hits']['hits']:
                #print(x['_source'])
                entry = x['_source']
                entry['quantity'] += item['quantity']
                if entry['name'] != item['name']:
                    entry['name'] = item['name']
                if date > entry['last_received']:
                    entry['number_of_days_received'] += 1
                    entry['last_received'] = date
                res = es.index(index='acme',doc_type='inventory',id=item['key'],body=entry)
                #print(res)
        else:  # first time of item insert
            item['first_received'] = date
            item['last_received'] = date
            item['number_of_days_received'] = 1
            #print(item)
            #cloud_logger.info(item)
            res = es.index(index='acme',doc_type='inventory',id=item['key'],body=item)   # index name lower case
            #print(res)
            #cloud_logger.info(res)
            #res=es.get(index='acme',doc_type='inventory',id=item['key'])
            #cloud_logger.info(res)
            # print(res['_source'])            
        # res=es.delete(index='acme',doc_type='inventory',id=i)
        # print(res['result'])

def hello_pubsub(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    #print(event)
    inventory = json.loads(base64.b64decode(event['data']).decode('utf-8'))
    #print(inventory)
    days = 1
    start_offset=OFFSET
    begin = time.time()
    for day in range(days,0,-1):
        date = str(datetime.datetime.utcnow()-datetime.timedelta(days = start_offset)-datetime.timedelta(days = day)).split(' ')[0]   # date only
        if inventory:  
            updateInventory(items = inventory, date=date)
        time.sleep(0)  # loop call test ES will not optimize skipping query
    #print('Elapsed time: %d'%(time.time()-begin))
    #cloud_logger.info('Elapsed time: %d'%(time.time()-begin))

