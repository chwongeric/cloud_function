#!/usr/bin/python3
# usage: $ ./es_test1.py -i <elastic_search's IP> -p 9200
import sys, argparse
import os

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", default="INVENTORY.json")
    parser.add_argument("-c", "--chunks", default="10") 
    parser.add_argument("-s", "--size", default="100")
    parser.add_argument("-p", "--project", default="abc")
    parser.add_argument("-t", "--topic", default="inventory")
    args = parser.parse_args()

    # INVENTORY - partition
    sz = int(args.size)
    N = int(args.chunks)
    topic = "projects/"+args.project+"/topics/"+args.topic
    for i in range(N):
        chunk = '.[%d:%d]'%(i*sz,(i+1)*sz)
        CMD = '"$(jq -c %s %s | cat)"'%("\'"+chunk+"\'",args.file)
        PUB_CMD = 'gcloud pubsub topics publish %s --message %s'%(topic,CMD)
        os.system(PUB_CMD)

if __name__ == '__main__':
    main(sys.argv)
