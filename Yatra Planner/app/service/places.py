from app.model import PlaceModel


PLACES_DATABASE = {
    'goa' : [
        PlaceModel(
            name='Baga Beach',
            description= 'A popular beach in goa known for nighlife and water sports',
            category= 'Beach',
            rating= 4.5,
            estimated_time_hours=3
        ),
        PlaceModel(
            name="Fort Aguada",
            description="A well-preserved 17th-century Portuguese fort overlooking the Arabian Sea",
            category="Historical Site",
            rating=4.7,
            estimated_time_hours=2,
            entry_fee=10.0,
        ),
    ],
    
    "manali": [
        PlaceModel(
            name="Solang Valley",
            description="A beautiful valley known for its adventure sports and scenic views",
            category="Nature",
            rating=4.5,
            estimated_time_hours=4,
        ),
        PlaceModel(
            name="Hadimba Temple",
            description="An ancient cave temple surrounded by cedar forests",
            category="Religious Site",
            rating=4.6,
            estimated_time_hours=1,
        ),
    ],
}


async def fetch_places(destination: str) -> list[PlaceModel]:
    return PLACES_DATABASE.get(destination.lower(), [])