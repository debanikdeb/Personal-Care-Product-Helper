API_VERSION = "1.0.0"
API_PREFIX = "/api/v1"
MAX_SUB_URL_TO_CRAWL = 5
PRODUCT_JSON_PATH = "data/sample_products.json"
SYSTEM_PROMPT_FILE_PATH = "app/services/ai/prompts/system_prompt.yaml"
SUPPORT_CONTACT = 9999999999
CHAT_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
PRODUCT_TEMPLATE = {
    "product_name": None,
    "brand": None,
    "price": None,
    "mrp": None,
    "discount_percent": None,
    "rating": None,
    "reviews_count": None,
    "image_url": None,
    "product_url": None,  
    "breadcrumbs": None,  
    "stock_status": None,
    "scraped_at": None
}
EXTRACTED_PRODUCT_CSV_PATH = "data/extracted_products.csv"
CSV_DOWNLOAD_PATH = "/downloads/extracted_products.csv"
MYNTRA_SUB_URL_TO_CRAWL = ""