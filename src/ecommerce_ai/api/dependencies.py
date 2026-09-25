from fastapi import Request


def get_main_graph(request: Request):

    return request.app.state.main_graph