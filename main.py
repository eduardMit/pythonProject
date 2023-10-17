import tkinter as tk
from tkinter import messagebox


def button_click(choice):
    if choice == 1:
        messagebox.showinfo("Choice", f" {entry_name.get()}, your coffee for today is:")
    elif choice == 2:
        messagebox.showinfo("Choice", f" {entry_name.get()} how good you want the coffee? (1-5)")
    elif choice == 3:
        messagebox.showinfo("Choice", f" Like, share and drink coffee, because this is keeping us alive !")


root = tk.Tk()
root.title("Drink your coffee now")  # Create a window

name_label = tk.Label(root, text="Please insert your name:")
name_label.pack()

entry_name = tk.Entry(root)
entry_name.pack()

button_random_coffee = tk.Button(root, text="Random Coffee", command=lambda: button_click(1))
button_manual_coffee = tk.Button(root, text="Manual Coffee", command=lambda: button_click(2))
button_rate_app = tk.Button(root, text="Rate Our App", command=lambda: button_click(3))

button_random_coffee.pack()
button_manual_coffee.pack()
button_rate_app.pack()

root.mainloop()
