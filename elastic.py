from elasticsearch import Elasticsearch

es_conn = None


def connect_elastic(ip, port):
    # Connect to an elasticsearch node with the given ip and port
    global es_conn

    es_conn = Elasticsearch([{"host": ip, "port": port}])
    if es_conn.ping():
        print("Connected to elasticsearch...")
    else:
        print("Elasticsearch connection error...")
    return es_conn


def create_qa_index():
    # Define the index mapping
    index_body = {
        "settings": {
            "number_of_shards": 8,
            "number_of_replicas": 1,
            "analysis": {
                "analyzer": {
                    "standard_analyzer": {"tokenizer": "standard"},
                    "ngram_analyzer": {"type": "custom", "tokenizer": "my_ngram"},
                    "korean_analyzer": {
                        "type": "custom",
                        "tokenizer": "nori_tokenizer",
                    },
                },
                "tokenizer": {
                    "my_ngram": {
                        "type": "ngram",
                        "min_gram": 2,
                        "max_gram": 2,
                        "token_chars": ["letter", "digit"],
                    },
                    "nori_user_dict": {
                        "type": "nori_tokenizer",
                        "decompound_mode": "mixed",
                    },
                },
            },
        },
        "mappings": {
            "properties": {
                "id": {"type": "long"},
                "document": {"type": "text", "analyzer": "ngram_analyzer"},
            }
        },
    }
    try:
        # Create the index if not exists
        if not es_conn.indices.exists("korea-qa"):
            # Ignore 400 means to ignore "Index Already Exist" error.
            es_conn.indices.create(
                index="korea-qa", body=index_body  # ignore=[400, 404]
            )
            print("Created Index -> korea-qa")
        else:
            print("Index korea-qa exists...")
    except Exception as ex:
        print(str(ex))


def insert_qa(body):
    if not es_conn.indices.exists("korea-qa"):
        create_qa_index()
    # Insert a record into the es index
    es_conn.index(index="korea-qa", body=body)
    # print("QA successfully inserted...")


def semantic_search(query_vec, thresh=1.2, top_n=10):
    # Retrieve top_n semantically similar records for the given query vector
    if not es_conn.indices.exists("korea-qa"):
        return "No records found"
    s_body = {
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'question_vec') + 1.0",
                    "params": {"query_vector": query_vec},
                },
            }
        }
    }
    # Semantic vector search with cosine similarity
    result = es_conn.search(index="korea-qa", body=s_body)
    total_match = len(result["hits"]["hits"])
    print("Total Matches: ", str(total_match))
    # print(result)
    data = []
    if total_match > 0:
        q_ids = []
        for hit in result["hits"]["hits"]:
            if (
                hit["_score"] > thresh
                and hit["_source"]["q_id"] not in q_ids
                and len(data) <= top_n
            ):
                print(
                    "--\nscore: {} \n question: {} \n answer: {}\n--".format(
                        hit["_score"],
                        hit["_source"]["question"],
                        hit["_source"]["answer"],
                    )
                )
                q_ids.append(hit["_source"]["q_id"])
                data.append(
                    {
                        "question": hit["_source"]["question"],
                        "answer": hit["_source"]["answer"],
                    }
                )
    return data


def keyword_search(query, thresh=1.2, top_n=10):
    # Retrieve top_n records using TF-IDF scoring for the given query vector
    if not es_conn.indices.exists("korea-qa"):
        return "No records found"
    k_body = {"query": {"match": {"question": query}}}

    # Keyword search
    result = es_conn.search(index="korea-qa", body=k_body)
    total_match = len(result["hits"]["hits"])
    print("Total Matches: ", str(total_match))
    # print(result)
    data = []
    if total_match > 0:
        q_ids = []
        for hit in result["hits"]["hits"]:
            if (
                hit["_score"] > thresh
                and hit["_source"]["q_id"] not in q_ids
                and len(data) <= top_n
            ):
                print(
                    "--\nscore: {} \n question: {} \n answer: {}\n--".format(
                        hit["_score"],
                        hit["_source"]["question"],
                        hit["_source"]["answer"],
                    )
                )
                q_ids.append(hit["_source"]["q_id"])
                data.append(
                    {
                        "question": hit["_source"]["question"],
                        "answer": hit["_source"]["answer"],
                    }
                )
    return data
