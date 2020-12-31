import uuid

def bulk_json_data(json_data, _index, doc_type):
    for doc in json_data:
    # use a `yield` generator so that the data
    # isn't loaded into memory
        if '{"index"' not in doc:
            yield {
                "_index": _index,
                "_type": doc_type,
                "_id": uuid.uuid4(),
                "_source": doc
            }
