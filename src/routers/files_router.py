import inject as inject
from boto3.exceptions import S3UploadFailedError
from fastapi import (APIRouter, Body, Depends, File, Query, Security,
                     UploadFile)
from fastapi.responses import ORJSONResponse
from fastapi_jwt import JwtAuthorizationCredentials
from starlette import status

from exceptions import ObjectNotFoundException
from models.dto.files import FileResponse, MultipleFilesResponse
from services.files_service import FilesService
from utils.exceptions_handler import ErrorResponse, mapping_to_doc
from utils.jwt_helper import access_security, credentials_exception

router = APIRouter(prefix="/files")


async def get_files_service() -> FilesService:
    return inject.instance(FilesService)


exceptions_map = {
    ObjectNotFoundException: ErrorResponse(
        status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
    ),
    S3UploadFailedError: ErrorResponse(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Upload failed"
    ),
}


@router.get(
    "",
    response_model=MultipleFilesResponse,
    responses=mapping_to_doc(exceptions_map),
)
async def get_files(
    limit: int = Query(default=40, gt=0, le=100),
    offset: int = Query(default=0, ge=0, le=2**32 - 1),
    service: FilesService = Depends(get_files_service),
    credentials: JwtAuthorizationCredentials = Security(access_security),
) -> ORJSONResponse:
    if not credentials:
        raise credentials_exception
    user_id = credentials.subject["id"]
    files = await service.get_list(user_id=user_id, limit=limit, offset=offset)
    return ORJSONResponse(
        status_code=status.HTTP_200_OK,
        content=MultipleFilesResponse.from_entity_list(user_id, files),
    )


@router.post("/upload", responses=mapping_to_doc(exceptions_map))
async def upload_file(
    path: str = Body(),
    file: UploadFile = File(...),
    service: FilesService = Depends(get_files_service),
    credentials: JwtAuthorizationCredentials = Security(access_security),
) -> ORJSONResponse:
    if not credentials:
        raise credentials_exception
    user_id = credentials.subject["id"]

    file = await service.upload_file(user_id=user_id, path=path, file=file)
    return ORJSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=FileResponse.from_entity(file),
    )


@router.post(
    "/check-access/{file_path}", responses=mapping_to_doc(exceptions_map)
)
async def check_file_access(
    file_path: str,
    credentials: JwtAuthorizationCredentials = Security(access_security),
    service: FilesService = Depends(get_files_service),
):
    """Route for nginx auth_request"""
    if not credentials:
        return ORJSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=None)

    user_id = credentials.subject["id"]
    if not await service.check_file_access(user_id, file_path):
        return ORJSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=None)

    return ORJSONResponse(status_code=status.HTTP_200_OK, content=None)
