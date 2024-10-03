main.py
from fastapi import FastAPI, UploadFile, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from azure.storage.blob import BlobServiceClient
import jwt
import logging

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# JWT 验证函数
def verify_jwt(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, "your_secret_key", algorithms=["HS256"])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid JWT token")

@app.post("/upload/")
async def upload_file(files: UploadFile = None, token: str = Depends(verify_jwt)):
    if files is None:
        raise HTTPException(status_code=400, detail="No file provided")

    try:
        # 第2步：上传文件到Azure Blob存储
        blob_service_client = BlobServiceClient.from_connection_string("your_blob_connection_string")
        blob_client = blob_service_client.get_blob_client(container="your-container-name", blob=files.filename)
        
        # 上传文件
        await blob_client.upload_blob(await files.read())

        # 第3步：发送消息到队列
        file_url = f"https://your_storage_account.blob.core.windows.net/your-container-name/{files.filename}"
        message = {"filename": files.filename, "url": file_url}
        # 假设有一个send_message_to_queue函数
        send_message_to_queue(message)

    except Exception as e:
        logging.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail="File upload failed")

    return {"filename": files.filename, "url": file_url}

# ... existing code ...