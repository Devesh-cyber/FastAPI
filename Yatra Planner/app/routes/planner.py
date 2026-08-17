from fastapi import APIRouter, HTTPException
from app.model import TravelRequestModel
from app.service.places import fetch_places
from app.service.weather import fetch_weather
from app.service.currency import fetch_currency_rates
from app.service.cache import get_cache_stats, clear_cache
import asyncio

router = APIRouter(
    prefix='/plan',
    tags=['Travel Plan']
)


@router.post('/')
async def create_travel_plan(travel_request: TravelRequestModel):
    if travel_request.start_date > travel_request.end_date:
        raise HTTPException(
            status_code=400,
            detail="Start date cannot be after end date"
        )

    trip_days = (
        travel_request.end_date - travel_request.start_date
    ).days

    if trip_days < 1:
        raise HTTPException(
            status_code=400,
            detail="Travel plan must be at least 1 day long"
        )

    if trip_days > 14:
        raise HTTPException(
            status_code=400,
            detail="Travel plan cannot be longer than 14 days"
        )

    places, weather, currency_rates = await asyncio.gather(
    fetch_places(travel_request.destination),
    fetch_weather(
        destination=travel_request.destination,
        start_date=travel_request.start_date,
        end_date=travel_request.end_date
    ),
    fetch_currency_rates(travel_request.base_currency)
)

    return {
        "message": "Travel plan created successfully",
        "destination": travel_request.destination,
        "trip_days": trip_days,
        "places": places,
        "weather": weather,
        "currency_rates": currency_rates
    }


@router.get("/cache-stats")
async def cache_stats():

    return get_cache_stats()

@router.delete("/cache")
async def clear_cache_endpoint():

    clear_cache()

    return {
        "message": "Cache cleared successfully"
    }