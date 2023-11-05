import json
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import webbrowser
import random


def random_coffee():
    try:
        with open("Coffee.json", "r") as json_file:
            data = json.load(json_file)
            coffee_shops = data.get("Locations", [])
            if coffee_shops:
                random_shop = random.choice(coffee_shops)
                location = random_shop.get("", "N/A")
                name = random_shop.get("Name", "N/A")
                rating = random_shop.get("Rating", "N/A")
                message = f"Random Coffee:\nLocation: {location}\nName: {name}\nRating: Rating: {rating}"
                messagebox.showinfo("Random Coffee", message)
            else:
                messagebox.showinfo("Random Coffee", "No coffee shop data available.")
    except FileNotFoundError:
        messagebox.showinfo("Error", "JSON file not found.")


def open_gps_link(gps_address):
    webbrowser.open(gps_address)


def create_gps_hyperlink(gps_address):
    gps_label = tk.Label(root, text=gps_address, fg="blue", cursor="hand2")
    gps_label.bind("<Button-1>", lambda e, link=gps_address: open_gps_link(link))
    return gps_label


def button_click(choice):
    if choice == 1:  # Random Coffee
        random_coffee()
    elif choice == 2:   # Manual Coffee
        number = simpledialog.askfloat("Manual Coffee", f"{entry_name.get()}, how good you want the coffee? (1-5)")
        if 1 <= number <= 5:
            messagebox.showinfo("Manual Coffee", f"Your coffee rated with {number} is:")
        else:
            messagebox.showinfo("Manual Coffee", "Your rate is incorrect, please try again.")
    elif choice == 3:   # Best Coffee
        messagebox.showinfo("Best Coffee", f"{entry_name.get()}, from our side, the best coffee is:")
    elif choice == 4:   # Locations
        try:
            with open("Coffee.json", "r") as json_file:
                data = json.load(json_file)
                coffee_info = "Locations, Ratings, and GPS Addresses:\n\n"
                for coffee_shop in data["Locations"]:
                    location = coffee_shop[""]
                    rating = coffee_shop["Rating"]
                    gps_address = coffee_shop["GPS Address"]
                    coffee_info += f"Location: {location}\nRating: {rating}\nGPS Address: {gps_address}\n\n"
                    gps_label = create_gps_hyperlink(gps_address)   # Create a clickable hyperlink for GPS Address
                    gps_label.pack()

                    coffee_info += "\n\n"

                messagebox.showinfo("Coffee Shops Info", coffee_info)
        except FileNotFoundError:
            messagebox.showinfo("Error", "JSON file not found.")
    else:
        messagebox.showinfo("Error", "Invalid choice")


root = tk.Tk()
root.geometry("640x360")
img = tk.PhotoImage(file="resources/coffeelogo2.png")
root.iconphoto(False, img)
root.title("Drink your coffee now")

name_label = tk.Label(root, text="Please insert your name:")
name_label.pack()

entry_name = tk.Entry(root)
entry_name.pack()

button_random_coffee = tk.Button(root, text="Random Coffee", command=lambda: button_click(1))
button_manual_coffee = tk.Button(root, text="Manual Coffee", command=lambda: button_click(2))
button_best_coffee = tk.Button(root, text="Best Coffee", command=lambda: button_click(3))
button_location = tk.Button(root, text="Locations", command=lambda: button_click(4))

button_random_coffee.pack()
button_manual_coffee.pack()
button_best_coffee.pack()
button_location.pack()

root.mainloop()
