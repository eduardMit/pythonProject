import tkinter as tk
from tkinter import messagebox
from tkinter import*
from tkinter import simpledialog


def button_click(choice):
    if choice == 1:     # This button generate your random coffee.
        messagebox.showinfo("Random Coffee", f" {entry_name.get()}, your coffee for today is:")
    elif choice == 2:     # This button provides you with a coffee based on the selected rate.
        number = simpledialog.askfloat("Manual Coffe", f" {entry_name.get()} how good you want the coffee?(1-5)")
        if 1 <= number <= 5:
            messagebox.showinfo("Manual Coffe", f"Your coffee rated with {number} is:")
        else:
            messagebox.showinfo("Manual Coffe", "Your rate is incorrect please try again.")
    elif choice == 3:     # This button provides you with the best coffee according to our opinion.
        messagebox.showinfo("Best Coffee", f" {entry_name.get()} from our side the best coffe is:")
    elif choice == 4:     # This button shows you the locations of the best coffee places in the city of Sibiu.
        user_input = simpledialog.askstring("Locations", "Were do you want to drink your coffee today?")
        if user_input is not None:
            messagebox.showinfo("Locations", f"Please click on the link below for your coffee:")
        else:
            messagebox.showinfo("Locations", "Invalid location")


root = tk.Tk()
root.geometry("300x200")
img = PhotoImage(file="resources/coffeelogo2.png")
root.iconphoto(False, img)
root.title("Drink your coffee now")     # Create a window.

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
