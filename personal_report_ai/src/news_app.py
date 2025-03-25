import requests
import json
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from models.news_report import NewsService

with open("../secrets.json") as f:
    secrets = json.load(f)
api_key = secrets['mediastack_api_key']

news_service = NewsService(api_key)

app = FastAPI(title = "News Report")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NewsArticle(BaseModel):
    title: str
    description: Optional[str] = None
    url: str
    source: str
    published_at: datetime
    category: Optional[str] = None
    image_url: Optional[str] = None

class NewsResponse(BaseModel):
    meta_info: str
    news: List[NewsArticle]
    
@app.get("/")
async def root():
    return {"message": "Welcome to news report API."}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/news", response_model = NewsResponse)
async def get_news(
    keywords: Optional[str] = None,
    category: Optional[str] = None,
    country: Optional[str] = None,
    limit: int = 10
):
    news_data = news_service.MediaStack_get_news(
        keywords=keywords,
        categories=category,
        countries =country,
        limit=limit
        )
    if not news_data or "data" not in news_data:
        raise HTTPException(status_code = 503, detail = "Unable to retrieve news data")
    articles = []
    
    for item in news_data["data"]:
        articles.append(NewsArticle(
            title=item.get("title", ""),
            description=item.get("description"),
            url=item.get("url", ""),
            source=item.get("source", ""),
            published_at=item.get("published_at"),
            category=item.get("category"),
            image_url=item.get("image")
        ))
        
    return NewsResponse(
        meta_info=f"Retrieved {len(articles)} articles",
        news=articles
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)