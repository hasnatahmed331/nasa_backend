
from qdrant_client import models
from django.conf import settings
from qdrant_client import models





def create(context):
    name = context['name']
    
    if name == 'user':

        id = context['id']
        bio = context['bio']
        already = context['already']
        
        vector = settings.ENCODER.encode(bio).tolist()

      

        if not already:
            settings.QDRANT_CLIENT.upsert(
                collection_name='user', 
                points= [
                    models.PointStruct(
                    id=int(id),
                    vector=vector,
                ),

                ]
            )

        else:
            settings.QDRANT_CLIENT.update(
                collection_name='user', 
                points= [
                    models.PointStruct(
                    id=int(id),
                    vector=vector,
                ),

                ]
            )

    elif name == 'project':
        id = context['id']
        description = context['description']
        already = context['already']
        vector = settings.ENCODER.encode(description).tolist()
        if already:
            settings.QDRANT_CLIENT.update(
                collection_name='project', 
                points= [
                    models.PointStruct(
                    id=int(id),
                    vector=vector,
                ),

                ]
            )
        
        else:
            settings.QDRANT_CLIENT.upsert(
                collection_name='project', 
                points= [
                    models.PointStruct(
                    id=int(id),
                    vector=vector,
                ),

                ]
            )


   
    









# doc = ['this project is related to python' , 'this project is related to HTML']
# doc_embeddings = settings.encoder.encode(doc)

# qdrant_client.delete_collection(collection_name="test_collection")
# qdrant_client.create_collection(collection_name="user" ,   
#                                 vectors_config=models.VectorParams(
#                                 size= encoder.get_sentence_embedding_dimension(),
#                                 distance=models.Distance.COSINE,
#                             ) )
# qdrant_client.create_collection(collection_name="project" , 
#                                 vectors_config=models.VectorParams(
#                                 size= encoder.get_sentence_embedding_dimension(),
#                                 distance=models.Distance.COSINE,
#                                 ))
# print(qdrant_client.get_collections())
# qdrant_client.close()
# settings.qdrant_client.upsert(
#     collection_name="test_collection",
#     points = models.Batch(
#         ids = [1,2],
#         vectors=doc_embeddings.tolist() 
#     )
# )

# ques = "my experties are in python"

# ques_embedding = settings.encoder.encode(ques)

# hits = settings.qdrant_client.search(
#     collection_name="test_collection",
#     query_vector=ques_embedding.tolist(),
#     limit=2,

# )
# print(hits)

# settings.qdrant_client.close()
# qdrant_client.create_collection(collection_name="test_collection",
#                             vectors_config=models.VectorParams(
#                                 size= encoder.get_sentence_embedding_dimension(),
#                                 distance=models.Distance.COSINE,
#                             ))

