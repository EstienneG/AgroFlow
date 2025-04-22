from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import os

import pickle

from pathlib import Path
from rank_bm25 import BM25Okapi
import nltk


def initialize_qdrant() -> QdrantClient:
    """
    Initialize Qdrant vector database client and load document embeddings.
    
    Returns:
        QdrantClient: Initialized Qdrant client
    """
    # Create Qdrant client - using :memory: for testing, but in production should use a persistent storage
    qdrant_client = QdrantClient(":memory:")
    
    # Load document embeddings if the pickle file exists
    embeddings_file = os.path.join("..", "RAG", "document_embeddings.pkl")
    if os.path.exists(embeddings_file):
        try:
            with open(embeddings_file, "rb") as f:
                document_embeddings = pickle.load(f)
                
            # Create collections for different document types if they don't exist
            collection_name = "technical_reports"
            # Check if collection exists
            try:
                qdrant_client.get_collection(collection_name=collection_name)
            except Exception:
                # Create collection if it doesn't exist
                qdrant_client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(size=1024, distance=Distance.COSINE)
                )
            
            # Process tabular structured embeddings and create points for Qdrant
            collection_points = []
            
            # Format of embeddings_file: id  vector  payload
            # Where id column contains UUIDs that should be used as Qdrant IDs
            for _, row in document_embeddings.iterrows():
                try:
                    # Extract UUID from the id column to use as the actual Qdrant ID
                    point_id = row['id']
                    vector = row['vector']
                    payload = row['payload']
                    
                    collection_points.append(
                        PointStruct(
                            id=point_id,
                            vector=vector,
                            payload=payload
                        )
                    )
                except Exception as e:
                    print(f"Error processing embedding row: {e}")
                    continue
                
                # Only upsert if there are points for this collection
                if collection_points:
                    qdrant_client.upsert(
                        collection_name=collection_name,
                        points=collection_points
                    )

            print(f"Loaded {len(collection_points)} document embeddings for {collection_name}")
            print("Document embeddings loaded successfully")
            
        except Exception as e:
            print(f"Error loading document embeddings: {str(e)}")
    else:
        print(f"Document embeddings file not found at {embeddings_file}")
    
    return qdrant_client


def initialize_bm25() -> BM25Okapi:
    input_dir = Path("../../data/md/technical_reports")
    output_dir = Path("../../data/txt/technical_reports")
    output_dir.mkdir(parents=True, exist_ok=True)

    for md_file in input_dir.glob("*.md"):
        with open(md_file, "r", encoding="utf-8") as f_in:
            content = f_in.read()
        txt_file = output_dir / (md_file.stem + ".txt")
        with open(txt_file, "w", encoding="utf-8") as f_out:
            f_out.write(content)


    nltk.download("punkt")

    input_dir = "../../data/txt/technical_reports"

    documents = []
    filenames = []

    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            with open(os.path.join(input_dir, filename), "r", encoding="utf-8") as f:
                text = f.read()
                documents.append(text)
                filenames.append(filename)

    tokenized_docs = [nltk.word_tokenize(doc.lower()) for doc in documents]

    return BM25Okapi(tokenized_docs)