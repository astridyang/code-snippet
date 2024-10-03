tests/test_main.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app  # 替换为实际模块名

client = TestClient(app)

def test_upload_file_success():
    # 模拟JWT验证
    with patch('main.verify_jwt') as mock_verify_jwt, \
         patch('main.BlobServiceClient') as mock_blob_service, \
         patch('main.send_message_to_queue') as mock_send_message:

        mock_verify_jwt.return_value = {"sub": "test_user"}
        
        # 模拟Blob存储的行为
        mock_blob_client = MagicMock()
        mock_blob_service.return_value.get_blob_client.return_value = mock_blob_client
        
        # 模拟文件上传
        response = client.post(
            "/upload/",
            headers={"Authorization": "Bearer your_jwt_token"},
            files={"files": ("test_file.txt", b"这是一个测试文件的内容。")}
        )

        assert response.status_code == 200
        assert response.json() == {"filename": "test_file.txt", "url": "https://your_storage_account.blob.core.windows.net/your-container-name/test_file.txt"}
        mock_blob_client.upload_blob.assert_called_once()
        mock_send_message.assert_called_once()

def test_upload_file_no_file():
    # 模拟JWT验证
    with patch('main.verify_jwt') as mock_verify_jwt:
        mock_verify_jwt.return_value = {"sub": "test_user"}

        response = client.post(
            "/upload/",
            headers={"Authorization": "Bearer your_jwt_token"},
            files={}  # 不提供文件
        )

        assert response.status_code == 400
        assert response.json() == {"detail": "No file provided"}

# ... 其他测试 ...