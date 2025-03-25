import requests
import json
from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models.job_report import JobReport

with open("../secrets.json") as f:
    secrets = json.load(f)
jsearch_api_key = secrets['jsearch_api_key']

jobsearch = JobReport(jsearch_api_key)

app = FastAPI(title = "Job Report")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class JobListing(BaseModel):
    job_id: str
    title: str
    company: str
    location: str
    description: Optional[str]
    salary: Optional[Union[str, int]] = None  # Accept either string or int
    url: Optional[str]
    posted_at: Optional[str]
    job_type: str

class JobResponse(BaseModel):
    result: List[JobListing]
    
@app.get("/")
async def root():
    return {"message": "Welcome to the jobs report API."}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/jobs", response_model=JobResponse)
async def get_jobs(
    job_title: str,
    location: Optional[str] = None,
    years_of_experience: Optional[str] = None,
    field: Optional[str] = None,
    date_posted: Optional[str] = None
):
    """
    Get job listings based on search criteria
    
    Parameters:
    - job_title: Job title to search for
    - location: Optional location (city, state, country)
    - years_of_experience: Optional experience level ("entry_level", "mid_level", "senior")
    - field: Optional field/industry (e.g., "machine learning", "data science")
    - date_posted: Optional time frame ("all", "today", "3days", "week", "month")
    """
    try:
        search_results = jobsearch.JobSearch(
            job_title=job_title,
            location=location,
            years_of_experience=years_of_experience,
            field=field,
            date_posted=date_posted
        )
        
        if search_results["count"] == 0:
            return {"result": []}
        
        job_listings = []
        for job in search_results["jobs"]:
            job_listings.append(JobListing(
                job_id=job["job_id"],
                title=job["title"],
                company=job["company"],
                location=job["location"],
                description=job.get("description"),
                salary=job.get("salary"),
                url=job.get("url"),
                posted_at=job.get("posted_at"),
                job_type=job.get("job_type", "Not specified")
            ))
        
        return {"result": job_listings}
    
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Error fetching job data: {str(e)}")
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)