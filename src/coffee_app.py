import json
import tkinter as tk
import webbrowser
from tkinter import simpledialog, scrolledtext
import re
import random
import logging
from coffee_shop import CoffeeShop  # Assuming you have a CoffeeShop class defined in a separate module


# Exception handling decorator
def exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"An exception occurred in {func.__name__}: {e}")
    return wrapper


# CoffeeApp class representing the main application
class CoffeeApp:
    def __init__(self, json_file_path):
        self.root = tk.Tk()
        self.root.geometry("800x600")
        img = tk.PhotoImage(file="resources/coffeelogo2.png")
        self.root.iconphoto(False, img)
        self.root.title("Drink your coffee now")

        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        self.json_file_path = json_file_path
        self.create_initial_interface()

    @exception_handler
    def create_initial_interface(self):
        # Create the initial user interface
        self.clear_interface()

        frame = tk.Frame(self.root)
        frame.pack(expand=True)

        # Define buttons with corresponding text and command functions
        buttons = [
            ("Random Coffee", self.random_coffee),
            ("Manual Coffee", self.manual_coffee),
            ("Best Coffee", self.best_coffee),
            ("Locations", self.location_list)
        ]

        for i, (text, command) in enumerate(buttons):
            button = tk.Button(frame, text=text, command=command, font=("Arial", 16), height=2, width=15)
            button.grid(row=i // 2, column=i % 2, padx=20, pady=20)

    @exception_handler
    def clear_interface(self):
        # Clear the user interface
        for widget in self.root.winfo_children():
            widget.destroy()

    @exception_handler
    def display_info(self, info, try_again_command=None, urls=None):
        # Display information in a scrolled text widget with clickable URLs
        self.clear_interface()

        scrolled_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=80, height=25)
        scrolled_text.insert(tk.END, info)
        scrolled_text.pack()

        # Make URLs clickable in the scrolled text
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
            scrolled_text.tag_bind(url, "<Button-1>", lambda e, link=url: self.open_browser(link))

        # Add Back and Try Again buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(side="bottom", pady=10)

        back_button = tk.Button(button_frame, text="Back", command=self.create_initial_interface, font=("Arial", 14))
        back_button.pack(side="left", padx=5)

        if try_again_command:
            try_again_button = tk.Button(button_frame, text="Try Again", command=try_again_command, font=("Arial", 14))
            try_again_button.pack(side="right", padx=5)

        if urls:
            # Add "Click Here" buttons for each URL
            for i, url in enumerate(urls):
                click_button = tk.Button(button_frame, text=f"Click Here {i + 1}",
                                         command=lambda u=url: self.open_browser(u), font=("Arial", 14))
                click_button.pack(side="left", padx=5)

    @exception_handler
    def open_browser(self, url):
        # Open a web browser with the provided URL
        webbrowser.open(url)

    @exception_handler
    def filter_coffee_by_rating(self, rating):
        # Filter coffee shops by rating
        try:
            with open(self.json_file_path, "r") as json_file:
                data = json.load(json_file)
                coffee_shops = [CoffeeShop(shop) for shop in data.get("Locations", [])]
                filtered_shops = [shop for shop in coffee_shops if
                                  float(shop.rating) >= float(rating) and shop.location]

                try_again_command = self.manual_coffee
                if filtered_shops:
                    coffee_info = f"Coffee Shops with Rating Equal or Greater than {rating}:\n\n"
                    urls = []

                    for shop in filtered_shops:
                        coffee_info += f"Location: {shop.location}\n"
                        for key, value in shop.coffee_data.items():
                            coffee_info += f"{key}: {value}\n"

                        # Check if the shop has a GPS Address with a valid URL
                        gps_address = shop.coffee_data.get("GPS Address", "")
                        url_match = re.search(r'https?://\S+', gps_address)
                        if url_match:
                            url_to_open = url_match.group()
                            urls.append(url_to_open)
                            coffee_info += f"GPS Address: {gps_address}\n\n"

                    self.display_info(coffee_info, try_again_command, urls)
                    logging.info(f"Filtered coffee shops by rating {rating}")
                else:
                    self.display_info(f"No coffee shops with rating equal or greater than {rating}.", try_again_command)
                    logging.error(f"No coffee shops with rating equal or greater than {rating}")
        except FileNotFoundError as e:
            logging.error(f"JSON file not found: {e}")

    @exception_handler
    def random_coffee(self):
        # Display information about a random coffee shop
        try:
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
                    logging.info("Displayed information about a random coffee shop")
                else:
                    self.display_info("No coffee shop data available.")
                    logging.error("No coffee shop data available")
        except FileNotFoundError as e:
            logging.error(f"JSON file not found: {e}")

    @exception_handler
    def best_coffee_rating(self, rating):
        # Display information about the best coffee shops based on rating
        try:
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
                    logging.info(f"Displayed information about best coffee shops with rating {rating}")
                else:
                    self.display_info(f"No coffee shops with rating equal or greater than {rating}.", try_again_command)
                    logging.error(f"No coffee shops with rating equal or greater than {rating}")
        except FileNotFoundError as e:
            logging.error(f"JSON file not found: {e}")

    @exception_handler
    def manual_coffee(self):
        # Ask the user for a coffee rating and filter coffee shops based on that rating
        try:
            rating = simpledialog.askinteger("Coffee Rating", "How good you want your coffee?(1-5):", minvalue=1,
                                             maxvalue=5)
            self.clear_interface()

            img = tk.PhotoImage(file="resources/coffeelogo2.png")
            self.root.iconphoto(False, img)

            if rating is not None:
                self.filter_coffee_by_rating(rating)
                logging.info(f"Filtered coffee shops by rating {rating}")
            else:
                try_again_command = self.manual_coffee
                self.display_info("Please enter a valid rating.", try_again_command)
                logging.error("Invalid rating entered")
        except Exception as e:
            logging.error(f"Error: {e}")

    @exception_handler
    def best_coffee(self):
        # Display information about the best coffee shops with a predefined rating
        rating = 4
        self.best_coffee_rating(rating)

    @exception_handler
    def location_list(self):
        # Hide the initial interface
        self.clear_interface()

        try:
            with open(self.json_file_path, "r") as json_file:
                data = json.load(json_file)
                coffee_shops = data.get("Locations", [])
                urls = []

                # Create a frame for the "Click Here" buttons and the "Back" button
                button_frame = tk.Frame(self.root)
                button_frame.pack(expand=True)

                for i in range(0, len(coffee_shops), 2):
                    coffee_shop_1 = coffee_shops[i]
                    coffee_shop_2 = coffee_shops[i + 1] if i + 1 < len(coffee_shops) else None

                    location_1 = coffee_shop_1.get("A", f"Location {i + 1}")
                    gps_address_1 = coffee_shop_1.get("GPS Address", "")
                    url_match_1 = re.search(r'https?://\S+', gps_address_1)
                    if url_match_1:
                        url_to_open_1 = url_match_1.group()
                        urls.append(url_to_open_1)

                    # Add "Click Here" button for the first location
                    button_1 = tk.Button(button_frame, text=f"{location_1}",
                                         command=lambda u=gps_address_1: self.open_browser(u), font=("Arial", 14))
                    button_1.grid(row=i // 2, column=0, padx=5, pady=5)

                    if coffee_shop_2:
                        location_2 = coffee_shop_2.get("A", f"Location {i + 2}")
                        gps_address_2 = coffee_shop_2.get("GPS Address", "")
                        url_match_2 = re.search(r'https?://\S+', gps_address_2)
                        if url_match_2:
                            url_to_open_2 = url_match_2.group()
                            urls.append(url_to_open_2)

                        # Add "Click Here" button for the second location
                        button_2 = tk.Button(button_frame, text=f"{location_2}",
                                             command=lambda u=gps_address_2: self.open_browser(u), font=("Arial", 14))
                        button_2.grid(row=i // 2, column=1, padx=5, pady=5)

                # Add "Back" button to return to the initial interface
                back_button = tk.Button(button_frame, text="Back", command=self.create_initial_interface,
                                        font=("Arial", 14))
                back_button.grid(row=(len(coffee_shops) - 1) // 2 + 1, column=0, columnspan=2, pady=10)

                logging.info("Displayed 'Click Here' buttons for all coffee shop locations")

        except FileNotFoundError as e:
            logging.error(f"JSON file not found: {e}")

    @exception_handler
    def run(self):
        # Run the main Tkinter event loop
        self.root.mainloop()


# Main block for script execution
if __name__ == "__main__":
    # Example usage:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    coffee_app = CoffeeApp("Coffee.json")
    coffee_app.run()
