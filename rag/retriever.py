import ollama
import chromadb


from config import (
    CHROMA_PATH,
    COLLECTION_NAME,
    EMBED_MODEL,
    TOP_K,
    
)



class Retriever:
    def __init__(self):
        self.client = (
            chromadb.PersistentClient(
                path=str(CHROMA_PATH)
            )
        )

        try:

            self.collection = (
                self.client.get_collection(
                    name=COLLECTION_NAME
                )
            )
        
        except Exception:
            raise RuntimeError(
                "RAG collection belum ada. "
                "Jalankan: "
                "python -m rag.index_knowledge"
            )
    
    def search(
        self,
        query,
        top_k=TOP_K
    ):

        response = ollama.embed(
            model=EMBED_MODEL,
            input=query
        )

        embedding = (
            response.embeddings[0]
        )

        results = self.collection.query(
            query_embeddings=[
                embedding
            ],

            n_results=top_k,

            include=[
                "documents",
                "metadatas",
                "distances"
            ]
        )

        hits = []

        documents = (
            results["documents"][0]
        )

        metadatas = (
            results["metadatas"][0]
        )

        distances = (
            results["distances"][0]
        )

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances
        ):
            hits.append({
                "context": document,
                "metadata": metadata,
                "distance": distance
            })

       

        return hits