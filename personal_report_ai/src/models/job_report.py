import requests
import json

class JobReport:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://jsearch.p.rapidapi.com/search"
        
    def JobSearch(self, job_title, location=None, years_of_experience=None, field=None, date_posted=None):
        """
        Search for jobs using the JSearch API
        
        Parameters:
        - job_title: The job title to search for
        - location: Optional city, state, or country
        - years_of_experience: Optional experience level (e.g., "entry_level", "mid_level", "senior")
        - field: Optional field/industry (e.g., "technology", "finance")
        - date_posted: Optional time frame for when job was posted (e.g., "all", "today", "3days", "week", "month")
        
        Returns:
        - Dictionary containing job listings data
        """
        headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
        }
        
        # Build query string based on parameters
        query = job_title
        if field:
            query += f" {field}"
        
        params = {
            "query": query,
            "page": 1,
            "num_pages": 1
        }
        
        if location:
            params["location"] = location
        
        # Date posted filter
        if date_posted:
            params["date_posted"] = date_posted
        
        # Experience level mapping
        if years_of_experience:
            if years_of_experience in ["entry_level", "mid_level", "senior"]:
                exp_terms = {
                    "entry_level": "entry level junior",
                    "mid_level": "mid level",
                    "senior": "senior experienced"
                }
                query += f" {exp_terms[years_of_experience]}"
            else:
                query += f" {years_of_experience} years experience"
            
            params["query"] = query
        
        try:
            response = requests.get(self.base_url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            if "data" not in data:
                return {"jobs": [], "count": 0, "message": "No jobs found"}
            
            # Process and format job listings
            job_listings = []
            for job in data["data"]:
                # Format location safely
                city = job.get("job_city", "")
                country = job.get("job_country", "")
                location_str = ""
                
                if city:
                    location_str = city
                    if country:
                        location_str += f", {country}"
                elif country:
                    location_str = country
                else:
                    location_str = "Location not specified"
                
                # Build job data dictionary
                job_data = {
                    "job_id": job.get("job_id", ""),
                    "title": job.get("job_title", ""),
                    "company": job.get("employer_name", ""),
                    "location": location_str,
                    "description": job.get("job_description", "")[:300] + "..." if job.get("job_description") else "",
                    "salary": str(job.get("job_salary", job.get("job_min_salary", ""))) if job.get("job_salary") or job.get("job_min_salary") else None,                    "url": job.get("job_apply_link", ""),
                    "posted_at": job.get("job_posted_at_datetime_utc", ""),
                    "job_type": job.get("job_employment_type", "")
                }
                job_listings.append(job_data)
            
            return {
                "jobs": job_listings,
                "count": len(job_listings),
                "message": f"Found {len(job_listings)} jobs matching '{query}'"
            }
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching job data: {str(e)}")
            return {"jobs": [], "count": 0, "message": f"Error: {str(e)}"}
    
    def pretty_print_jobs(self, jobs_data):
        """
        Format and print job listings in a readable format
        
        Parameters:
        - jobs_data: Dictionary returned by the JobSearch method
        """
        if jobs_data["count"] == 0:
            print(jobs_data["message"])
            return
        
        print(f"\n📋 JOB SEARCH RESULTS: {jobs_data['message']}")
        print("=" * 80)
        
        for i, job in enumerate(jobs_data["jobs"], 1):
            print(f"\n{i}. {job['title']}")
            print("-" * 80)
            print(f"🏢 Company: {job['company']}")
            print(f"📍 Location: {job['location']}")
            
            if job['job_type']:
                print(f"💼 Type: {job['job_type']}")
                
            if job['salary']:
                print(f"💰 Salary: {job['salary']}")
                
            if job['posted_at']:
                print(f"📅 Posted: {job['posted_at']}")
                
            print(f"\n📝 Description: {job['description']}")
            print(f"\n🔗 Apply: {job['url']}")
            print("-" * 80)
        
        print(f"\nFound {jobs_data['count']} jobs matching your criteria.")