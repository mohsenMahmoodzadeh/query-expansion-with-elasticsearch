import nltk
import json
from elasticsearch import Elasticsearch
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


installed_packages = 0
try:
    wordnet_dir = nltk.find('corpora/wordnet')
    print('Wordnet is already installed in ' + str(wordnet_dir))
    installed_packages += 1
    punkt_dir = nltk.find('tokenizers/punkt')
    print('Punkt is already installed in ' + str(punkt_dir))
    installed_packages += 1
    omw_dir = nltk.find('corpora/omw-1.4')
    print('Open Multilingual Wordnet(OMW) is already installed in ' + str(omw_dir))
    installed_packages += 1
    print()
except:
    print('One of these corporas and tokenizers were not installed:\n \t- corpora/wordnet\n \t- corpora/omw-1.4\n \t- tokenizers/punkt')
    print()
    print('Installing required packages...')
    if installed_packages == 0:
        print('Installing corpora/wordnet...')
        nltk.download('wordnet')
        print('corpora/wordnet installed successfully')
        print()
        print('Installing tokenizers/punkt...')
        nltk.download('punkt')
        print('tokenizers/punkt installed successfully')
        print()
        print('Installing corpora/omw-1.4...')
        nltk.download('omw-1.4')
        print('corpora/omw-1.4 installed successfully')
    elif installed_packages == 1:
        print('Installing tokenizers/punkt...')
        nltk.download('punkt')
        print('tokenizers/punkt installed successfully')
        print()
        print('Installing corpora/omw-1.4...')
        nltk.download('omw-1.4')
        print('corpora/omw-1.4 installed successfully')
    else:
        print('Installing corpora/omw-1.4...')
        nltk.download('omw-1.4')
        print('corpora/omw-1.4 installed successfully')

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
    path = './result/simple_queries/'
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
    path = './result/expanded_queries/'
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

if __name__ == '__main__':
    path = './simple_queries.txt'
    simple_queries_file = open(path, 'r')
    lines = simple_queries_file.readlines()
    simple_queries_file.close()
    simple_queries = []
    
    for line in lines:
        line = line.replace('\n', '')
        line = line.replace('"', '')
        q = line.split('=')[1]
        q = q[1: len(q)]
        simple_queries.append(q)
    
    for q in simple_queries:
        query(q)