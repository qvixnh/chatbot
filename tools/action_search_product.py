from langchain.pydantic_v1 import BaseModel, Field
import requests
import json
url = 'http://localhost:8001/product'
class SearchInput(BaseModel):
    query: str = Field(description="should be a search query")


class SearchProductTool():
    name = "search_product"
    description = "useful for when you need to find or buy a product"

    async def run(
        self, query: str, chain, rewrite_chain = None
    ) -> str:
        list_entities = [
            "product_name",
            "price_from",
            "price_to"
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
                "product_name":"name",
                "price_from":"priceForm",
                "price_to": "priceTo"
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
        