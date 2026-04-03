import sys
import traceback
from pathlib import Path
from bs4 import BeautifulSoup

try:
    from app.services.scrapping.parser import extract_product_cards
    
    # Load saved page
    page_file = Path('tmp/page_5.txt')
    with open(page_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse HTML
    soup = BeautifulSoup(content, 'html.parser')
    
    # Extract products
    products = extract_product_cards(soup, 'https://www.myntra.com/personal-care?f=Categories%3ALipstick')
    
    print(f'✅ Extracted {len(products)} products')
    for i, prod in enumerate(products[:5]):
        print(f'{i+1}. {prod.get("product_name")} - {prod.get("brand")} - Rating: {prod.get("rating")}')
        
except Exception as e:
    print(f'❌ Error: {e}')
    traceback.print_exc()
