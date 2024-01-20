from fastapi import FastAPI
from data_type.manager_request import ManagerRequest
from data_type.product_filter import ProductRequest
from config.constants import *
from tools.tool import *

# default defination
apiVersion = "1"


app = FastAPI(
  title="LangChain Server",
  version="1.0",
  description="A simple api server using Langchain's Runnable interfaces",
)

@app.post("/product")
async def product(req: ProductRequest):

    if (req.priceForm != None and req.priceForm >= 700) or (req.priceTo != None and req.priceTo <= 900):
        return {
            "name" : "Iphone 15 product",
            "price": "$800"
        }
    else :
       return {
            "name" : "Iphone 14 product",
            "price": "$200"
        } 

@app.post("/managers")
async def product(req: ManagerRequest):
    heads = {
        "bu1": {
            "name": "Lac Bui Minh",
            "role": "Sr.Vice President"
        },
        "bu2": {
            "name": "Hien Pham Thanh",
            "role": "Vice President"
        },
        "bu3": {
            "name": "Phuoc Tran Phu",
            "role": "Vice President"
        },
        "dg5": {
            "name": "The Dong Pham Thanh",
            "role": "Sr.Director"
        },
        "dg5 - Common Functions": {
            "name": "The Dong Pham Thanh",
            "role": "Sr.Director"
        },
        "dc29": {
            "name": "Khanh Nguyen Nhat",
            "role": "Director"
        },
        "dc19": {
            "name": "Huy Nguyen Khac Quoc",
            "role": "Director"
        },
        "dc9": {
            "name": "Tam Ngo Hoang",
            "role": "Director (Acting)"
        },
        "dc9common": {
            "name": "Tam Ngo Hoang",
            "role": "Director (Acting)"
        },
        "dc9program1": {
            "name": "Tam Ngo Hoang",
            "role": "Director (Acting)"
        },
        "dc9program2": {
            "name": "Man Nguyen Van",
            "role": "Senior Manager"
        },
        "dc9program3": {
            "name": "Tuan Phan Hoang",
            "role": "Project Manager"
        },
        "apextension": {
            "name": "Duy Nguyen Thai",
            "role": "Project Manager (Acting)"
        },
        "axswetech": {
            "name": "Duy Nguyen Thai",
            "role": "Project Manager (Acting)"
        }
    }
    print(req.name)
    findName = req.name.replace(" ","").lower()
    try:
        return heads[findName]
    except KeyError:
        return {
            "error": "Unit not found!"
        }

if __name__ == "__main__":
    
    import uvicorn

    uvicorn.run(app, host="localhost", port=8001)