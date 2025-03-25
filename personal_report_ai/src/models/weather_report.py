import requests
import json

class Weather:
    def __init__(self, latitude, longitude, num_day_forecast):
        self.latitude = latitude
        self.longitude = longitude
        self.num_day_forecast = num_day_forecast
    def NOAA_forecast(self):
        try:
            metadata_url = f"https://api.weather.gov/points/{self.latitude},{self.longitude}"
            metadata_response = requests.get(
                metadata_url,
                headers={"User-Agent": "WeatherReportAssistant/1.0"}
            )
            
            # Raise for exception error
            metadata_response.raise_for_status()
            metadata = metadata_response.json()
            
            # Extract the forecast URL from the meta data
            forecast_url = metadata["properties"]["forecast"]
            
            # Get the actual forcast data
            forecast_response = requests.get(
                forecast_url,
                headers={"User-Agent": "WeatherReportAssistant/1.0"}  # Add header here too
            )
            # Raise for exception error
            forecast_response.raise_for_status()
            return forecast_response.json()
        except Exception as e:
            print(f"Error fetching weather data: {e}")
            return None
            
    def NOAA_report(self):
        metadata = self.NOAA_forecast()
        if not metadata:
            return None
        
        seven_day_forecast = []
        metadata_day_forecast = metadata.get("properties", {}).get("periods", [])
        
        for period in metadata_day_forecast[:self.num_day_forecast]:
            day_forecast = {
                "name": period.get("name"),
                "startTime": period.get("startTime"),
                "temperature": period.get("temperature"),
                "temperatureUnit": period.get("temperatureUnit"),
                "precipitation": period.get("probabilityOfPrecipitation", {}).get("value"),  # Fixed nested structure
                "windSpeed": period.get("windSpeed"),
                "windDirection": period.get("windDirection"),
                "shortForecast": period.get("shortForecast"),
                "detailedForecast": period.get("detailedForecast")
            }
            seven_day_forecast.append(day_forecast)
        return seven_day_forecast
        
    def pretty_print_report(self):
        """Format and print the weather report in a readable format"""
        forecast_data = self.NOAA_report()
        
        if not forecast_data:
            print("Unable to retrieve weather data at this time.")
            return
            
        location_name = self.get_location_name()  # You might want to add this method
        
        print(f"\n📍 WEATHER FORECAST FOR {location_name or f'LAT: {self.latitude}, LON: {self.longitude}'}")
        print("=" * 60)
        
        for day in forecast_data:
            # Format the date/time
            if day.get("startTime"):
                try:
                    from datetime import datetime
                    start_time = datetime.fromisoformat(day["startTime"].replace("Z", "+00:00"))
                    formatted_date = start_time.strftime("%A, %B %d, %Y")
                except:
                    formatted_date = day.get("startTime", "N/A")
            else:
                formatted_date = "N/A"
                
            print(f"\n{day.get('name', 'Unknown')} - {formatted_date}")
            print("-" * 60)
            print(f"🌡️  Temperature: {day.get('temperature', 'N/A')}°{day.get('temperatureUnit', 'F')}")
            
            # Format precipitation chance
            precip = day.get('precipitation')
            if precip is not None:
                print(f"🌧️  Precipitation chance: {precip}%")
            else:
                print("🌧️  Precipitation chance: N/A")
                
            print(f"💨  Wind: {day.get('windSpeed', 'N/A')} {day.get('windDirection', '')}")
            print(f"☁️  Conditions: {day.get('shortForecast', 'N/A')}")
            print(f"\n{day.get('detailedForecast', '')}")
            
        print("\nData provided by the National Weather Service (weather.gov)")
    
    def get_location_name(self):
        """Get the location name from the NWS API"""
        try:
            metadata_url = f"https://api.weather.gov/points/{self.latitude},{self.longitude}"
            response = requests.get(
                metadata_url,
                headers={"User-Agent": "WeatherReportAssistant/1.0"}
            )
            response.raise_for_status()
            data = response.json()
            
            city = data.get("properties", {}).get("relativeLocation", {}).get("properties", {}).get("city")
            state = data.get("properties", {}).get("relativeLocation", {}).get("properties", {}).get("state")
            
            if city and state:
                return f"{city}, {state}"
            return None
        except:
            return None