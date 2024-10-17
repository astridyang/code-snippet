# code-snippet

# 部署

### 错误 ERROR: Could not install packages due to an OSError

1.检查当前空间使用情况 2.清理空间 3.修改部署方式

- .deployment pip install --no-cache-dir -r requirements.txt
- 减少不必要的包
- 修改应用程序设置 4.增加存储配额，在应用设置中添加：WEBSITE_CONTENTSHARE_SIZE = 2 # 增加到 2GB

## kudo console

- https://learn.microsoft.com/en-us/azure/app-service/resources-kudu
- https://cloud-right.com/2016/07/azure-functions-kudu/
- https://stackoverflow.com/questions/78075199/im-having-a-problem-with-my-application-on-azure-web-app
