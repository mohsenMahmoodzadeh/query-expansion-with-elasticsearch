# Query Expansion with Elasticsearch & NLTK
This project is developed in Python + NLTK + Elasticsearch for query expansion over a data. the data crawled from [Snopes Fact checks](https://www.snopes.com/fact-check/) and the designed crawler and its implementation is accessible from this [repository](https://github.com/mohsenMahmoodzadeh/Fact-Checks-Crawler). 

[Snopes Fact checks](https://www.snopes.com/fact-check/) contains some rumors and questionable claims of the day. After gathering data via the crawler, it's time to index the data into a search engine to use it for retrieving the information. We use Elasticsearch which has a big community and also uses the power of [Apache Lucene](https://lucene.apache.org/) indexing & search tool.

We use query expansion, a technique for improving the quality of search results in a search engine and get help from [wordnet](https://wordnet.princeton.edu/) database to find semantic relations between words. For simplifying the usage from wordnet and also tokenizing the queries and other preprocessings, we use [NLTK](https://www.nltk.org/) python module. 

The general idea behind query expansion is that for every token in the query, the sysnonyms are conjuncted with OR and the results are conjuncted with AND operator.

## Environment
- Python: 3.7.0
- Elasticsearch: 7.16.0
- NLTK: 3.6.7

## Installation Guide
Clone the repository:
```
git clone https://github.com/mohsenMahmoodzadeh/query-expansion-with-Elasticsearch.git
```

Create a virtual environement (to avoid conflicts):
```
virtualenv -p python3.7 fcquery

# this may vary depending on your shell
. fcquery/bin/activate 
```

Install the dependencies:
```
pip install -r requirements.txt
```
The dataset is accsessible from [here](https://drive.google.com/file/d/1QO3-UxU3Fpgvn7Vjl-dV5SvkMllIugYZ/view?usp=sharing). Put it on the root directory of your project.


## Usage Guide

First of all, download the elasticsearch configuration from [here](https://www.elastic.co/downloads/elasticsearch) and run it according to the installation guide of the website.

After setting up elasticsearch service, run the following command to index the data into elasticsearch engine:
```
python create_index.py
```

After the completion of the indexing phase, run the script below to query on the data, expand the queries and save the results into `result/` directory.
```
python search_index.py
```

## Future Works

- Preprocess the data to be prepared for analyzing. This can contain some tasks such as encoding, setting lowercase, converting to numeric, etc.

- Analyze the data with applying DSL queries and creating dashboards.

## Contributing
Fixes and improvements are more than welcome, so raise an issue or send a PR!