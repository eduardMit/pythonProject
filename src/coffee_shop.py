class CoffeeShop:
    def __init__(self, data):
        self.location = data.get("A", "N/A")
        self.rating = data.get("Rating", "N/A")
        self.gps_address = data.get("GPS Address", "N/A")
        self.coffee_data = {k: int(v) for k, v in data.items() if k not in ("A", "Rating", "GPS Address")}
