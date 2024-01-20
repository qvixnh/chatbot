from langchain.pydantic_v1 import BaseModel, Field
import requests
import json
url = 'http://localhost:8001/managers'

class FindManagerTool():
    name = "find_manager"
    description = "useful for when you need to find head or manager or director of unit BU, DG, DC, Program, Team"

    async def run(
        self, query: str, chain, rewrite_chain = None
    ) -> str:
        list_entities = [
            "unit_name"
        ]
        detected_result = chain({"context":"\n".join(list_entities), 'user_input':query})
        context = detected_result['text']
        if context != "None":
            dict_entities = {}

            pairs = context.split('|')
            for pair in pairs:
                if len(pair) > 0:
                    key_value = pair.split(':')
                    
                    if key_value[0].strip() in list_entities and len(key_value) > 1:
                        dict_entities[key_value[0].strip()] = key_value[1].strip()
            print(dict_entities)
            data = {}
            keys = {
                "unit_name":"name"
            }
            rewrite_context= []
            for key in list_entities:
                try:
                    data[keys[key]] = dict_entities[key]
                    rewrite_context.append("'"+key + "':'" + dict_entities[key]+"'")
                except KeyError:
                    pass
            r = requests.post(url, params={}, json=data)
            rewrite_result = rewrite_chain({"context":", ".join(rewrite_context)})
            return {
                "text": rewrite_result['text'],
                "data": r.json()
            }
        else:
            return context
        