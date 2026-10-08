from fastapi import APIRouter, UploadFile, File, HTTPException
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from database.chroma import collection
import logging

logger = logging.getLogger(__name__)


# -----------------------------
# Router
# -----------------------------

router = APIRouter(prefix="/chunks", tags=["Chunking & Embedding"])


# -----------------------------


# -----------------------------
# Embedding Model
# -----------------------------

embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


# -----------------------------
# Create Chunks
# -----------------------------


@router.post("/create")
async def create_chunks(file: UploadFile = File(...)):
    """
    Upload a Markdown file, split it into chunks,
    generate embeddings and store them in ChromaDB.
    """

    # -------------------------
    # Check file type
    # -------------------------

    if file.content_type not in ["text/markdown", "text/plain"]:

        logger.warning(f"Invalid markdown file: {file.filename}")

        raise HTTPException(status_code=400, detail="Only Markdown files are allowed")

    # -------------------------
    # Read Markdown file
    # -------------------------

    markdown_text = await file.read()

    markdown_text = markdown_text.decode("utf-8")

    logger.info(f"Markdown file read successfully: {file.filename}")

    # -------------------------
    # Create Text Splitter
    # -------------------------

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    logger.info("Recursive text splitter created")

    # -------------------------
    # Create Chunks
    # -------------------------

    chunks = text_splitter.split_text(markdown_text)

    logger.info(f"{file.filename} converted into " f"{len(chunks)} chunks")

    # -------------------------
    # Create Embeddings
    # -------------------------

    embeddings = embedding_model.encode(chunks, normalize_embeddings=True)

    logger.info(f"Embeddings created successfully for " f"{len(chunks)} chunks")

    # -------------------------
    # Create IDs
    # -------------------------

    ids = [f"{file.filename}_chunk_{i}" for i in range(len(chunks))]

    # -------------------------
    # Create Metadata
    # -------------------------

    metadatas = [{"filename": file.filename, "chunk_id": i} for i in range(len(chunks))]

    # -------------------------
    # Store in ChromaDB
    # -------------------------

    collection.add(
        ids=ids, documents=chunks, embeddings=embeddings.tolist(), metadatas=metadatas
    )

    logger.info(f"{len(chunks)} chunks stored in ChromaDB")

    # -------------------------
    # Response
    # -------------------------

    return {
        "message": "Markdown chunked and embedded successfully",
        "filename": file.filename,
        "total_chunks": len(chunks),
        "chunks": chunks,
        "embeddings": embeddings.tolist(),
    }
