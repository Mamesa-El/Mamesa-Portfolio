import requests
import json
from typing import List, Dict, Any
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models.weather_report import Weather

app = FastAPI(title = "Weather Reports")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response validation
class WeatherResponse(BaseModel):
    location:str
    forecast: List[Dict[str, Any]]
    
@app.get("/")
async def root():
    return {"message": "Welcome to the weather Report API."}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/weather/{lat},{long},{num_days_forecast}", response_model=WeatherResponse)
async def get_weather_report(lat: float, long: float, num_days_forecast: int):
    weather = Weather(lat, long, num_days_forecast)
    forecast = weather.NOAA_report()  # Use NOAA_report directly
    
    if not forecast:
        raise HTTPException(status_code=503, detail="Unable to retrieve weather data")
    
    location = weather.get_location_name()
    return {
        "location": location,
        "forecast": forecast
    }
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)  # Changed from 8000 to 8001

