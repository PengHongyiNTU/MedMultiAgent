from typing import Any, List, Optional, Dict, Type, Literal
from uuid import UUID
from langchain_core.runnables import Runnable
from langchain_core.callbacks import AsyncCallbackHandler
from loguru import logger
from workflow import Workflow
from session import state


class SessionCallbackHandler(AsyncCallbackHandler):
    def __init__(self, workflow_name : Optional[str]="Unknown"):
        self.workflow_name = workflow_name
    async def on_chain_start(self,
                             serialized: Dict[str, Any], 
                             inputs: Dict[str, Any], *, 
                             run_id: UUID, 
                             parent_run_id: Optional[UUID] = None, 
                             tags: Optional[List[str]] = None, 
                             metadata: Optional[Dict[str, Any]] = None, 
                             **kwargs: Any) -> None:
        sub_process_name = serialized['name']
        logger.info(f"Running {self.workflow_name}.{sub_process_name} with run_id: {run_id}")
        if 'current_running' not in state:
            state['current_running'] = {run_id: f"{self.workflow_name}.{sub_process_name}"}
        else:
            state.current_running[run_id] = f"{self.workflow_name}.{sub_process_name}"
    
    async def on_chain_end(self,
                           outputs: Dict[str, Any], 
                           *, run_id: UUID, 
                           parent_run_id: Optional[UUID] = None, 
                           **kwargs: Any) -> None:
        sub_process_name = state.current_running[run_id]
        logger.info(f"Finished {sub_process_name} with run_id: {run_id}")
        state.current_running.pop(run_id)



def _worflow_bind_with_session(workflow: Workflow) -> Runnable:
    workflow_name = workflow.__class__.__name__
    runnable = workflow.get_runnable()
    return runnable.with_config(callbacks=[SessionCallbackHandler(workflow_name)])


def bind_with_session(cls: Type[Workflow]) -> Type[Workflow]:
   def new_get_runnable(self):
       return _worflow_bind_with_session(self)
   cls.get_runnable = new_get_runnable
   return cls

def bind_runnable_with_session(runnable: Runnable, 
                               parent_Workflow: Type[Workflow]) -> Runnable:
    workflow_name = parent_Workflow.__name__
    return runnable.with_config(callbacks=[SessionCallbackHandler(workflow_name)])


    