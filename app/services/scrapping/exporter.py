import pandas as pd
from datetime import datetime
from constants import PRODUCT_TEMPLATE
from app.utils.logger import logger
from constants import EXTRACTED_PRODUCT_CSV_PATH
from pathlib import Path


def calculate_discount(price: str, mrp: str) -> str:
    """Calculate discount percentage if both price and MRP available"""
    try:
        if price and mrp and float(mrp) > 0:
            discount = ((float(mrp) - float(price)) / float(mrp)) * 100
            return f"{discount:.0f}%"
    except (ValueError, TypeError):
        pass
    return None

def aggregate_to_dataframe(products: list[dict], breadcrumbs: str) -> pd.DataFrame:
    """Convert product list to DataFrame with template structure"""
    rows = []
    
    for prod in products:
        row = PRODUCT_TEMPLATE.copy()
        row.update({k: v for k, v in prod.items() if v is not None})
        row["breadcrumbs"] = breadcrumbs
        row["scraped_at"] = datetime.now().isoformat()
        
        # Calculate discount if possible
        if row["price"] and row["mrp"]:
            row["discount_percent"] = calculate_discount(row["price"], row["mrp"])
        
        rows.append(row)
    
    df = pd.DataFrame(rows)
    
    # Reorder columns for readability
    preferred_order = [
        "product_name", "brand", "price", "mrp", "discount_percent",
        "rating", "reviews_count", "stock_status",
        "image_url", "product_url", "breadcrumbs", "scraped_at"
    ]
    existing_cols = [c for c in preferred_order if c in df.columns]
    remaining_cols = [c for c in df.columns if c not in preferred_order]
    
    return df[existing_cols + remaining_cols]

def export_to_csv(df: pd.DataFrame, category_name: str = "lipstick", overwrite: bool = True) -> str:
    """Export DataFrame to CSV"""
    filepath = Path(EXTRACTED_PRODUCT_CSV_PATH)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    df.to_csv(filepath, index=False, encoding="utf-8")
    logger.info(f"Exported {len(df)} products to {filepath}")
    
    return str(filepath)