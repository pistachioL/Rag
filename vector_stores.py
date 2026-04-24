"""
向量存储：通过embedding模型，将文本转换为向量
"""
import os
from langchain_chroma import Chroma
from langchain_zhipu import ZhipuAIEmbeddings
import config_data
class VectorStoreService:
    def __init__(self, embedding):
        self.embedding = embedding

        self.vector_store = Chroma(
            collection_name=config_data.collection_name,
            embedding_function=self.embedding,
            persist_directory=config_data.persist_directory,
        )

    # 获取向量检索器
    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k":config_data.similarity_threshold}) # 返回检索个数

if __name__ == "__main__":
    retriever = VectorStoreService(ZhipuAIEmbeddings(
                api_key= os.getenv("ZHIPU_API_KEY"),
                model="embedding-3",  # 官方推荐嵌入模型
            )).get_retriever()
    res = retriever.invoke("我的身高体重是160cm，100斤，尺码推荐")
    print(res)