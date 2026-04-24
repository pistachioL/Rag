import streamlit as st
from knowledge_base import KnowledgeBaseService
st.title("知识库更新")
upload_file = st.file_uploader(
    "上传文件",
    type=["txt"],
    accept_multiple_files=False
)

if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()

if upload_file is not None:
    file_name = upload_file.name
    file_type = upload_file.type
    file_size = upload_file.size

    st.subheader(f"文件名：{file_name}")
    st.write(f"格式: {file_type} | 大小: {file_size}")
    text = upload_file.getvalue().decode("utf-8")
    result = st.session_state["service"].upload_by_str(text, file_name)
    st.write(result)
