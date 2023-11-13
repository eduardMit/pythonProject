import json
import tkinter as tk
from tkinter import simpledialog, scrolledtext
import webbrowser
import random
import logging


class CoffeeApp:
    def __init__(self):
        # Initialize the Tkinter application
        self.root = tk.Tk()
        self.root.geometry("800x600")
        img = tk.PhotoImage(file="resources/coffeelogo2.png")
        self.root.iconphoto(False, img)
        self.root.title("Drink your coffee now")

        # Configure logging directly to the console
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        # Create the initial graphical interface
        self.create_initial_interface()

    def create_initial_interface(self):
        # Clear the existing interface
        self.clear_interface()

        # Create a frame for better organization
        frame = tk.Frame(self.root)
        frame.pack(expand=True)

        # Create buttons for different functionalities
        button_random_coffee = tk.Button(frame, text="Random Coffee",
                                         command=self.random_coffee, font=("Arial", 16), height=2, width=15)
        button_random_coffee.grid(row=0, column=0, padx=20, pady=20)

        button_manual_coffee = tk.Button(frame, text="Manual Coffee",
                                         command=self.manual_coffee, font=("Arial", 16), height=2, width=15)
        button_manual_coffee.grid(row=0, column=1, padx=20, pady=20)

        button_best_coffee = tk.Button(frame, text="Best Coffee",
                                       command=self.best_coffee, font=("Arial", 16), height=2, width=15)
        button_best_coffee.grid(row=1, column=0, padx=20, pady=20)

        button_location = tk.Button(frame, text="Locations",
                                    command=self.location_list, font=("Arial", 16), height=2, width=15)
        button_location.grid(row=1, column=1, padx=20, pady=20)

    def clear_interface(self):
        # Destroy all widgets in the interface
        for widget in self.root.winfo_children():
            widget.destroy()

    def display_info(self, info, try_again_command=None):
        # Clear the existing interface
        self.clear_interface()

        # Add a scrolled text with the desired information
        scrolled_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=80, height=25)
        scrolled_text.insert(tk.END, info)
        scrolled_text.pack()

        # Add web links and configure them to open in a browser
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

        # Add a frame for navigation buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(side="bottom", pady=10)

        # Add the "Back" button
        back_button = tk.Button(button_frame, text="Back", command=self.create_initial_interface, font=("Arial", 14))
        back_button.pack(side="left", padx=5)

        # Add the "Try Again" button if specified
        if try_again_command:
            try_again_button = tk.Button(button_frame, text="Try Again", command=try_again_command, font=("Arial", 14))
            try_again_button.pack(side="right", padx=5)

    def open_url(self, url):
        # Function to open a URL in a browser
        webbrowser.open(url)

    def filter_coffee_by_rating(self, rating):
        try:
            with open("src/Coffee.json", "r") as json_file:
                # Load data from the JSON file
                data = json.load(json_file)
                coffee_shops = data.get("Locations", [])
                filtered_shops = [shop for shop in coffee_shops
                                  if float(shop.get("Rating", 0)) >= float(rating) and shop.get("A") is not None]

                try_again_command = self.manual_coffee
                if filtered_shops:
                    # Build a string of information for display
                    coffee_info = f"Coffee Shops with Rating Equal or Greater than {rating}:\n\n"
                    for shop in filtered_shops:
                        location = shop.get("A", "N/A")
                        rating_values = {k: int(v) for k, v in shop.items()
                                         if k not in ("A", "Rating", "GPS Address") and int(v) >= int(rating)}
                        if rating_values:
                            coffee_info += f"Location: {location}\n"
                            for key, value in rating_values.items():
                                coffee_info += f"{key}: {value}\n"
                            coffee_info += "\n"
                    # Display the information in the interface
                    self.display_info(coffee_info, try_again_command)
                    self.log_and_print_success(f"Filtered coffee shops by rating {rating}")
                else:
                    # Display a message if there are no coffee shops matching the criteria
                    self.display_info(f"No coffee shops with rating equal or greater than {rating}.", try_again_command)
                    self.log_and_print_error(f"No coffee shops with rating equal or greater than {rating}")
        except FileNotFoundError as e:
            # Display an error message if the file is not found
            self.log_and_print_error(f"JSON file not found: {e}")

    def random_coffee(self):
        try:
            with open("src/Coffee.json", "r") as json_file:
                # Load data from the JSON file
                data = json.load(json_file)
                coffee_shops = data.get("Locations", [])
                if coffee_shops:
                    # Choose a random coffee shop
                    random_shop = random.choice(coffee_shops)
                    location = random_shop.get("A", "N/A")
                    coffee_list = [k for k in random_shop.keys() if k not in ("A", "Rating", "GPS Address")]
                    coffee_name = random.choice(coffee_list)
                    rating = random_shop.get(coffee_name, "N/A")
                    # Build a string of information for display
                    info_text = f"Random Coffee:\nLocation: {location}\nName: {coffee_name}\nRating: {rating}\n"
                    try_again_command = self.random_coffee
                    # Display the information in the interface
                    self.display_info(info_text, try_again_command)
                    self.log_and_print_success("Displayed information about a random coffee shop")
                else:
                    # Display a message if there is no coffee shop data available
                    self.display_info("No coffee shop data available.")
                    self.log_and_print_error("No coffee shop data available")
        except FileNotFoundError as e:
            # Display an error message if the file is not found
            self.log_and_print_error(f"JSON file not found: {e}")

    def best_coffee_rating(self, rating):
        try:
            with open("src/Coffee.json", "r") as json_file:
                # Load data from the JSON file
                data = json.load(json_file)
                coffee_shops = data.get("Locations", [])
                filtered_shops = [shop for shop in coffee_shops
                                  if int(shop.get("Rating", 0)) >= int(rating) and shop.get("A") is not None]
                try_again_command = None  # No try again for best coffee
                if filtered_shops:
                    # Build a string of information for display
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
                    # Display the information in the interface
                    self.display_info(coffee_info, try_again_command)
                    self.log_and_print_success(f"Displayed information about best coffee shops with rating {rating}")
                else:
                    # Display a message if there are no coffee shops matching the criteria
                    self.display_info(f"No coffee shops with rating equal or greater than {rating}.", try_again_command)
                    self.log_and_print_error(f"No coffee shops with rating equal or greater than {rating}")
        except FileNotFoundError as e:
            # Display an error message if the file is not found
            self.log_and_print_error(f"JSON file not found: {e}")

    def manual_coffee(self):
        try:
            # Get the rating from the user using a dialog window
            rating = simpledialog.askinteger("Coffee Rating", "How good you want your coffe?(1-5):", minvalue=1, maxvalue=5)

            # Clear the existing interface
            self.clear_interface()

            # Set the same logo as in the initial window
            img = tk.PhotoImage(file="resources/coffeelogo2.png")
            self.root.iconphoto(False, img)

            if rating is not None:
                # Filter coffee shops based on rating
                self.filter_coffee_by_rating(rating)
                self.log_and_print_success(f"Filtered coffee shops by rating {rating}")
            else:
                # Display a message if an invalid rating is entered
                try_again_command = self.manual_coffee
                self.display_info("Please enter a valid rating.", try_again_command)
                self.log_and_print_error("Invalid rating entered")
        except Exception as e:
            # Display an error message if an unexpected exception occurs
            self.log_and_print_error(f"Error: {e}")

    def best_coffee(self):
        # Set the minimum rating for best coffee
        rating = 4
        self.best_coffee_rating(rating)

    def location_list(self):
        try:
            with open("src/Coffee.json", "r") as json_file:
                # Load data from the JSON file
                data = json.load(json_file)
                coffee_info = "Locations, Ratings, and GPS Addresses:\n\n"
                for coffee_shop in data["Locations"]:
                    location = coffee_shop["A"]
                    rating = coffee_shop["Rating"]
                    gps_address = coffee_shop["GPS Address"]
                    # Build a string of information for display
                    coffee_info += f"Location: {location}\nRating: {rating}\nGPS Address: {gps_address}\n\n"
                # Display the information in the interface
                self.display_info(coffee_info)
                self.log_and_print_success("Displayed information about all coffee shop locations")
        except FileNotFoundError as e:
            # Display an error message if the file is not found
            self.log_and_print_error(f"JSON file not found: {e}")

    def log_and_print_success(self, success_message):
        # Log and print a success message
        logging.info(success_message)
        print(success_message)

    def log_and_print_error(self, error_message):
        # Log and print an error message
        logging.error(error_message)
        print(f"Error: {error_message}")

    def run(self):
        # Start the main Tkinter loop
        self.root.mainloop()


if __name__ == "__main__":
    # Initialize and run the CoffeeApp application
    coffee_app = CoffeeApp()
    coffee_app.run()
