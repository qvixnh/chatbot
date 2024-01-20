import time, os
from fastapi import FastAPI
from data_type.conversation_request import ConvesationRequest
from langchain_community.utilities.searchapi import SearchApiAPIWrapper
from embedding.embedding import LangChainEmbedding
from infrastructure.defination import LangChainDefination, ModelType
from langchain.memory import MongoDBChatMessageHistory, ConversationBufferMemory
from config.constants import *
from tools.tool import *

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = "AIzaSyBTiUCRKEn7jPQqTn2Ok1jWTCXhjMEiHT0"
if "SEARCHAPI_API_KEY" not in os.environ:
    os.environ["SEARCHAPI_API_KEY"] = "T61bzfFQuTuC5wRYxRsJj83A"

# default defination
apiVersion = "1"
defination = LangChainDefination(type= ModelType.GEMINI)
defination_local = LangChainDefination(type= ModelType.GEMINI)
embedding = LangChainEmbedding()

llm = defination.llm(MODEL_PATH)
llm_chain_embedding = defination.llm_chain(prompt=defination.prompt(EMBEDDING_TEMPLATE),llm=llm)
llm_local = defination.llm(MODEL_PATH,0)
llm_chain_tool = defination.llm_chain(prompt=defination.prompt(TOOL_TEMPLATE),llm=llm_local)
llm_chain_detect = defination.llm_chain(prompt=defination.prompt(DETECT_ENTITY_TEMPLATE),llm=llm_local)
llm_chain_rewrite = defination.llm_chain(prompt=defination.prompt(REWRITE_TEMPLATE),llm=llm)

embedding.load_document(EMBEDDING_DOCUMENT_PATH,EMBEDDING_STORED_PATH)

app = FastAPI(
  title="LangChain Server",
  version="1.0",
  description="A simple api server using Langchain's Runnable interfaces",
)

@app.post("/completion")
async def completion(req: ConvesationRequest):
    text = req.text
    start = time.perf_counter()
    mongo_history = MongoDBChatMessageHistory(connection_string= MEMORY_CONNECTION_STRING,session_id= str(req.sessionId))
    memory = ConversationBufferMemory(
        input_key="user_input",
        chat_memory=mongo_history,
        memory_key='chat_history'
    )
    
    result = llm_chain_tool({"context":tool_context, "user_query": text})
    print("Tool:" , result["text"])
    if result["text"] != "None":
        cur_tool = next((tool for tool in tools if tool["name"] == result["text"]), None)
        result_of_tool = await cur_tool["func"](query = text,chain= llm_chain_detect,rewrite_chain=llm_chain_rewrite)
        end = time.perf_counter()
        print(f"Time elapsed: {end - start:.2f} seconds")
        return {
            "response" : result_of_tool,
            "type": "This result from tool",
            "sessionId": req.sessionId
        }
    else:
        document = embedding.find_document(text)
        result = llm_chain_embedding(document)
        print("Embedding:" , result["text"])
        if result["text"] != "None":
            mongo_history.add_user_message(text)
            mongo_history.add_ai_message(result["text"])
            return {
                "response" : {
                    "text": result["text"]
                },
                "type": "This result from embedding",
                "sessionId": req.sessionId
            }
        else:
            conversation = defination.conversation_chain(prompt=defination.conversation_prompt(DEFAULT_TEMPLATE), llm=llm, memory= memory)
            result = conversation({"user_input": text})
            end = time.perf_counter()
            print(f"Time elapsed: {end - start:.2f} seconds")
            return {
                "response" : {
                    "text": result["text"]
                },
                "type": "This result from conversation",
                "sessionId": req.sessionId
            }


if __name__ == "__main__":
    
    import uvicorn

    uvicorn.run(app, host=HOST, port=8000)
