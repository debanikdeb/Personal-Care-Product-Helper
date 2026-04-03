import random
import time
import requests
import random
import time
import requests
from bs4 import BeautifulSoup
from app.utils.logger import logger
from requests.adapters import HTTPAdapter, Retry


def create_session():
    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=0.5,
        status_forcelist=[500, 502, 503, 504, 404, 403],
        allowed_methods=["GET", "POST"],
    )
    session.mount("http://", HTTPAdapter(max_retries=retries))
    session.mount("https://", HTTPAdapter(max_retries=retries))
    return session


def is_valid_html(soup):
    if not soup or not soup.body:
        return False
    content_length = len(str(soup))
    return content_length > 500


def get_html_of_url(url, max_retries=3, delay=2):
    """Fetch HTML using requests only - NO Selenium"""
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    ]
    
    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": "https://www.myntra.com/",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-site",
    }

    session = create_session()  
    
    for attempt in range(max_retries):
        try:
            response = session.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            # Handle gzip/deflate encoding
            if response.encoding == 'ISO-8859-1':
                response.encoding = response.apparent_encoding
                
            soup = BeautifulSoup(response.text, "html.parser")
            
            if is_valid_html(soup):
                return soup
            logger.warning(f"Invalid HTML structure from {url}, attempt {attempt+1}")
            
        except requests.exceptions.RequestException as e:
            logger.warning(f"Request failed (attempt {attempt+1}/{max_retries}): {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error fetching {url}: {str(e)}")
        
        if attempt < max_retries - 1:
            time.sleep(delay * (attempt + 1))  # Exponential backoff
    
    logger.error(f"All attempts failed for {url}")
    return BeautifulSoup("<html><body></body></html>", "html.parser")