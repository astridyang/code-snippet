tests/test_function_app.py
import pytest
from unittest.mock import patch, MagicMock
import azure.functions as func
from your_module import queue_trigger  # 替换为实际模块名

# ... existing tests ...

def test_queue_trigger():
    # 创建一个模拟的QueueMessage
    mock_msg = MagicMock(spec=func.QueueMessage)
    mock_msg.get_body.return_value = b'test_document_link'

    with patch('your_module.blob.BlobServiceClient') as mock_blob_service, \
         patch('your_module.cosmos.CosmosClient') as mock_cosmos_client, \
         patch('your_module.create_index_from_file') as mock_create_index:

        # 设置Blob和CosmosDB的返回值
        mock_blob_client = MagicMock()
        mock_blob_service.return_value.get_blob_client.return_value = mock_blob_client
        mock_blob_client.download_blob.return_value.readall.return_value = b'test file content'
        
        mock_create_index.return_value = {'index': 'test_index'}

        mock_container = MagicMock()
        mock_cosmos_client.return_value.get_database_client.return_value.get_container_client.return_value = mock_container

        # 调用queue_trigger函数
        queue_trigger(mock_msg)

        # 断言Blob存储和CosmosDB的调用
        mock_blob_service.assert_called_once_with("your_blob_connection_string")
        mock_blob_client.download_blob.assert_called_once()
        mock_create_index.assert_called_once_with("downloaded_file")
        mock_container.upsert_item.assert_called_once_with({'index': 'test_index'})

# ... existing tests ...