from pydantic import BaseModel, Field, validator
from typing import Optional


class ScrapeRequest(BaseModel):
    url: str = Field(..., example="https://www.myntra.com/personal-care?f=Categories%3ALipstick")
    max_pages: Optional[int] = Field(default=5, ge=1, le=10)
    category_name: Optional[str] = Field(default="lipstick")

    @validator('url')
    def validate_myntra_url(cls, v):
        if "myntra.com" not in v.lower():
            raise ValueError("Only Myntra URLs are supported")
        return v.strip()

class ScrapeResponse(BaseModel):
    status: str
    products_count: int
    csv_download_url: str
    pages_scraped: int