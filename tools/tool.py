from tools.action_find_manger import FindManagerTool
from tools.action_search_product import SearchProductTool

    
search_product = SearchProductTool()
find_manager = FindManagerTool()

tools = [
    {
        "name":search_product.name,
        "func":search_product.run,
        "description":search_product.description
    },
    {
        "name":find_manager.name,
        "func":find_manager.run,
        "description":find_manager.description
    }
]


tool_context = "\n\n".join(["tool_name:" + tool["name"] + "\ntool_description:" + tool["description"] for tool in tools])
