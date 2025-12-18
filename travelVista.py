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


def normalize(text):
    return re.sub(r"\s+", " ", text.strip().lower())

def detect_intent(message):
    for block in TRAVELVISTA_DATA:
        for keyword in block["keywords"]:
            if keyword in message:
                return block
    return None


def recommendation_flow(data):
    print(Fore.CYAN + "TravelVista: Preferred category? (beaches / mountains / cities / heritage)")
    choice = normalize(input(Fore.YELLOW + "You: "))
    if choice in data["categories"]:
        info = data["categories"][choice]
        destination = random.choice(info["places"])
        month = random.choice(info["best_months"])
        print(Fore.GREEN + f"TravelVista: Recommended destination → {destination}")
        print(Fore.GREEN + f"TravelVista: Ideal travel period → {month}")
    else:
        print(Fore.RED + "TravelVista: Category not supported")


def packing_flow(data):
    print(Fore.CYAN + "TravelVista: Trip duration in days?")
    try:
        days = int(input(Fore.YELLOW + "You: "))
    except:
        print(Fore.RED + "TravelVista: Invalid duration")
        return
    for rule in data["rules"]:
        if rule["min"] <= days <= rule["max"]:
            print(Fore.GREEN + "TravelVista: Suggested packing list:")
            for item in rule["items"]:
                print(Fore.GREEN + f"- {item}")
            return
    print(Fore.RED + "TravelVista: No applicable packing rule")
    
    
def budget_flow(data):
    print(Fore.CYAN + "TravelVista: Budget level? (low / medium / high)")
    level = normalize(input(Fore.YELLOW + "You: "))
    if level in data["levels"]:
        print(Fore.GREEN + f"TravelVista: {data['levels'][level]}")
    else:
        print(Fore.RED + "TravelVista: Invalid budget selection")

def weather_flow(data):
    print(Fore.CYAN + "TravelVista: Destination type?")
    category = normalize(input(Fore.YELLOW + "You: "))
    if category in data["guidance"]:
        print(Fore.GREEN + f"TravelVista: {data['guidance'][category]}")
    else:
        print(Fore.RED + "TravelVista: Weather guidance unavailable")
        

def joke_flow(data):
    print(Fore.YELLOW + f"TravelVista: {random.choice(data['responses'])}")

def show_help():
    print(Fore.MAGENTA + "\nTravelVista Capabilities:")
    print(Fore.GREEN + "- Destination recommendations")
    print(Fore.GREEN + "- Packing guidance")
    print(Fore.GREEN + "- Budget planning")
    print(Fore.GREEN + "- Weather insights")
    print(Fore.GREEN + "- Light humour")
    print(Fore.CYAN + "Type exit or bye to close the session\n")
