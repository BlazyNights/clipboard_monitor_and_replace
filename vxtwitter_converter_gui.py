import tkinter as tk
import vxtwitter_converter


def toggle_replace():
    if replace_active.get():
        for row in rows:
            for widget in row:
                widget.config(state=tk.NORMAL)
    else:
        for row in rows:
            for widget in row:
                widget.config(state=tk.DISABLED)


root = tk.Tk()
root.title("Text Replacement Tool")

replace_active = tk.BooleanVar()
replace_checkbox = tk.Checkbutton(root, text="Replacing active", variable=replace_active, command=toggle_replace)
replace_checkbox.grid(row=0, column=0, columnspan=2, pady=10)

rows = []


# Function to create a row with two entry widgets
def create_row(row_number):
    text_to_look_for_label = tk.Label(root, text="Text to look for:")
    text_to_look_for_entry = tk.Entry(root)

    text_to_replace_label = tk.Label(root, text="Text to replace:")
    text_to_replace_entry = tk.Entry(root)

    text_to_look_for_label.grid(row=row_number, column=0, padx=10, pady=5, sticky=tk.E)
    text_to_look_for_entry.grid(row=row_number, column=1, padx=10, pady=5, sticky=tk.W)

    text_to_replace_label.grid(row=row_number, column=2, padx=10, pady=5, sticky=tk.E)
    text_to_replace_entry.grid(row=row_number, column=3, padx=10, pady=5, sticky=tk.W)

    # Disable the entry widgets initially
    text_to_look_for_entry.config(state=tk.DISABLED)
    text_to_replace_entry.config(state=tk.DISABLED)

    return [text_to_look_for_label, text_to_look_for_entry, text_to_replace_label, text_to_replace_entry]


# Create three rows initially
for i in range(1, 4):
    rows.append(create_row(i))

# Button to perform the replacement (add your functionality here)
replace_button = tk.Button(root, text="Replace Text", command=lambda: print("Replace button clicked"))
replace_button.grid(row=4, column=0, columnspan=4, pady=10)

root.mainloop()
