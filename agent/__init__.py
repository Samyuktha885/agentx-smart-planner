
"""Tool registry for the AgentX Smart Planner."""


class Tool:
    name = "tool"
    description = ""
    args_doc = "{}"

    def execute(self, **kwargs):
        raise NotImplementedError


def build_tools():
    from tools.calculator import Calculator
    from tools.data_query import ListFiles, ReadFile, SqlQuery
    from tools.web_search import WebSearch

    tools = [
        ListFiles(),
        ReadFile(),
        SqlQuery(),
        Calculator(),
        WebSearch(),
    ]

    return {tool.name: tool for tool in tools}
