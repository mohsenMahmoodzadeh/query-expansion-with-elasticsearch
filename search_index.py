import nltk
import json
from elasticsearch import Elasticsearch
from nltk.corpus import wordnet
from nltk.tokenize import  word_tokenize
from nltk.corpus import stopwords


installation_dir = nltk.find('corpora/wordnet')
if installation_dir:
    print('Wordnet is already installed in ' + str(installation_dir))
else:
    nltk.download('wordnet')

elastic_host = {
    "host": "localhost", 
    "port": 9200
    }

index = 'facts-index'

es = Elasticsearch(hosts=[elastic_host])

def expand(query):
    query = query.lower()
    
    tokens = word_tokenize(query)
    query_string = ""
    num_tokens = 0
    
    for token in tokens:
        synonyms = []
        synset_array = wordnet.synsets(token)
        for syn in synset_array:
            for l in syn.lemmas():
                if l.name() not in synonyms:
                    synonyms.append(l.name())
                    
        if(len(synset_array) == 0):
            synonyms.append(token)
        
        query_string += '(' + ' OR '.join(synonyms) + ')'
        num_tokens += 1
        
        if (num_tokens < len(tokens)):
            query_string = query_string + ' AND '
        
    print(query, '\n*******************\n', query_string)
    
    return query_string

def search(query):
    result = es.search(
        index=index,
        body={
            "query": {
                "query_string": {
                    "fields": ["title", "url", "date_published", "rating", "author_name", "category", "tags", "claim", "content"],
                    "query": query
                }
            }
        }
    )
    
    return result

def write(path, query, result):
    if(not path.endswith("/")):
        path+="/"
    
    path += query + ".txt"
    print(path)
    dst_file = open(path, 'w')
    dst_file.write(result)
    dst_file.close()

def query(simple_query):
    simple_search_results = search(simple_query)
    path = '../simple_queries/'
    write(path, 
        simple_query, 
        json.dumps(
            {
                "max_score": simple_search_results['hits']['max_score'],
                "hits": simple_search_results['hits']['hits']
            }, 
            indent=1
        )
    )
    
    expanded_query = expand(simple_query)
    expanded_search_result = search(expanded_query)
    path = '../extended_queries/'
    write(
        path, 
        simple_query, 
        json.dumps(
            {
                "max_score": expanded_search_result['hits']['max_score'],
                "hits": expanded_search_result['hits']['hits']
            }, 
            indent=1
        )
    )