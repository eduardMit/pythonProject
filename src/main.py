from coffee_app import CoffeeApp
import os

# Entry point for the script
if __name__ == "__main__":
    # Initialize and run the CoffeeApp application
    json_file_path = os.path.join("src", "Coffee.json")
    coffee_app = CoffeeApp(json_file_path)
    coffee_app.run()