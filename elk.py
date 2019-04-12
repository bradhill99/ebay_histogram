import requests
import json
import sys

'''
Index json files into elasticsearch
Usage elk.py json_file
'''
if __name__ == "__main__":
    try:
        with open(sys.argv[1]) as fp:
            for line in fp.readlines():
                r = requests.post(
                    'http://localhost:9200/ebay_hist/_doc/',
                    headers={
                        "Content-Type": "application/json"
                    },
                    data=line.strip()
                )
                print("index result:{}".format(r.text))
    finally:
        fp.close()
