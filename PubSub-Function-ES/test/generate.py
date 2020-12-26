#!/usr/bin/python3
# usage: $ ./generate.py -f <jsonfile> -r 1000000
import sys, argparse
import os
import uuid, gzip, json

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", default="INVENTORY")
    parser.add_argument("-c", "--customer", default="acme")
    parser.add_argument("-r", "--rec", default="1000")
    args = parser.parse_args()

    # INVENTORY - generate
    filename = args.file+'.json.gz'
    N = int(args.rec)
    with gzip.GzipFile(filename, 'w') as fout:		# write back as json.gz
        L = []
        for i in range(N+1):
            data = {}
            data['key'] = str(uuid.uuid4())
            data['name'] = 'item '+str(i)
            data['quantity'] = i
            L.append(data)
        fout.write(json.dumps(L).encode('utf-8'))  

if __name__ == '__main__':
    main(sys.argv)

