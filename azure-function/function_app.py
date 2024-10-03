import azure.storage.blob as blob
import azure.cosmos.cosmos_client as cosmos
import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
    
@app.function_name(name="queue_trigger")
@app.queue_trigger(queue_name="your-queue-name", connection="your-connection-string")
def queue_trigger(msg: func.QueueMessage) -> None:
    logging.info('Queue trigger function processed a message.')

    try:
        document_link = msg.get_body().decode('utf-8')
        
        # 第2步：从Blob存储下载文件
        blob_service_client = blob.BlobServiceClient.from_connection_string("your_blob_connection_string")
        blob_client = blob_service_client.get_blob_client(container="your-container-name", blob=document_link)
        with open("downloaded_file", "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())

        # 第3步：使用下载的流创建索引
        # 假设使用e5创建索引的代码在这里
        index = create_index_from_file("downloaded_file")

        # 第4步：将索引存储到CosmosDB
        cosmos_client = cosmos.CosmosClient("your_cosmos_connection_string")
        database = cosmos_client.get_database_client("your_database_name")
        container = database.get_container_client("your_container_name")
        container.upsert_item(index)

    except Exception as e:
        logging.error(f"Error processing queue message: {e}")