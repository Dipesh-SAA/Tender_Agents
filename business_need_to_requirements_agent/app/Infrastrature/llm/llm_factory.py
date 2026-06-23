from dotenv import load_dotenv
import os
load_dotenv()
from langchain_mistralai import ChatMistralAI
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from bson import ObjectId

from business_need_to_requirements_agent.app.Infrastrature.llm.mongo_client import (
    get_document,
)
from business_need_to_requirements_agent.app.utils.decrept import decrypt
# def get_llm(provider: str | None = None):
#     provider = (provider or os.getenv("LLM_PROVIDER", "mistral")).lower()

#     security_doc = get_document(
#         collection_name="Security",
#         filter_query={
#             "_id": ObjectId("6a3944f958430082848fc63d")
#         }
#     )
 
#     if not security_doc:
#         raise Exception("Security document not found")
 
#     encrypted_key = security_doc.get("Security")
 
#     if not encrypted_key:
#         raise Exception("Security field not found")
 
#     openai_api_key = decrypt(encrypted_key)
 
#     self.llm = ChatOpenAI(
#         model=os.getenv(
#             "LLM_MODEL",
#             "gpt-4.1"
#         ),
#         temperature=0,
#         api_key=openai_api_key
#     )

#     elif provider == "mistral":
#         return ChatMistralAI(
#             model=os.getenv("MISTRAL_MODEL", "mistral-large-latest"),
#             temperature=float(os.getenv("LLM_TEMPERATURE", 0)),
#             api_key=os.getenv("MISTRAL_API_KEY"),
#         )

#     elif provider == "ollama":
#         return ChatOllama(
#             model=os.getenv("OLLAMA_MODEL", "mistral:7b"),
#             temperature=float(os.getenv("LLM_TEMPERATURE", 0)),
#         )

#     else:
#         raise ValueError(f"Unsupported LLM_PROVIDER: {provider}")
    


def get_llm(provider: str | None = None):
    provider = (provider or os.getenv("LLM_PROVIDER", "mistral")).lower()

    if provider == "openai":
        security_doc = get_document(
            collection_name="Security",
            filter_query={
                "_id": ObjectId("6a3944f958430082848fc63d")
            }
        )
     
        if not security_doc:
            raise Exception("Security document not found")
     
        encrypted_key = security_doc.get("Security")
     
        if not encrypted_key:
            raise Exception("Security field not found")
     
        openai_api_key = decrypt(encrypted_key)
     
        # Fixed: Changed from self.llm to a standard return statement
        return ChatOpenAI(
            model=os.getenv(
                "LLM_MODEL",
                "gpt-4.1"
            ),
            temperature=0,
            api_key=openai_api_key
        )

    elif provider == "mistral":
        return ChatMistralAI(
            model=os.getenv("MISTRAL_MODEL", "mistral-large-latest"),
            temperature=float(os.getenv("LLM_TEMPERATURE", 0)),
            api_key=os.getenv("MISTRAL_API_KEY"),
        )

    elif provider == "ollama":
        return ChatOllama(
            model=os.getenv("OLLAMA_MODEL", "mistral:7b"),
            temperature=float(os.getenv("LLM_TEMPERATURE", 0)),
        )

    else:
        raise ValueError(f"Unsupported LLM_PROVIDER: {provider}")

 
# ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
 
# def decrypt(encrypted_text):
#     key_bytes = ENCRYPTION_KEY.encode("utf-8")
#     iv = bytes(16)
 
#     cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
 
#     decrypted_bytes = unpad(
#         cipher.decrypt(base64.b64decode(encrypted_text)),
#         AES.block_size
#     )
 
#     return decrypted_bytes.decode("utf-8")
