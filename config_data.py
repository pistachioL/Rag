md5_path = "./md5.txt"

#chroma
collection_name = "rag"
persist_directory="./chroma_db"

#spliter
chunk_size=1000
chunk_overlap = 100
separators=["\n\n","\n",".","!","?","？","。","！",""," "]
max_split_char_number = 1000

#检索返回匹配的文章数
similarity_threshold = 2

embedding_model_name="embedding-3"
chat_model_name="glm-5.1"

session_config = {
    "configurable": {"session_id": "user_123"}
}