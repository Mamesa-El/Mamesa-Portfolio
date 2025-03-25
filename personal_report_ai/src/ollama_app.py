import requests
import json
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Summary Report Assistant")

# Add CORS middleware to allow web clients to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ollama API configuration
OLLAMA_BASE_URL = "http://localhost:11434"
# Update this at the top of your file
MODEL_NAME = "vanilj/phi-4-unsloth:latest"  # Update with your Ollama model name

# Pydantic models for request/response validation
class Message(BaseModel):
    role: str
    content: str
    
class ChatRequest(BaseModel):
    messages: List[Message]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 1000
    stream: Optional[bool] = False

class ChatResponse(BaseModel):
    response: str
    model: str

class HealthResponse(BaseModel):
    status: str
    model: str
    
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Check if the API and Ollama service are running."""
    try:
        # Check if Ollama is accessible
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags")
        if response.status_code == 200:
            return {"status": "ok", "model": MODEL_NAME} 
        else:
            raise HTTPException(status_code=503, detail="Ollama service unavailable")
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Error connecting to Ollama: {str(e)}") 
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Process a chat request through Ollama."""
    try:
        # Format messages for Ollama API
        prompt = ""
        for msg in request.messages:
            if msg.role == "user":
                prompt += f"User: {msg.content}\n"
            elif msg.role == "assistant":
                prompt += f"Assistant: {msg.content}\n"
            elif msg.role == "system":
                prompt += f"System: {msg.content}\n"
                
        # Make request to Ollama
        ollama_request = {
            "model": "vanilj/phi-4-unsloth:latest",
            "prompt": prompt,
            "temperature": request.temperature,
            "num_predict": request.max_tokens,
            "stream": False
        }
        
        print(f"Sending request to Ollama: {ollama_request}")
        
        # Use streaming mode and collect the full response
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json=ollama_request,
            stream=True  # Always use streaming
        )
        
        print(f"Ollama response status: {response.status_code}")
        
        if response.status_code != 200:
            error_text = response.text
            print(f"Ollama error: {error_text}")
            raise HTTPException(
                status_code=response.status_code, 
                detail=f"Ollama API error: {error_text}"
            )
            
        # Collect the full response from the stream
        full_response = ""
        for line in response.iter_lines():
            if line:
                try:
                    chunk = json.loads(line)
                    text_chunk = chunk.get("response", "")
                    full_response += text_chunk
                    
                    # If done, break the loop
                    if chunk.get("done", False):
                        break
                except json.JSONDecodeError:
                    continue
        
        return {
            "response": full_response,
            "model": "vanilj/phi-4-unsloth:latest"
        }
        
    except requests.RequestException as e:
        print(f"Request exception: {str(e)}")
        raise HTTPException(status_code=503, detail=f"Connection error: {str(e)}")
    except Exception as e:
        import traceback
        print(f"Unexpected error: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
# @app.post("/chat", response_model=ChatResponse)
# async def chat(request: ChatRequest):
#     """Process a chat request through Ollama."""
#     try:
#         # Format messages for Ollama API
#         prompt = ""
#         for msg in request.messages:
#             if msg.role == "user":
#                 prompt += f"User: {msg.content}\n"
#             elif msg.role == "assistant":
#                 prompt += f"Assistant: {msg.content}\n"
#             elif msg.role == "system":
#                 prompt += f"System: {msg.content}\n"
                
#         # Make request to Ollama
#         ollama_request = {
#             "model": "vanilj/phi-4-unsloth:latest",  # Use the exact model name
#             "prompt": prompt,
#             "temperature": request.temperature,
#             "num_predict": request.max_tokens,
#             "stream": False
#         }
        
#         print(f"Sending request to Ollama: {ollama_request}")
        
#         response = requests.post(
#             f"{OLLAMA_BASE_URL}/api/generate",
#             json=ollama_request
#         )
        
#         print(f"Ollama response status: {response.status_code}")
        
#         if response.status_code != 200:
#             error_text = response.text
#             print(f"Ollama error: {error_text}")
#             raise HTTPException(
#                 status_code=response.status_code, 
#                 detail=f"Ollama API error: {error_text}"
#             )
            
#         result = response.json()
#         print(f"Ollama response: {result}")
        
#         return {
#             "response": result.get("response", ""),
#             "model": "vanilj/phi-4-unsloth:latest"
#         }
        
#     except requests.RequestException as e:
#         print(f"Request exception: {str(e)}")
#         raise HTTPException(status_code=503, detail=f"Connection error: {str(e)}")
#     except json.JSONDecodeError as e:
#         print(f"JSON decode error: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Invalid JSON response: {str(e)}")
#     except Exception as e:
#         import traceback
#         print(f"Unexpected error: {str(e)}")
#         print(traceback.format_exc())
#         raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    

@app.post("/stream-chat")
async def stream_chat(request: ChatRequest):
    """Stream a chat response from Ollama."""
    from fastapi.responses import StreamingResponse
    
    async def generate_stream():
        try:
            # Format messages for Ollama
            prompt = ""
            for msg in request.messages:
                if msg.role == "user":
                    prompt += f"User: {msg.content}\n"
                elif msg.role == "assistant":
                    prompt += f"Assistant: {msg.content}\n"
                elif msg.role == "system":
                    prompt += f"System: {msg.content}\n"
                    
            # Make streaming request to Ollama
            ollama_request = {
                "model": MODEL_NAME,
                "prompt": prompt,
                "temperature": request.temperature,
                "num_predict": request.max_tokens,
                "stream": True
            }
            
            with requests.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json=ollama_request,
                stream=True
            ) as response:
                if response.status_code != 200:
                    yield f"data: {json.dumps({'error': response.text})}\n\n"
                    return
                
                for line in response.iter_lines():
                    if line:
                        try:
                            chunk = json.loads(line)
                            text_chunk = chunk.get("response", "")
                            if text_chunk:
                                yield f"data: {json.dumps({'text': text_chunk})}\n\n"
                            # If 'done' is True, we've reached the end
                            if chunk.get("done", False):
                                break
                        except json.JSONDecodeError:
                            continue
                
                yield f"data: [DONE]\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream"
    )
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)