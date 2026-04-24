import os

# 强制配置环境变量（解决API Key问题）
os.environ["ZHIPUAI_API_KEY"] =os.getenv("ZHIPUAI_API_KEY")

from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough
import config_data
from vector_stores import VectorStoreService
from langchain_zhipu import ZhipuAIEmbeddings, ChatZhipuAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def print_prompt(prompt):
    print("="*20)
    print(prompt.to_string())
    print("="*20)
    return prompt

# 工具函数：格式化文档
def format_document(docs: list[Document]) -> str:
    if not docs:
        return "无相关参考资料"
    formatted_str = ""
    for doc in docs:
        formatted_str += f"文档片段:{doc.page_content} \n文档元数据: {doc.metadata}\n"
    return formatted_str

class RagService(object):
    def __init__(self):
        # 向量库 + 嵌入模型
        self.vector_service = VectorStoreService(
            embedding=ZhipuAIEmbeddings(
                model=config_data.embedding_model_name,
            )
        )

        # 提示词模板
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "以我提供的资料为准，简洁专业回答用户问题。参考资料：{context}"),
                ("user", "用户问题：{input}")
            ]
        )

        # 智谱聊天模型
        self.chat_model = ChatZhipuAI(
            model_name=config_data.chat_model_name,
            temperature=0.1,
        )

        # 构建完整 RAG 链
        self.chain = self.__get_chain()

    def __get_chain(self):
        retriever = self.vector_service.get_retriever()

        # 标准 RAG 链结构
        chain = (
            {
                "context": retriever | format_document,  # 检索 + 格式化
                "input": RunnablePassthrough()
            }
            | self.prompt_template
            | print_prompt
            | self.chat_model
            | StrOutputParser()
        )
        return chain

if __name__ == "__main__":
    rag = RagService()
    res = rag.chain.invoke("我体重180斤，尺码推荐")
    print(res)