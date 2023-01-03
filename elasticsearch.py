import csv
import pandas

from elasticsearch import helpers, Elasticsearch

# setting up a connection to the localhost
elasticsearch = Elasticsearch([{'host': 'localhost', 'port': 9200}])


def elastic():
    # the main function that calls other functions
    my_index = "movies"

    # closing index after creating in order to create and update analyzer
    elasticsearch.indices.create(my_index)
    elasticsearch.indices.close(my_index)

    splitter(my_index)
    mapping(my_index)

    # opening the index to be able to upload
    elasticsearch.indices.open(index=my_index)
    upload(my_index)


def upload(my_index):
    # outputting a new csv file after formatting before uploading to Elasticsearch
    csv_name = "wiki_movie_plots_deduped.csv"
    sample_size = 1000
    index_name = my_index
    sample = "sample.csv"

    csv_file = pandas.read_csv(csv_name)
    formatted_csv = csv_file.iloc[:sample_size]
    formatted_csv.to_csv(sample, index=False)

    with open(sample, 'r') as outfile:
        helpers.bulk(elasticsearch, csv.DictReader(outfile), index=index_name)


def splitter(my_index):
    elasticsearch.indices.put_settings(
        index=my_index, body={
            "analysis": {
                "analyzer": {
                    "my_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": ["lowercase",
                                   "stop",
                                   "unique",
                                   "stemmer",
                                   ]
                    }
                }
            }
        }
    )


def mapping(my_index):
    elasticsearch.indices.put_mapping(
        index=my_index, body={
            "properties": {
                "Title": {
                    "type": "text",
                    "analyzer": "my_analyzer",
                },
                "Release Year": {
                    "type": "text",
                    "analyzer": "my_analyzer",
                },
                "Plot": {
                    "type": "text",
                    "analyzer": "my_analyzer",
                }
            }
        }
    )


# Call to the function to start indexing
elastic()
