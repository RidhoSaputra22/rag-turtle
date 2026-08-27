import json
import ollama
import chromadb

from config import (
    CHROMA_PATH,
    COLLECTION_NAME,
    KNOWLEDGE_PATH,
    EMBED_MODEL
)


def main():

    client = chromadb.PersistentClient(
        path=str(CHROMA_PATH)
    )

    # Rebuild collection
    try:
        client.delete_collection(
            COLLECTION_NAME
        )
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME
    )

    files = list(
        KNOWLEDGE_PATH.glob("*.json")
    )

    print(
        f"Found {len(files)} knowledge files."
    )

    for file in files:

        with file.open(
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        embedding_text = (
            data["embedding_text"]
        )

        response = ollama.embed(
            model=EMBED_MODEL,
            input=embedding_text
        )

        embedding = (
            response.embeddings[0]
        )

        collection.upsert(
            ids=[
                data["id"]
            ],

            embeddings=[
                embedding
            ],

            # What will be sent to LLM
            documents=[
                data["context"]
            ],

            metadatas=[
                {
                    "category": data[
                        "category"
                    ],

                    "source": file.name
                }
            ]
        )

        print(
            f"Indexed: {data['id']}"
        )

    print(
        f"\nTotal: {collection.count()}"
    )


if __name__ == "__main__":
    main()