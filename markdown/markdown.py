from fastapi import APIRouter, UploadFile, File, HTTPException
import pymupdf4llm
import os


from fastapi import FastAPI

app = FastAPI(title="Hybrid RAG System")


@app.get("/")
async def home():
    return {"message": "Hello"}


import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/markdown", tags=["Markdown Conversion"])


@router.post("/convert")
async def convert_to_markdown(file: UploadFile = File(...)):
    """Upload PDF and convert it to Markdown."""

    # Check file type
    if file.content_type != "application/pdf":

        logger.warning(f"Non-PDF file rejected: {file.filename}")

        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    # Read uploaded file
    contents = await file.read()

    logger.info(f"PDF file read successfully: {file.filename}")

    # Create uploads folder if it doesn't exist
    os.makedirs("uploads", exist_ok=True)

    # Create PDF path
    pdf_path = f"uploads/{file.filename}"

    logger.info(f"PDF path created: {pdf_path}")

    # Save PDF
    with open(pdf_path, "wb") as f:
        f.write(contents)

    logger.info("PDF to Markdown conversion started")

    # Convert PDF to Markdown
    markdown = pymupdf4llm.to_markdown(pdf_path)

    logger.info("PDF to Markdown conversion completed")

    # Create Markdown filename
    markdown_filename = os.path.splitext(file.filename)[0] + ".md"

    logger.info(f"Markdown filename created: {markdown_filename}")

    # Save Markdown file
    markdown_path = f"uploads/{markdown_filename}"

    with open(markdown_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    logger.info(f"Markdown conversion finished: {file.filename}")

    return {
        "message": "PDF converted to Markdown successfully",
        "pdf_filename": file.filename,
        "markdown_filename": markdown_filename,
        "markdown": markdown,
    }
