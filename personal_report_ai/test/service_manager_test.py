# test_service_manager.py
import time

# from service_manager import ServiceManager

# Create service manager
manager = ServiceManager()

# Testing Service Manager
try:
    # Test with weather service
    print("\n--- Testing weather service ---")
    weather_url = manager.ensure_service_running("weather")
    if weather_url:
        print(f"Weather service is available at: {weather_url}")
    
    # Wait a bit to see the service running
    time.sleep(5)
    
    # Test with news service
    print("\n--- Testing news service ---")
    news_url = manager.ensure_service_running("news")
    if news_url:
        print(f"News service is available at: {news_url}")
    
    time.sleep(5)
    
    # Test stopping a specific service
    print("\n--- Testing stop service ---")
    manager.stop_service("weather")
    
    time.sleep(2)
    
    # Test restarting a service
    print("\n--- Testing restart service ---")
    weather_url = manager.ensure_service_running("weather")
    if weather_url:
        print(f"Weather service restarted at: {weather_url}")
    
    time.sleep(5)

finally:
    # Always stop all services when done
    print("\n--- Stopping all services ---")
    manager.stop_all_services()