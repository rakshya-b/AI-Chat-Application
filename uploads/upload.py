from fastapi import APIRouter, UploadFile,File,HTTPException
import logging 
import os




logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
)

router = APIRouter(
    prefix="/upload",
    tags=["Upload"])


ALLOWED_TYPES = {"application/pdf","application/msword","application/vnd.openxmlformats-officedocument.wordprocessingml.document"}


@router.post("/")
async def  upload_document(file:UploadFile = File( ) ):
    """This is a function to upload the pdf """


    if file.content_type not in ALLOWED_TYPES :

        logger.warning (
            f" Invalid file type:{file.filename}"
        )

        raise HTTPException(status_code = 400,
                            detail = "Only PDF, DOC  and DOCX files are allowed"
                            )
    contents = await file.read()

    logger.info(f" File read successfully : {file.filename}")


    return {
        "message": "File uploaded successfully",
        "filename": file.filename
    }

