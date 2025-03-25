import requests
import subprocess
import time
import os
import platform

class BrainManager:
    def __init__(self, ollama_url="http://localhost:11434", api_url="http://localhost:8000"):
        self.ollama_url = ollama_url  # Direct Ollama URL
        self.api_url = api_url        # Your FastAPI wrapper URL
        self.ollama_process = None
        self.api_process = None
    
    def ensure_ollama_running(self):
        """Ensure Ollama is running, start it if needed"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=3)
            if response.status_code == 200:
                print("Ollama service is already running")
                return True
        except requests.RequestException:
            print("Ollama is not running, will start it")
            
            # Start Ollama based on platform
            try:
                if platform.system() == "Windows":
                    ollama_path = os.path.expanduser("~\\AppData\\Local\\Programs\\Ollama\\ollama.exe")
                    if not os.path.exists(ollama_path):
                        print(f"Ollama executable not found at {ollama_path}")
                        return False
                    
                    self.ollama_process = subprocess.Popen(
                        [ollama_path, "serve"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                else:
                    # Linux/Mac
                    self.ollama_process = subprocess.Popen(
                        ["ollama", "serve"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                
                # Wait for Ollama to start
                for attempt in range(1, 11):
                    print(f"Waiting for Ollama to start (attempt {attempt}/10)...")
                    time.sleep(3)
                    try:
                        response = requests.get(f"{self.ollama_url}/api/tags", timeout=3)
                        if response.status_code == 200:
                            print("Ollama service is now running")
                            return True
                    except requests.RequestException:
                        continue
                
                print("Failed to start Ollama service")
                return False
            except Exception as e:
                print(f"Error starting Ollama: {str(e)}")
                return False
                
        return True
    
    def ensure_api_running(self):
        """Ensure FastAPI wrapper is running, start it if needed"""
        try:
            response = requests.get(f"{self.api_url}/health", timeout=3)
            if response.status_code == 200:
                print("API wrapper is already running")
                return True
        except requests.RequestException:
            print("API wrapper is not running, will start it")
            
            # First ensure Ollama is running since the API depends on it
            if not self.ensure_ollama_running():
                print("Cannot start API wrapper because Ollama failed to start")
                return False
            
            # Start the FastAPI wrapper
            try:
                # Adjust the path to your FastAPI wrapper script
                api_script_path = "ollama_app.py"  # Change to your actual script name
                
                self.api_process = subprocess.Popen(
                    ["uvicorn", f"{api_script_path.replace('.py', '')}:app", "--host", "0.0.0.0", "--port", "8000"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                
                # Wait for API to start
                for attempt in range(1, 11):
                    print(f"Waiting for API wrapper to start (attempt {attempt}/10)...")
                    time.sleep(2)
                    try:
                        response = requests.get(f"{self.api_url}/health", timeout=3)
                        if response.status_code == 200:
                            print("API wrapper is now running")
                            return True
                    except requests.RequestException:
                        continue
                
                print("Failed to start API wrapper")
                return False
            except Exception as e:
                print(f"Error starting API wrapper: {str(e)}")
                return False
                
        return True
    
    def ensure_services_running(self):
        """Ensure both Ollama and API wrapper are running"""
        if not self.ensure_ollama_running():
            return False
        
        if not self.ensure_api_running():
            return False
            
        return True
    
    def stop_services(self):
        """Stop all services that were started by this manager"""
        print("stop_services method called")
        
        # Stop API wrapper first (since it depends on Ollama)
        print(f"API process status: {self.api_process is not None}")
        if self.api_process:
            print("Stopping API wrapper...")
            self.api_process.terminate()
            try:
                self.api_process.wait(timeout=5)
                print("API wrapper stopped")
            except subprocess.TimeoutExpired:
                print("Forcibly killing API wrapper...")
                self.api_process.kill()
            self.api_process = None
        else:
            print("No API process to stop (it was None)")
        
        # Then stop Ollama
        print(f"Ollama process status: {self.ollama_process is not None}")
        if self.ollama_process:
            print("Stopping Ollama service...")
            self.ollama_process.terminate()
            try:
                self.ollama_process.wait(timeout=10)
                print("Ollama service stopped")
            except subprocess.TimeoutExpired:
                print("Forcibly killing Ollama service...")
                self.ollama_process.kill()
            self.ollama_process = None
        else:
            print("No Ollama process to stop (it was None)")
            
    def force_stop_all_services(self):
        """Force stop Ollama and API services regardless of who started them"""
        # Try to find and kill the API process
        import subprocess
        import platform
        
        if platform.system() == "Windows":
            # Windows command to kill processes
            try:
                subprocess.run(["taskkill", "/f", "/im", "python.exe"], capture_output=True)
                print("Attempted to stop API wrapper")
            except Exception as e:
                print(f"Error stopping API: {e}")
                
            try:
                subprocess.run(["taskkill", "/f", "/im", "ollama.exe"], capture_output=True)
                print("Attempted to stop Ollama")
            except Exception as e:
                print(f"Error stopping Ollama: {e}")
        else:
            # Linux/Mac command to kill processes
            try:
                subprocess.run(["pkill", "-f", "uvicorn"], capture_output=True)
                print("Attempted to stop API wrapper")
            except Exception as e:
                print(f"Error stopping API: {e}")
                
            try:
                subprocess.run(["pkill", "-f", "ollama"], capture_output=True)
                print("Attempted to stop Ollama")
            except Exception as e:
                print(f"Error stopping Ollama: {e}")