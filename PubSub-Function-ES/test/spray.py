#!/usr/bin/python3
# usage: $ ./es_test1.py -i <elastic_search's IP> -p 9200
import sys, argparse
import os
from google.cloud import pubsub_v1

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", default="INVENTORY.json")
    parser.add_argument("-c", "--chunks", default="10")
    parser.add_argument("-o", "--offset", default="0")
    parser.add_argument("-s", "--size", default="1500")
    parser.add_argument("-p", "--project", default="abc")
    parser.add_argument("-t", "--topic", default="inventory")
    args = parser.parse_args()

    # INVENTORY - partition
    sz = int(args.size)
    N = int(args.chunks)
    publisher = pubsub_v1.PublisherClient()
    topic = "projects/"+args.project+"/topics/"+args.topic
    for i in range(N):
        chunk = '.[%d:%d]'%((int(args.offset)+i)*sz,((int(args.offset)+i)+1)*sz)
        ''' # smaller chunk - limited by shell stack size
        CMD = '"$(jq -c %s %s | cat)"'%("\'"+chunk+"\'",args.file)
        PUB_CMD = 'gcloud pubsub topics publish %s --message %s'%(topic,CMD)
        os.system(PUB_CMD)
        '''
        tmp = 'tmp-'+args.offset
	CMD = "jq -c %s %s > %s"%("\'"+chunk+"\'",args.file,tmp)
        print(CMD)
        os.system(CMD)

        while not os.path.exists(tmp):
            time.sleep(0)

        if  os.path.exists(tmp):
            data = open(tmp).read()
            os.remove(tmp)
            res = publisher.publish(topic, data.encode("utf-8"))
            print(res.result(), res.exception())
        
if __name__ == '__main__':
    main(sys.argv)
