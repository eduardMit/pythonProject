from coffee_app import CoffeeApp
import os

# Entry point for the script
if __name__ == "__main__":
    # Get the absolute path to the JSON file
    script_directory = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(script_directory, "src", "Coffee.json")

    # Initialize and run the CoffeeApp application
    coffee_app = CoffeeApp(json_file_path)
    coffee_app.run()
