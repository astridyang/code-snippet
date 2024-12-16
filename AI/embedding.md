What are the text chunking/splitting and embedding best practices for RAG applications?

e5-large-v2

instructor-large

multilingual-e5-large

https://huggingface.co/intfloat/multilingual-e5-large-instruct

[Embeddings Tutorial using Azure OpenAI Service](https://clemenssiebler.com/posts/azure-openai-service-embeddings-tutorial/)
[How to Generate Embeddings with Azure OpenAI?](https://thetechplatform.medium.com/how-to-generate-embeddings-with-azure-openai-f0f1a96638b0)
[AzureOpenAIEmbeddings](https://python.langchain.com/docs/integrations/text_embedding/azureopenai/)
[Tutorial: Explore Azure OpenAI Service embeddings and document search](https://learn.microsoft.com/en-us/azure/ai-services/openai/tutorials/embeddings?tabs=python-new%2Ccommand-line&pivots=programming-language-python)

## tool_calls
- 定义function，xx情况下调用function，如果llm的返回提示要调用function，则去调用function
documentation
- [OpenAI tool_calls](https://platform.openai.com/docs/guides/function-calling)
- [Streaming tool calls](https://platform.openai.com/docs/guides/function-calling#advanced-usage)