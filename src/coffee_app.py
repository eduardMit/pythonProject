import json
import tkinter as tk
from tkinter import simpledialog, scrolledtext
import webbrowser
import random
import logging
from coffee_shop import CoffeeShop  # Importing the CoffeeShop class


# Decorator to handle exceptions and log errors
def try_except_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {e}")
            print(f"Error: {e}")

    return wrapper


# The main CoffeeApp class
class CoffeeApp:
    def __init__(self, json_file_path):
        # Initialize the Tkinter application
        self.root = tk.Tk()
        self.root.geometry("800x600")
        img = tk.PhotoImage(file="resources/coffeelogo2.png")
        self.root.iconphoto(False, img)
        self.root.title("Drink your coffee now")

        # Configure logging directly to the console
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        # Store the path to the JSON file
        self.json_file_path = json_file_path

        # Create the initial graphical interface
        self.create_initial_interface()

    # Decorated method to create the initial interface with buttons
    @try_except_decorator
    def create_initial_interface(self):
        self.clear_interface()

        frame = tk.Frame(self.root)
        frame.pack(expand=True)

        buttons = [
            ("Random Coffee", self.random_coffee),
            ("Manual Coffee", self.manual_coffee),
            ("Best Coffee", self.best_coffee),
            ("Locations", self.location_list)
        ]

        for i, (text, command) in enumerate(buttons):
            button = tk.Button(frame, text=text, command=command, font=("Arial", 16), height=2, width=15)
            button.grid(row=i // 2, column=i % 2, padx=20, pady=20)

    # Decorated method to clear the existing interface
    @try_except_decorator
    def clear_interface(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # Decorated method to display information with clickable URLs
    @try_except_decorator
    def display_info(self, info, try_again_command=None):
        self.clear_interface()

        scrolled_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=80, height=25)
        scrolled_text.insert(tk.END, info)
        scrolled_text.pack()

        url_pattern = r'https?://\S+'
        start = 1.0
        while True:
            match = scrolled_text.search(url_pattern, start, stopindex=tk.END)
            if not match:
                break
            start = f'{match.split(".")[0]}.end'
            end = scrolled_text.search(r'\s', start, stopindex=tk.END) or tk.END
            url = scrolled_text.get(match, end)
            scrolled_text.tag_add(url, match, end)
            scrolled_text.tag_config(url, foreground="blue", underline=True)
            scrolled_text.tag_bind(url, "<Button-1>", lambda e, link=url: self.open_url(link))

        button_frame = tk.Frame(self.root)
        button_frame.pack(side="bottom", pady=10)

        back_button = tk.Button(button_frame, text="Back", command=self.create_initial_interface, font=("Arial", 14))
        back_button.pack(side="left", padx=5)

        if try_again_command:
            try_again_button = tk.Button(button_frame, text="Try Again", command=try_again_command, font=("Arial", 14))
            try_again_button.pack(side="right", padx=5)

    # Decorated static method to open a URL in a browser
    @staticmethod
    @try_except_decorator
    def open_url(url):
        webbrowser.open(url)

    # Decorated method to filter coffee shops by rating
    @try_except_decorator
    def filter_coffee_by_rating(self, rating):
        with open(self.json_file_path, "r") as json_file:
            data = json.load(json_file)
            coffee_shops = [CoffeeShop(shop) for shop in data.get("Locations", [])]
            filtered_shops = [shop for shop in coffee_shops if
                              float(shop.rating) >= float(rating) and shop.location]

            try_again_command = self.manual_coffee
            if filtered_shops:
                coffee_info = f"Coffee Shops with Rating Equal or Greater than {rating}:\n\n"
                for shop in filtered_shops:
                    coffee_info += f"Location: {shop.location}\n"
                    for key, value in shop.coffee_data.items():
                        coffee_info += f"{key}: {value}\n"
                    coffee_info += "\n"
                self.display_info(coffee_info, try_again_command)
                self.log_and_print_success(f"Filtered coffee shops by rating {rating}")
            else:
                self.display_info(f"No coffee shops with rating equal or greater than {rating}.", try_again_command)
                self.log_and_print_error(f"No coffee shops with rating equal or greater than {rating}")

    # Decorated method to display information about a random coffee shop
    @try_except_decorator
    def random_coffee(self):
        with open(self.json_file_path, "r") as json_file:
            data = json.load(json_file)
            coffee_shops = data.get("Locations", [])
            if coffee_shops:
                random_shop = random.choice(coffee_shops)
                location = random_shop.get("A", "N/A")
                coffee_list = [k for k in random_shop.keys() if k not in ("A", "Rating", "GPS Address")]
                coffee_name = random.choice(coffee_list)
                rating = random_shop.get(coffee_name, "N/A")
                info_text = f"Random Coffee:\nLocation: {location}\nName: {coffee_name}\nRating: {rating}\n"
                try_again_command = self.random_coffee
                self.display_info(info_text, try_again_command)
                self.log_and_print_success("Displayed information about a random coffee shop")
            else:
                self.display_info("No coffee shop data available.")
                self.log_and_print_error("No coffee shop data available")

    # Decorated method to display information about the best coffee shops with a given rating
    @try_except_decorator
    def best_coffee_rating(self, rating):
        with open(self.json_file_path, "r") as json_file:
            data = json.load(json_file)
            coffee_shops = data.get("Locations", [])
            filtered_shops = [shop for shop in coffee_shops
                              if int(shop.get("Rating", 0)) >= int(rating) and shop.get("A") is not None]
            try_again_command = None
            if filtered_shops:
                coffee_info = f"Best locations:\n\n"
                for shop in filtered_shops:
                    location = shop.get("A", "N/A")
                    rating_values = {k: int(v) for k, v in shop.items()
                                     if k not in ("A", "Rating", "GPS Address") and int(v) >= int(rating)}
                    if rating_values:
                        coffee_info += f"Location: {location}\n"
                        for key, value in rating_values.items():
                            coffee_info += f"{key}: {value}\n"
                        coffee_info += "\n"
                self.display_info(coffee_info, try_again_command)
                self.log_and_print_success(f"Displayed information about best coffee shops with rating {rating}")
            else:
                self.display_info(f"No coffee shops with rating equal or greater than {rating}.", try_again_command)
                self.log_and_print_error(f"No coffee shops with rating equal or greater than {rating}")

    # Decorated method to get a manual coffee rating from the user and filter coffee shops
    @try_except_decorator
    def manual_coffee(self):
        rating = simpledialog.askinteger("Coffee Rating", "How good you want your coffee?(1-5):", minvalue=1,
                                         maxvalue=5)
        self.clear_interface()

        img = tk.PhotoImage(file="resources/coffeelogo2.png")
        self.root.iconphoto(False, img)

        if rating is not None:
            self.filter_coffee_by_rating(rating)
            self.log_and_print_success(f"Filtered coffee shops by rating {rating}")
        else:
            try_again_command = self.manual_coffee
            self.display_info("Please enter a valid rating.", try_again_command)
            self.log_and_print_error("Invalid rating entered")

    # Decorated method to display information about the best coffee shops with a predefined rating
    @try_except_decorator
    def best_coffee(self):
        rating = 4
        self.best_coffee_rating(rating)

    # Decorated method to display information about all coffee shop locations
    @try_except_decorator
    def location_list(self):
        with open(self.json_file_path, "r") as json_file:
            data = json.load(json_file)
            coffee_info = "Locations, Ratings, and GPS Addresses:\n\n"
            for coffee_shop in data["Locations"]:
                location = coffee_shop["A"]
                rating = coffee_shop["Rating"]
                gps_address = coffee_shop["GPS Address"]
                coffee_info += f"Location: {location}\nRating: {rating}\nGPS Address: {gps_address}\n\n"
            self.display_info(coffee_info)
            self.log_and_print_success("Displayed information about all coffee shop locations")

    # Decorated static method to log and print success messages
    @staticmethod
    @try_except_decorator
    def log_and_print_success(success_message):
        logging.info(success_message)
        print(success_message)

    # Decorated static method to log and print error messages
    @staticmethod
    @try_except_decorator
    def log_and_print_error(error_message):
        logging.error(error_message)
        print(f"Error: {error_message}")

    # Decorated method to start the Tkinter main loop
    @try_except_decorator
    def run(self):
        self.root.mainloop()


# Example usage
if __name__ == "__main__":
    # Create an instance of CoffeeApp and run the application
    app = CoffeeApp("your_json_file_path.json")
    app.run()
