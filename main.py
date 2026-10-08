from fastapi import FastAPI

from uploads.upload import router as upload_router
from markdown.markdown import router as markdown_router
from chunk.chunk import router as chunk_router
from query.query import router as query_router


app = FastAPI(
    title="Hybrid RAG System",
    description="Document Upload, Conversion, Chunking, Embedding and Query System",
    version="1.0"
)


app.include_router(upload_router)
app.include_router(markdown_router)
app.include_router(chunk_router)
app.include_router(query_router)