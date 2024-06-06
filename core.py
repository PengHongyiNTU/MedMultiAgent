from typing import AsyncIterator, Dict, Any, Union
import dotenv
from loguru import logger
from workflow import ConsultOpenAIGPT4
from langchain_core.messages import HumanMessage



# Just for testing
# Not the final version
class Coordinator:
    def __init__(self) -> None:
        try:
            dotenv.load_dotenv()
        except Exception:
            logger.warning("No .env file found")
        logger.info("Initializing the coordinator")


    async def start_with(self, 
                         message: str) -> AsyncIterator:
        workflow = ConsultOpenAIGPT4().get_runnable()
        return workflow.astream(message)
        
