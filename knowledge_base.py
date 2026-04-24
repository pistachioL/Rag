"""
知识库
"""
import hashlib
import os.path
from langchain_chroma import Chroma
import config_data
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime
from langchain_zhipu import ZhipuAIEmbeddings

def check_md5(md5_str:str):
    if not os.path.exists(config_data.md5_path):
        open(config_data.md5_path,"w",encoding="utf-8").close()
        return False
    else :
        for line in open(config_data.md5_path, "r", encoding="utf-8").readlines():
            line = line.strip()
            if line==md5_str:
                return True
        return False

def save_md5(md5_str: str):
    with open(config_data.md5_path, "a", encoding="utf-8") as f:
        f.write(md5_str + '\n')

def get_string_md5(input_str:str, encoding='utf-8'):
    str_bytes = input_str.encode(encoding=encoding)
    md5_obj= hashlib.md5()
    md5_obj.update(str_bytes)
    md5_hex = md5_obj.hexdigest()
    return md5_hex


class KnowledgeBaseService(object):
    def __init__(self):
        # 文件夹不存在则创建
        os.makedirs(config_data.persist_directory, exist_ok = True)

        # 向量数据库
        self.chroma = Chroma(
            collection_name = config_data.collection_name,
            embedding_function=ZhipuAIEmbeddings(
                api_key= os.getenv("ZHIPU_API_KEY"),
                model=config_data.embedding_model_name,  # 官方推荐嵌入模型
            ),
            persist_directory=config_data.persist_directory
        )

        # 文本分割器
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config_data.chunk_size,
            chunk_overlap = config_data.chunk_overlap, # 两个文本之间分段重叠数
            separators=config_data.separators,
            length_function=len,
        )

    def upload_by_str(self, data:str, filename):

        md5_hex = get_string_md5(data)
        if check_md5(md5_hex):
            return "[跳过]内容已经存在知识库中"
        if len(data) > config_data.max_split_char_number:
            knowledge_chunks : list[str] = self.spliter.split_text(data)
        else:
            knowledge_chunks = [data]

        metadata = {
            "source": filename,
            "create_time" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator":"admin"
        }
        # 切割好的文本存储到chroma
        self.chroma.add_texts(
            knowledge_chunks,
            metadatas=[metadata for _ in knowledge_chunks] # 给每一个切好的n段文本（knowledge_chunks）带上一摸一样的metadata，存入chroma
        )
        save_md5(md5_hex)

        return "[成功]内容已成功载入向量库"


if __name__ == '__main__':
    print("开始初始化知识库服务...")
    service = KnowledgeBaseService()
    print("2...")
    r = service.upload_by_str("周杰伦1","testfile")
    print(r)