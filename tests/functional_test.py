import httpx
from starlette import status

from main import app


async def test_file_upload(authed_client: httpx.AsyncClient) -> None:
    file_data = {"path": "path/test.txt"}
    with open("tests/test.txt", "rb") as f:
        result = await authed_client.post(
            app.url_path_for("upload_file"),
            data=file_data,
            files={"file": ("test.txt", f)},
        )

    assert result.status_code == status.HTTP_201_CREATED

    result = await authed_client.get(app.url_path_for("get_files"))
    assert result.status_code == status.HTTP_200_OK
    assert len(result.json()["files"]) == 1
