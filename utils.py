from typing import Tuple, Type
from langchain_core.pydantic_v1 import BaseModel
from langchain_core.output_parsers import JsonOutputParser


def auto_schema_prompt(
    basemodel: Type[BaseModel],
) -> Tuple[str, JsonOutputParser]:
    """
    Generate the schema prompt and output parser for LLMs that do not
    implement `llm.with_structured_output()`.

    Args:
        basemodel (BaseModel): The Pydantic BaseModel defining the schema.

    Returns:
        Tuple[str, BaseOutputParse]: The generated schema prompt and 
        the output parser.
    """
    parser = JsonOutputParser(pydantic_object=basemodel)
    prompt = parser.get_format_instructions()
    return prompt, parser
