import httpx
from datetime import date
from app.model import WeatherResponseModel
from app.service.cache import get_cache, set_cache

async def fetch_weather(
    destination: str,
    start_date: date,
    end_date: date
) -> list[WeatherResponseModel]:

    cache_key = f"weather_{destination}_{start_date}_{end_date}"

    cached_data = get_cache(cache_key)

    if cached_data is not None:
        return cached_data
    
    async with httpx.AsyncClient() as client:

        # 1. Find coordinates of destination
        geo_response = await client.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={
                "name": destination,
                "count": 1,
                "language": "en",
                "format": "json"
            }
        )

        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if not geo_data.get("results"):
            return []

        location = geo_data["results"][0]

        latitude = location["latitude"]
        longitude = location["longitude"]

        # 2. Get weather
        weather_response = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "daily": [
                    "weather_code",
                    "temperature_2m_max",
                    "temperature_2m_min",
                    "relative_humidity_2m_mean",
                    "precipitation_probability_max"
                ],
                "start_date": start_date,
                "end_date": end_date,
                "timezone": "auto"
            }
        )

        weather_response.raise_for_status()
        data = weather_response.json()

    forecasts = []

    daily = data["daily"]

    for i in range(len(daily["time"])):

        forecast = WeatherResponseModel(
            date=daily["time"][i],
            condition=str(daily["weather_code"][i]),
            temperature_high=daily["temperature_2m_max"][i],
            temperature_low=daily["temperature_2m_min"][i],
            humidity=daily["relative_humidity_2m_mean"][i],
            rain_chance=daily["precipitation_probability_max"][i]
        )

        forecasts.append(forecast)

    set_cache(
        cache_key,
        forecasts,
        ttl=3600
    )
    
    return forecasts