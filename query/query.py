from fastapi import Query, APIRouter
import logging 
logger =  logging.getLogger(__name__)
import ollama 
from main import collection,embedding_model,app



router = APIRouter(
    prefix="/query",
    tags=["Chunking & Embedding"]
)

@app.post("/query")
async def query_documents(query: str = Query(...)):

    logger.info(f"Received query: {query}")

    query_embedding = embedding_model.encode(
        query,
        normalize_embeddings=True
    )

    logger.info("Query embedding created successfully")
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=5
    )

    logger.info("Relevant chunks retrieved from ChromaDB")
    documents = results["documents"][0]
    context = "\n\n".join(documents)
    logger.info("context created successfully")
    prompt = f"""
You are a helpful assistant.

Answer the user's question using ONLY the information
provided in the context.

If the answer is not available in the context,
say that you don't know.

Context:
{context}

Question:
{query}

Answer:
"""
    response = ollama.chat(
        model = "gemma4:latest",
        messages = [{
            "role":"user",
            "content": prompt
        }]
    )
    answer = response["message"]["content"]
    logger.info("LLM generated successfully")
    return {
        "query": query,
        "answer": answer,
        "retrieved_chunks": documents
    }