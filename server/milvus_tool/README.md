# README

Milvus is an open source feature vector similarity search engine. This tool is based on Milvus' implementation of vector storage and recall services. You can use this tool in the recall process in the recommendation system.

For Milvus tutorial, please refer to the official website: https://milvus.io/cn/

Milvus source code details refer to: https://github.com/milvus-io/milvus

## Table of Contents

The following is a brief directory structure and description of this tool:

```
├── readme.md #Introduction document
├── config.py #Parameter configuration
├── milvus_insert.py #vector insert script
├── milvus_recall.py #vector recall script
```

## Environmental requirements

**operating system**

CentOS: 7.5 or above

Ubuntu LTS: 18.04 or above

**hardware**

cpu: Intel CPU Sandy Bridge or above

> The CPU is required to support at least one of the following instruction sets: SSE42, AVX, AVX2, AVX512

Memory: 8GB or more (depending on the specific vector data size)

**software**

Python version: 3.6 and above

Docker: 19.03 or above

Milvus 2.0.0



## Install and start Milvus

Here will install standalone [Milvus2.0.0 Standalone](https://milvus.io/docs/v2.0.0/install_standalone-docker.md), or you can choose to install distributed Milvus2.0, please refer to the installation method: [Milvus2. 0.0 Cluster](https://milvus.io/docs/v2.0.0/install_cluster-docker.md).

**Install Milvus Python SDK**

```shell
$ pip install pymilvus-orm==2.0.0rc5
```



## Instructions for use

The script in this tool provides two functions: vector insertion and vector recall. Before using the script of the tool, you need to modify the configuration file `config.py` of the tool according to the environment:

| Parameters | Description | Reference value |
| ---------------- | -------------------------------- ---------------------------- | --------------------- --------------------------------------- |
| MILVUS_HOST | IP of the machine where the Milvus service is located | localhost |
| MILVUS_PORT | Port providing Milvus service | 19530 |
| schema | Set parameters established in Milvus. <br />`fields`<br />`description` description of the collection<br />`dim` vector dimension | dim = 32<br /> pk = FieldSchema(name='pk', dtype=DataType.INT64 , is_primary=True)<br /> field = FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR, dim=dim)<br /> schema = CollectionSchema(fields=[pk, field], description="movie recommendation : demo films") |
| index_param | Parameters for indexing, different indexes require different parameters | {<br /> "metric_type": "L2",<br /> "index_type":"IVF_FLAT",<br /> "params":{ "nlist":128}<br />} |
| top_k | The number of vectors recalled when querying. | 10 |
| search_params | Parameters when querying in Milvus, this parameter will image query performance and recall rate | {<br /> "metric_type": "L2",<br /> "params": {"nprobe": 10}< br /> }|

### Vector import

The Milvus_insert.py script provides vector import function. Before using the script, you need to modify the corresponding parameters in config.py. The calling method is as follows:

```python
from milvus_tool.milvus_insert import VecToMilvus

client = VecToMilvus()
mr = client.insert(ids=ids, vectors=embeddings, collection_name=collection_name, partition_name=partition_name)
```

> The parameters that need to be passed in when calling the insert method:
>
> **collection_name**: Insert the vector into the name of the collection in Milvus. Before importing data, the script will check whether the collection exists in the library. If it does not exist, it will create a new collection according to the collection parameters set in `config.py`.
>
> **vectors**: Insert the vectors in the Milvus collection. What is required here is that the vector format is in the form of a two-dimensional list, for example: [[2.1, 3.2, 10.3, 5.5], [3.3, 4.2, 6.5, 6.3]], here means to insert two vectors of dimension four.
>
> **ids**: ID corresponding to the vector one-to-one. The ids required here is in the form of a one-dimensional list. Example: [1,2], which means that the IDs corresponding to the above two vectors are 1 and 2. Here The ids can also be empty and no parameters are passed in. At this time, the inserted vector will be automatically assigned an ID by Milvus.
>
> **partition_name**: Specify the name of the partition to be inserted into the vector. In Milvus, a set can be divided into several partitions by label. This parameter can be empty. When it is empty, the vector is inserted directly into the collection.

**Return result**: After the vector is imported, it will return MutationResult `mr`, which contains the primary key column primary_keys: `mr.primary_keys` corresponding to the inserted data.

For specific use, please refer to the project movie_recommender/to_milvus.py

### Vector recall

milvus_recall.py provides vector recall function. Before using this script, you need to modify the corresponding parameters in config.py. The calling method is as follows:

```python
from milvus_tool.milvus_recall import RecallByMilvus
milvus_client = RecallByMilvus()
res = milvus_client.search(collection_name=collection_name, vectors=embeddings)
```

> **collection_name**: Specify the name of the collection to be queried.
>
> **vectors**: Specify the vector to be queried. The vector format is the same as the vector format when inserting, which is a two-dimensional list.
>

**Return result**: The search result res will be returned including ID and distance:

```
for x in res:
    for y in x:
        print(y.id, y.distance)
OR
for x in res:
    print(x.ids, x.distances)
```

For specific use, please refer to the project movie_recommender/recall.py