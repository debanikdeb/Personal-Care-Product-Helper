from app.utils.logger import logger
from constants import MAX_SUB_URL_TO_CRAWL
from bs4 import BeautifulSoup
from app.core.config import settings
import re
from pathlib import Path


def get_pagination_urls(base_url: str, max_pages: int = MAX_SUB_URL_TO_CRAWL) -> list[str]:
    """Generate pagination URLs for Myntra category pages"""
    urls = [base_url]  # Page 1 is the base URL
    
    # Myntra uses p=2, p=3, etc. for pagination
    if "?" in base_url:
        base_with_amp = base_url + "&"
    else:
        base_with_amp = base_url + "?"
    
    for page in range(2, max_pages + 1):
        urls.append(f"{base_with_amp}p={page}")
    
    return urls


def save_page_to_temp(soup: BeautifulSoup, page_num: int, url: str) -> str:
    """Save raw HTML to TEMP folder as txt file"""
    filepath = Path(settings.TEMP_PATH) / f"page_{page_num}.txt"
    
    # Save metadata as first line for reference
    content = f"<!-- SOURCE_URL: {url} -->\n<!-- PAGE: {page_num} -->\n{str(soup)}"
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    
    logger.info(f"Saved page {page_num} to {filepath}")
    return str(filepath)


def load_page_from_temp(page_num: int) -> tuple[BeautifulSoup, str]:
    """Load page from TEMP folder and return soup + original URL"""
    filepath = Path(settings.TEMP_PATH) / f"page_{page_num}.txt"
    
    if not filepath.exists():
        raise FileNotFoundError(f"TEMP file not found: {filepath}")
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Extract original URL from comment
    url_match = re.search(r"<!-- SOURCE_URL: (.*?) -->", content)
    original_url = url_match.group(1) if url_match else None
    
    # Remove metadata comments before parsing
    clean_content = re.sub(r"<!-- SOURCE_URL: .*? -->\n<!-- PAGE: \d+ -->\n", "", content)
    soup = BeautifulSoup(clean_content, "html.parser")
    
    return soup, original_url