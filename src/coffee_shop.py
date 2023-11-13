class CoffeeShop:
    def __init__(self, data):
        # Initialize attributes with default values if the corresponding keys are not present in the data
        self.location = data.get("A", "N/A")  # Location of the coffee shop
        self.rating = data.get("Rating", "N/A")  # Rating of the coffee shop
        self.gps_address = data.get("GPS Address", "N/A")  # GPS address of the coffee shop

        # Extract additional coffee data excluding keys "A", "Rating", and "GPS Address"
        # Convert values to integers using a dictionary comprehension
        self.coffee_data = {k: int(v) for k, v in data.items() if k not in ("A", "Rating", "GPS Address")}
