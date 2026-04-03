from fastapi import HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from app.services.scrapping.fetcher import get_html_of_url, is_valid_html
from app.services.scrapping.parser import extract_product_cards, extract_breadcrumbs
from app.services.scrapping.pagination import get_pagination_urls, save_page_to_temp
from app.services.scrapping.exporter import aggregate_to_dataframe, export_to_csv
from constants import EXTRACTED_PRODUCT_CSV_PATH, CSV_DOWNLOAD_PATH
from app.utils.logger import logger
from fastapi import APIRouter
from app.schemas.scrape import ScrapeRequest, ScrapeResponse
from constants import MAX_SUB_URL_TO_CRAWL



router = APIRouter()


@router.post("/scrape", response_model=ScrapeResponse)
async def scrape_myntra(request: ScrapeRequest):
    """
    Scrape Myntra category page and export to fixed CSV path.
    Each call OVERWRITES the previous CSV at: data/extracted_products.csv
    
    Payload:
    {
        "url": "https://www.myntra.com/personal-care?f=Categories%3ALipstick",
        "category_name": "lipstick"
    }
    
    Response:
    {
        "status": "success",
        "products_count": 120,
        "csv_download_url": "/downloads/extracted_products.csv",
        "pages_scraped": 5
    }
    """
    try:
        # Step 1: Generate pagination URLs
        page_urls = get_pagination_urls(request.url, MAX_SUB_URL_TO_CRAWL)
        
        all_products = []
        breadcrumbs = None
        
        # Step 2: Scrape each page
        for idx, url in enumerate(page_urls, 1):
            logger.info(f"[{idx}/{len(page_urls)}] Scraping: {url}")
            
            soup = get_html_of_url(url)
            if not is_valid_html(soup):
                logger.warning(f"Skipping invalid page: {url}")
                continue
            
            # Save raw HTML to TEMP (for debugging/audit)
            save_page_to_temp(soup, idx, url)
            
            # Extract breadcrumbs once (from first valid page)
            if not breadcrumbs:
                breadcrumbs = extract_breadcrumbs(soup, request.url)
            
            # Extract product cards
            products = extract_product_cards(soup, request.url)
            all_products.extend(products)
            
            # Respectful delay to avoid rate limiting
            import time
            time.sleep(2)
        
        if not all_products:
            raise HTTPException(status_code=404, detail="No products found on the provided URL")
        
        # Step 3: Aggregate and export to FIXED CSV path (overwrites previous)
        df = aggregate_to_dataframe(all_products, breadcrumbs)
        csv_path = export_to_csv(df, category_name=request.category_name, overwrite=True)
        
        # Step 4: Build response
        return ScrapeResponse(
            status="success",
            products_count=len(df),
            csv_download_url=CSV_DOWNLOAD_PATH,
            pages_scraped=len(page_urls)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Scraping failed")
        raise HTTPException(status_code=500, detail=f"Scraping error: {str(e)}")


@router.get("/download-csv")
async def download_csv():
    """
    Download the latest scraped CSV file.
    File location: data/extracted_products.csv (overwritten on each scrape)
    """
    filepath = Path(EXTRACTED_PRODUCT_CSV_PATH)
    
    if not filepath.exists():
        raise HTTPException(
            status_code=404, 
            detail="CSV file not found. Please run /scrape first."
        )
    
    return FileResponse(
        path=str(filepath),
        filename="extracted_products.csv",
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=extracted_products.csv"
        }
    )
