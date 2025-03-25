import os
import json
import time
import requests
import subprocess

class ServiceManager:
    def __init__(self, config_path = "api_services.json"):
        with open (config_path, "r") as f:
            self.config = json.load(f)
        self.services = {}
        self.running_processes = {}
    
    def ensure_service_running(self, service_name: str) -> str:
        "Ensure a service is running and return its base URL"
        if service_name not in self.config:
            raise ValueError(f"Unknown service: {service_name}")
        
        service_config = self.config[service_name]
        port = service_config["port"]
        base_url = f"http://localhost:{port}"
        
        try:
            response = requests.get(f"{base_url}/health")
            if response.status_code == 200:
                return base_url
        except requests.RequestException:
            pass
        
        # If the service is not running, we start it
        if service_name not in self.running_processes:
            app_module = service_config["app_module"]
            print(f"Starting {service_name} service on port {port}...")
            
            process = subprocess.Popen(
                ["uvicorn", f"{app_module}:app", "--port", str(port)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            self.running_processes[service_name] = process
            
            # Wait for the service to start
            for _ in range(10):
                time.sleep(2)
                try:
                    response = requests.get(f"{base_url}/health")
                    if response.status_code == 200:
                        print(f"{service_name} service is running now.")
                        return base_url
                except requests.RequestException:
                    continue
                
            print(f"Failed to start {service_name} service.")
            return None
        
        return base_url
        
    def stop_service(self, service_name):
        """Stop a specific service"""
        if service_name in self.running_processes:
            print(f"Stopping {service_name} service...")
            process = self.running_processes[service_name]
            process.terminate()
            try:
                process.wait(timeout=5)
                print(f"{service_name} service stopped")
            except subprocess.TimeoutExpired:
                print(f"Forcibly killing {service_name} service...")
                process.kill()
            del self.running_processes[service_name]
        else:
            print(f"{service_name} service is not running")
    
    def stop_all_services(self):
        """Stop all running services"""
        service_names = list(self.running_processes.keys())
        for name in service_names:
            self.stop_service(name)