# -*- coding: utf-8 -*-
from typing import TypedDict, List
from langchain_core.runnables import Runnable
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore
from langchain_core.retrievers import BaseRetriever
import importlib
import inspect
from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from loguru import logger
from workflow import Workflow


class NotWorkflowError(Exception):
    pass


class WorkFlowNotFoundError(Exception):
    pass


class WorkflowRecord(TypedDict):
    name: str
    description: str
    runnable: Runnable


class WorkflowStorage:
    def __init__(self):
        self.runnables = self._load_defined_workflows()
        if not self.runnables:
            raise WorkFlowNotFoundError("No workflows found")
        logger.info(f"Found {len(self.runnables)} workflows")
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        # Chroma is an In-memory vector store
        # Thus it is recommended to use it only to store workflows
        self.vector_store_cls = Chroma
        logger.info("Creating vector store from workflows")
        self.vectorstore = self._init_vectorstore()

    def _load_defined_workflows(self) -> List[WorkflowRecord]:
        runnables = []
        try:
            workflow_module = importlib.import_module("workflow")
        except ImportError as e:
            logger.error(f"Error importing workflow module: {e}")
            raise

        for name, obj in inspect.getmembers(workflow_module):
            if inspect.isclass(obj):
                if issubclass(obj, Workflow) and obj != Workflow:
                    instance = obj()
                    description = instance.description
                    runnable = instance.get_runnable()
                    workflow_record = WorkflowRecord(
                        name=name,
                        description=description,
                        runnable=runnable,
                    )
                    runnables.append(workflow_record)
        return runnables

    def _init_vectorstore(self) -> VectorStore:
        documents = [
            Document(
                page_content=f"{record['name']}: {record['description']}",
                metadata={"name": record["name"]},
            )
            for record in self.runnables
        ]
        logger.info("Creating vector store from documents")
        vectorstore = self.vector_store_cls.from_documents(
            documents=documents,
            embedding=self.embeddings,
        )
        logger.info("Vector store created")
        return vectorstore

    def get_as_retriever(self) -> BaseRetriever:
        retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 20},
        )
        return retriever

    def get_as_prompts(self) -> str:
        if len(self.runnables) >= 15:
            logger.warning("Too many workflows. Recommend to use as retriever")
        prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """Following are the workflows available \n
                    {workflows}""",
                ),
            ],
        )
        workflows_str = "\n".join(
            [
                f"{idx + 1}. {record['name']}: {record['description']}"
                for idx, record in enumerate(self.runnables)
            ],
        )
        prompt = prompt_template.format(workflows=workflows_str)
        return prompt


if __name__ == "__main__":
    storage = WorkflowStorage()
    retriever = storage.get_as_retriever()
    print(retriever)
    print(storage.get_as_prompts())
