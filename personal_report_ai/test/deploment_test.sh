# Updating the conda env with the packages and dependency from enviroment.yml
conda env update --file environment.yml

# Running test cases
python test.py

# Verifying that Ollama endpoint is working
curl -X GET "http://localhost:11434/api/tags"
# Health endpopint test
curl -X GET "http://127.0.0.1:8000/health" -H "accept: application/json"
# Chat endpoint test (window command prompt)
curl -X POST "http://127.0.0.1:8000/chat" -H "Content-Type: application/json" -d "{\"messages\":[{\"role\":\"user\",\"content\":\"Hello, how are you?\"}],\"temperature\":0.7,\"max_tokens\":100}"
# Stream Chat endpoint test (window command prompt)
curl -X POST "http://127.0.0.1:8000/stream-chat" -H "Content-Type: application/json" -d "{\"messages\":[{\"role\":\"user\",\"content\":\"Hello, how are you?\"}],\"temperature\":0.7,\"max_tokens\":100}"

# Weather Report API
uvicorn weather_app:app --port 8001

# News Report API
uvicorn news_app:app --port 8002
# Curl News Report Endpoint
curl -X GET "http://localhost:8001/news?keywords=technology&category=business&country=us&limit=5" -H "accept: application/json"

# Job Report API
uvicorn jobs_app:app --port 8003
# Curl Job Report Endpoint
curl -X GET "http://localhost:8003/jobs?job_title=Data%20Scientist&location=Seattle&field=machine%20learning&date_posted=week" -H "accept: application/json"

# Run the apps locally --> This code work only if we are in src/
uvicorn api:app --reload # --> Running the fastapi locally

streamlit run app.py # --> Running streamlit locally

docker build --no-cache -t math-tutor-bot -f deployments/Dockerfile .

