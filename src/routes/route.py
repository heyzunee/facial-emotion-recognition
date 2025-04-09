import logging
import shutil
import tempfile
from typing import Any, List, Optional

from fastapi import APIRouter, File, HTTPException, Request, UploadFile
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse

from ..config import *
from ..module.detector import FaceEmotionRecognition
from ..schemas import output

logger = logging.getLogger(PROJECT_NAME)

api_router = APIRouter()
detector = FaceEmotionRecognition()


def success_response(response_data: Optional[Any] = None) -> JSONResponse:
    """
    Returns a JSON response with the given status code and the given data.
    :param response_data: The data to be returned.
    :return: A JSON response with the given status code and the given data.
    """
    if response_data is not None:
        response_json = jsonable_encoder(response_data)

    return JSONResponse(response_json, status_code=status.HTTP_200_OK)


def error_response(
    errors: Optional[Any] = None,
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
) -> JSONResponse:
    """
    Returns a JSON response with the given status code and the given errors.
    :param errors: The errors to be returned.
    :param status_code: The status code of the response.
    :return: A JSON response with the given status code and the given errors.
    """
    response_json = {}
    if errors is not None:
        response_json["errors"] = jsonable_encoder(errors)

    return JSONResponse(response_json, status_code=status_code)


@api_router.post("/emotion", response_model=output.EmotionListResponse)
async def emotion(request: Request, image: UploadFile = File(...)):
    try:
        form_data = await request.form()
        if len(form_data.getlist("image")) > 1:
            raise HTTPException(status_code=400, detail="Only one image file is allowed")

        if image.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(status_code=400, detail="File must be JPG or PNG")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            shutil.copyfileobj(image.file, tmp)
            tmp_path = tmp.name

        message, results = detector.detect_emotions(tmp_path)
        response = output.EmotionListResponse(**{"message": message, "results": results})

        return success_response(response)

    except Exception as e:
        logger.error(f"Failed to detect emotion: {str(e)}")
        return error_response(errors=str(e.detail), status_code=e.status_code)
