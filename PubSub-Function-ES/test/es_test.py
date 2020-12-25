#!/usr/bin/python3
# usage: $ ./es_test.py -i <elastic_search's IP> -p 9200
import sys, argparse
from elasticsearch import Elasticsearch#, RequestsHttpConnection
import datetime, time
CUSTOMER = 'acme'

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", default="localhost")   
    parser.add_argument("-p", "--port", default="9200")
    parser.add_argument("-s", "--size", default="100")
    parser.add_argument("-k", "--key", default="")
    parser.add_argument("-n", "--count", default=False)
    parser.add_argument("-c", "--clean", default=False)
    args = parser.parse_args()

    esinfo = {}
    esendpoint = args.ip
    es = Elasticsearch(
        [{'host':esendpoint,'port':int(args.port)}],
        # hosts=[{'host': esendpoint, 'port': 443}],
        # http_auth=awsauth,
        # use_ssl=True,
        # verify_certs=True,
        # ca_certs=certifi.where(),
        # connection_class=RequestsHttpConnection
    )
    # esinfo = es.info()
    #print(esinfo)
    if args.clean:
        res = es.delete_by_query(index=CUSTOMER, body={"query": {"match_all": {}}})
        print(res)
        return
    elif args.count:
        print(args.count)
        res= es.search(index=CUSTOMER,body={'query':{'match_all':{}}},size=0)
        print(res['hits']['total']['value'])
    elif args.key and len(args.key) > 0:
    	res= es.search(index=CUSTOMER,body={'query':{'match':{'_id':args.key}}})
    	if res['hits']['total']['value'] > 0:  # output each element
            for x in res['hits']['hits']:
                print(x['_source'])
    else:
        res= es.search(index=CUSTOMER,body={'query':{'match_all':{}}},size=int(args.size))
        if res['hits']['total']['value'] > 0:  # output each element
            for x in res['hits']['hits']:
                print(x['_source'])

if __name__ == '__main__':
    main(sys.argv)
