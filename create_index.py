from elasticsearch import Elasticsearch
import json

elastic_host = {
    "host": "localhost", 
    "port": 9200
    }

es = Elasticsearch(hosts=[elastic_host])

path = './prettified_facts.json'
mode = 'r'

f = open(path, mode= mode)
facts = json.load(f)
f.close()

id = 1
index = 'facts-index'
request_timeout = 45

print('Indexing started')
for fact in facts:
    print(f'indexing document {id} ...')
    es.index(
        index = index, 
        id = id, 
        document = fact, 
        request_timeout = request_timeout
        )
    id += 1

print('Indexing completed successfully.')