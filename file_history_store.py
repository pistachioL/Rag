import json
import os
from typing import Sequence

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict

def get_history(session_id):
    return FileChatMessageHistory(session_id, "./char_history")


class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id, store_path):
        self.session_id = session_id
        self.store_path = store_path
        self.file_path = os.path.join(self.store_path, self.session_id)
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        # 存储在内存
        all_messages = list(self.messages)
        all_messages.extend(messages)

        new_messages = [message_to_dict(msg) for msg in all_messages]
        # 存储到磁盘
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(new_messages, f)


    @property
    def messages(self) -> list[BaseMessage]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                message_data= json.load(f)
                return messages_from_dict(message_data)
        except FileNotFoundError:
            return []

    def clear(self)-> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f)


