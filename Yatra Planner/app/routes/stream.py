import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.model import TravelRequestModel
from app.service.weather import fetch_weather
from app.service.places import fetch_places
from app.service.currency import fetch_currency_rates

router = APIRouter(
    prefix='/plan',
    tags=['Travel Plan Stream']
)

def format_sse(data, event=None):

    message = ''

    if event:
        message += f'event: {event}\n'

    message += f'data: {json.dumps(data, default=str)}\n\n'

    return message


async def stream_generator(travel_request: TravelRequestModel):
    yield format_sse(
        {
            "message": "Travel plan generation started"
        },
        event="start"
    )

    weather = await fetch_weather(
        destination=travel_request.destination,
        start_date=travel_request.start_date,
        end_date=travel_request.end_date
    )

    yield format_sse(
        {
            "weather": weather
        },
        event="weather"
    )

    places = await fetch_places(
        travel_request.destination
    )

    yield format_sse(
        {
            "places": places
        },
        event="places"
    )

    currency_rates = await fetch_currency_rates(
        travel_request.base_currency
    )

    yield format_sse(
        {
            "currency_rates": currency_rates
        },
        event="currency"
    )

    yield format_sse(
        {
            "message": "Travel plan generation completed"
        },
        event="complete"
    )


@router.get("/stream")
async def stream_travel_plan(
    destination: str,
    start_date: str,
    end_date: str,
    base_currency: str = "INR"
):
    travel_request = TravelRequestModel(
        destination=destination,
        start_date=start_date,
        end_date=end_date,
        base_currency=base_currency
    )

    if travel_request.start_date > travel_request.end_date:
        raise HTTPException(
            status_code=400,
            detail="Start date cannot be after end date"
        )

    trip_days = (
        travel_request.end_date - travel_request.start_date
    ).days + 1

    if trip_days < 1 or trip_days > 14:
        raise HTTPException(
            status_code=400,
            detail="Trip duration must be between 1 and 14 days"
        )

    return StreamingResponse(
        stream_generator(travel_request),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )