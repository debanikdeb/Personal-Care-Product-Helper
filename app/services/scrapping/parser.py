import re
import json
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from app.utils.logger import logger
import pandas as pd


def extract_breadcrumbs(soup: BeautifulSoup, base_url: str) -> str:
    """Extract breadcrumb trail: Home/Personal Care/Lipstick"""
    # Try common breadcrumb patterns
    breadcrumb_selectors = [
        {"class": re.compile(r"bread.*crumb", re.I)},
        {"class": re.compile(r"breadcrumbs", re.I)},
        {"nav": True},
        {"aria-label": re.compile(r"breadcrumb", re.I)},
    ]
    
    for selector in breadcrumb_selectors:
        bc_container = soup.find(**selector)
        if bc_container:
            links = bc_container.find_all("a")
            if links:
                crumbs = [link.get_text(strip=True) for link in links if link.get_text(strip=True)]
                if crumbs:
                    return "/" + "/".join(crumbs)
    
    # Fallback: parse from URL path
    parsed = urlparse(base_url)
    path_parts = [p for p in parsed.path.split("/") if p and p not in ["search", "shop"]]
    if path_parts:
        return "/" + "/".join([part.replace("-", " ").title() for part in path_parts[:3]])
    
    return "Home/Personal Care/Lipstick"  # Default fallback



def extract_product_cards(soup: BeautifulSoup, base_url: str) -> list[dict]:
    """Extract Myntra products from embedded JSON using productId as anchor"""
    products = []
    
    # Get full HTML and decode unicode escapes upfront for reliable regex
    html_str = str(soup)
    try:
        html_decoded = html_str.encode().decode('unicode_escape')
    except (UnicodeDecodeError, UnicodeEncodeError):
        html_decoded = (html_str
            .replace('\\u002F', '/').replace('\\u003C', '<').replace('\\u003E', '>')
            .replace('\\u0026', '&').replace('\\u0022', '"').replace('\\u003D', '=')
            .replace('\\u0020', ' ').replace('\\u003A', ':'))
    
    logger.info(f"Starting Myntra extraction for {base_url}")
    
    # Find productId anchors - every Myntra product has one
    anchor_pattern = r'"productId"\s*:\s*(\d+)'
    matches = list(re.finditer(anchor_pattern, html_decoded))
    logger.info(f"Found {len(matches)} productId anchors")
    
    success_count = 0
    parse_error_count = 0
    extract_error_count = 0
    validation_fail_count = 0
    
    for match_idx, match in enumerate(matches):
        try:
            anchor_pos = match.start()
            
            # Extract JSON object containing this anchor
            json_str = _extract_json_object(html_decoded, anchor_pos)
            if not json_str:
                extract_error_count += 1
                continue
            
            # Parse JSON
            try:
                data = json.loads(json_str)
            except json.JSONDecodeError as e:
                parse_error_count += 1
                logger.debug(f"Product {match_idx}: JSON parse failed: {e}")
                continue
            
            # Validate minimal product signature
            if not isinstance(data, dict):
                validation_fail_count += 1
                continue
            product_id = data.get("productId")
            if not product_id:
                validation_fail_count += 1
                continue
            # Accept if has productName OR brand OR articleType == Lipstick
            if not (data.get("productName") or data.get("brand") or data.get("articleType") == "Lipstick"):
                validation_fail_count += 1
                continue
            
            # Build product URL
            landing_url = data.get("landingPageUrl") or data.get("url") or data.get("productUrl")
            if landing_url:
                if landing_url.startswith("http"):
                    product_url = landing_url
                else:
                    product_url = urljoin(base_url, "/" + landing_url.lstrip("/"))
            else:
                product_url = None
            
            # Extract image URL
            image_url = data.get("searchImage") or data.get("imageUrl")
            if not image_url:
                images = data.get("images")
                if isinstance(images, list) and images:
                    first_img = images[0]
                    if isinstance(first_img, dict):
                        image_url = first_img.get("src") or first_img.get("imageUrl")
                    elif isinstance(first_img, str):
                        image_url = first_img
            
            # Extract price fields
            price = data.get("price")
            mrp = data.get("mrp") or data.get("originalPrice")
            discount = data.get("discount")
            
            # Calculate discount percent
            discount_percent = None
            if discount is not None:
                discount_percent = f"{int(discount)}%"
            elif price and mrp:
                try:
                    pct = ((float(mrp) - float(price)) / float(mrp)) * 100
                    discount_percent = f"{int(pct)}%"
                except (ValueError, TypeError):
                    pass
            
            products.append({
                "product_name": data.get("productName") or data.get("product") or data.get("name"),
                "brand": data.get("brand"),
                "price": str(price) if price is not None else None,
                "mrp": str(mrp) if mrp is not None else None,
                "discount_percent": discount_percent,
                "rating": data.get("rating"),
                "reviews_count": data.get("ratingCount"),
                "image_url": image_url,
                "product_url": product_url,
                "stock_status": "in_stock",
                "productId": product_id,
            })
            success_count += 1
            
        except Exception as e:
            logger.debug(f"Product {match_idx}: Unexpected error: {type(e).__name__}: {e}")
            continue
    
    logger.info(f"Extraction complete: {success_count} succeeded, {parse_error_count} parse errors, {extract_error_count} extract errors, {validation_fail_count} validation fails")
    logger.info(f"Extracted {len(products)} products from JSON")
    
    # Fallback: DOM scraping if JSON extraction yielded few results
    if len(products) < 10:
        logger.info("Fallback: attempting DOM-based extraction via URL patterns")
        product_links = soup.find_all("a", href=lambda x: x and re.search(
            r"/(lipstick|buy|product)/[^/]+/\d+", x, re.I
        ))
        
        seen_urls = set()
        for link in product_links[:100]:
            href = link.get("href", "")
            if not href or href in seen_urls:
                continue
            seen_urls.add(href)
            
            product_url = urljoin(base_url, href)
            name_elem = link.find(["h3", "h4", "p", "span"], string=lambda s: s and len(str(s).strip()) < 100)
            product_name = name_elem.get_text(strip=True) if name_elem else link.get_text(strip=True)[:80]
            
            price = None
            price_elem = link.find(string=lambda s: s and "₹" in str(s))
            if price_elem:
                match = re.search(r"₹\s*([\d,]+\.?\d*)", str(price_elem))
                if match:
                    price = match.group(1).replace(",", "")
            
            if product_name or price:
                products.append({
                    "product_name": product_name or None,
                    "brand": None,
                    "price": price,
                    "mrp": None,
                    "discount_percent": None,
                    "rating": None,
                    "reviews_count": None,
                    "image_url": None,
                    "product_url": product_url,
                    "stock_status": "in_stock",
                })
        
        logger.info(f"DOM fallback extracted {len(products) - success_count} additional products")
    
    return products


def _extract_json_object(text: str, anchor_pos: int, max_len: int = 8000) -> str:
    """
    Extract complete JSON object {...} containing the anchor position.
    More tolerant: searches wider range, handles nested structures better.
    """
    # Search further back to find opening brace (product objects can be deeply nested)
    search_start = max(0, anchor_pos - 5000)
    open_brace = text.rfind("{", search_start, anchor_pos + 1)
    
    if open_brace == -1:
        return None
    
    # Count braces to find matching close, respecting strings and escapes
    brace_count = 0
    in_string = False
    escape_next = False
    
    for i in range(open_brace, min(open_brace + max_len, len(text))):
        char = text[i]
        
        if escape_next:
            escape_next = False
            continue
        if char == "\\":
            escape_next = True
            continue
        if char == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        
        if char == "{":
            brace_count += 1
        elif char == "}":
            brace_count -= 1
            if brace_count == 0:
                return text[open_brace:i + 1]
    
    return None