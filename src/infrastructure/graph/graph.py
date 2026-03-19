from src.domain.utilities.logger import logger

def build_graph(model, tools):
    """"""
    logger.info(msg="Start")
    logger.debug() # TODO

    model_with_tools = model.bind_tools(tools)
