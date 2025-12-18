import re, random
from colorama import Fore, init

init(autoreset=True)

TRAVELVISTA_DATA = [
    {
        "intent": "recommendation",
        "keywords": ["recommend", "suggest", "destination", "travel"],
        "categories": {
            "beaches": {
                "places": ["Bali", "Maldives", "Phuket", "Goa"],
                "best_months": ["November", "December", "January"]
            },
            "mountains": {
                "places": ["Himalayas", "Swiss Alps", "Rocky Mountains"],
                "best_months": ["March", "April", "October"]
            },
            "cities": {
                "places": ["Tokyo", "Paris", "New York", "Dubai"],
                "best_months": ["February", "March", "September"]
            },
            "heritage": {
                "places": ["Rome", "Athens", "Cairo"],
                "best_months": ["January", "February", "November"]
            }
        }
    },
    {
        "intent": "packing",
        "keywords": ["packing", "pack", "luggage"],
        "rules": [
            {"min": 1, "max": 3, "items": ["Basic clothing", "Phone charger", "Toiletries"]},
            {"min": 4, "max": 7, "items": ["Extra outfits", "Comfort shoes", "Power bank"]},
            {"min": 8, "max": 30, "items": ["Laundry kit", "Adapters", "Medicines"]}
        ]
    },
    {
        "intent": "budget",
        "keywords": ["budget", "cost", "expense"],
        "levels": {
            "low": "Public transport and budget accommodation",
            "medium": "Balanced comfort and cost efficiency",
            "high": "Premium hotels and private transport"
        }
    },
    {
        "intent": "weather",
        "keywords": ["weather", "climate", "season"],
        "guidance": {
            "beaches": "Warm climate, sunscreen recommended",
            "mountains": "Cold conditions, jackets required",
            "cities": "Moderate weather, layered clothing advised"
        }
    },
    {
        "intent": "joke",
        "keywords": ["joke", "funny", "laugh"],
        "responses": [
            "Why did the traveller bring a pencil? To draw conclusions.",
            "Why don’t suitcases panic? They are well handled.",
            "Why did the map feel confident? It knew the route."
        ]
    }
]
