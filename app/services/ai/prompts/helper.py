import aiofiles
import yaml
from constants import SYSTEM_PROMPT_FILE_PATH
from app.utils.logger import logger


async def async_load_prompt_file(prompt_name, file_path):
    async with aiofiles.open(file_path, "r", encoding="utf-8") as file:
        content = await file.read()
        prompts = yaml.safe_load(content)

    # Search for the prompt by name and return its text
    for prompt in prompts["prompts"]:
        if prompt["name"] == prompt_name:
            return prompt["text"]

    return None


async def async_load_system_prompt(
    prompt_name, file_path=SYSTEM_PROMPT_FILE_PATH
):
    return await async_load_prompt_file(prompt_name, file_path)



async def load_system_prompt(prompt_name: str, prompt_path: str) -> str:
    """Async load prompt text from YAML file."""
    prompt_text = await async_load_system_prompt(
        prompt_name, prompt_path
    )
    if not prompt_text:
        logger.critical(f"Prompt {prompt_name} not found in {prompt_path}")
        raise ValueError(f"Prompt '{prompt_name}' not found in {prompt_path}")
    logger.info(f"Loaded prompt {prompt_name} successfully")
    return prompt_text



def format_content_prompt(
    prompt_template: str,
    context: str, 
    query: str, 
    tool: str,
    contact_info: str
) -> str:
    """
    Fills the prompt template with context and query.
    """
    return prompt_template.format(
        context=context, query=query, tool=tool, contact_info=contact_info
    )
