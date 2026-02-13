from tkinter import *
from tkinter import messagebox
from random import randint, shuffle, choice
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR --------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_numbers + password_symbols + password_letters
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD --------------------------------- #

def save():
    input_website = website_entry.get()
    input_email = email_username_entry.get()
    input_password = password_entry.get()
    new_data = {
        input_website: {
            "email": input_email,
            "password": input_password
        }
    }

    if len(input_website) == 0 or len(input_password) == 0:
        messagebox.showinfo(title="OOPS", message="Please don't leave any fields empty")
    else:
        is_ok = messagebox.askokcancel(title=input_website,
                                       message=f"These are the details entered: \nEmail: {input_email} "
                                               f"\nPassword: {input_password} \nIs it okay to save")
        if is_ok:
            try:
                with open("data.json", mode="r") as file:
                    # Reading old data
                    data = json.load(file)
            except FileNotFoundError:
                with open("data.json", mode="w") as file:
                    json.dump(new_data, file, indent=4)
            else:
                # Updating old data with new data
                data.update(new_data)

                with open("data.json", mode="w") as file:
                    # Saving uptade data
                    json.dump(data, file, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)


# ---------------------------- Find Password -------------------------- #
def find_password():
    website = website_entry.get()
    try:
        with open("data.json", mode="r") as file_data:
            data_json = json.load(file_data)

    except FileNotFoundError:
        messagebox.showinfo(message="No data file found")

    else:
        if website in data_json:
            getting_email = data_json[website]["email"]
            getting_password = data_json[website]["password"]
            messagebox.showinfo(message=f"Email: {getting_email}"
                                        f"\nPassword: {getting_password}")
        else:
            messagebox.showinfo(message=f"No detail for {website} exists")


            # ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Entries

website_entry = Entry(width=21)
website_entry.grid(column=1, row=1, sticky=EW)
website_entry.focus()

email_username_entry = Entry(width=21)
email_username_entry.grid(column=1, row=2, columnspan=2, sticky=EW)
email_username_entry.insert(END, "mirzaahmedov10@mail.ru")

password_entry = Entry(width=21)
password_entry.grid(column=1, row=3, sticky=EW)

# Labels

website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

email_username_label = Label(text="Email/Username:")
email_username_label.grid(column=0, row=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# Buttons

generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(column=2, row=3)

add_button = Button(text="Add", width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2)

search_button = Button(text="Search", width=13, command=find_password)
search_button.grid(column=2, row=1)

window.mainloop()
