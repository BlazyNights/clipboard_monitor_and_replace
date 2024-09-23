import threading
import time
import tkinter as tk
from tkinter import ttk

import pyperclip

import vxtwitter_converter


class Application(tk.Tk, threading.Thread):
    def __init__(self):
        super().__init__()
        threading.Thread.__init__(self)
        self.start()
        self.title("Text Manipulation Tool")
        self.geometry("1000x400")
        self.config = vxtwitter_converter.read_config()

        # Checkbox at the top
        self.replacing_active_var = tk.BooleanVar()
        self.chk_replacing_active = tk.Checkbutton(self, text="Replacing active", var=self.replacing_active_var)
        self.chk_replacing_active.pack(anchor="nw")

        self.running = False

        self.btn_manual_replace = tk.Button(
            self, text="Manual replace", command=lambda: vxtwitter_converter.clipboard_scan_and_replace(self.config))
        self.btn_manual_replace.pack(anchor="nw")

        # Split the window into two frames
        self.frame_left = tk.Frame(self)
        self.frame_right = tk.Frame(self)

        self.frame_left.pack(side="left", expand=True, fill="both")
        self.frame_right.pack(side="right", expand=True, fill="both")

        # Lists to keep track of all rows in each half
        self.left_rows = []
        self.right_rows = []

        # Initial rows
        # self.add_row("left")
        # self.add_row("right")

        # Add and Remove buttons for the left half
        self.btn_add_left = tk.Button(self.frame_left, text="Add Row", command=lambda: self.add_row("left"))
        self.btn_add_left.pack(side="bottom", fill="x")

        # Add and Remove buttons for the right half
        self.btn_add_right = tk.Button(self.frame_right, text="Add Row", command=lambda: self.add_row("right"))
        self.btn_add_right.pack(side="bottom", fill="x")
        self.timer = RepeatTimer(interval=0.5,
                                 function=vxtwitter_converter.clipboard_scan_and_replace,
                                 args=(self.config,))

    def add_row(self, side, first_text=None, second_text=None):
        frame = self.frame_left if side == "left" else self.frame_right
        rows = self.left_rows if side == "left" else self.right_rows

        row_frame = tk.Frame(frame)
        row_frame.pack(fill="x", padx=5, pady=5)

        label1_text = "Text to look for" if side == "left" else "Trigger string"
        label2_text = "Text to replace" if side == "left" else "Characters to strip after"

        tk.Label(row_frame, text=label1_text).pack(side="left")
        entry_1 = tk.Entry(row_frame)
        if first_text is not None:
            entry_1.insert(0, first_text)
        entry_1.pack(side="left")

        tk.Label(row_frame, text=label2_text).pack(side="left")

        entry_2 = tk.Entry(row_frame)
        if second_text is not None:
            entry_2.insert(0, second_text)
        entry_2.pack(side="left")

        btn_remove = tk.Button(row_frame, text="Remove", command=lambda: self.remove_row(side, row_frame))
        btn_remove.pack(side="right")

        rows.append(row_frame)

        self.update_remove_buttons(side)

    def remove_row(self, side, row_frame):
        rows = self.left_rows if side == "left" else self.right_rows
        if len(rows) > 1:
            row_frame.destroy()
            rows.remove(row_frame)
            self.update_remove_buttons(side)

    def update_remove_buttons(self, side):
        rows = self.left_rows if side == "left" else self.right_rows
        for row in rows:
            button = row.winfo_children()[-1]  # The remove button is the last widget in the row
            button.config(state="normal" if len(rows) > 1 else "disabled")

    def clipboard_loop(self):
        if not self.running and self.replacing_active_var.get():
            self.running = True
            self.timer.start()
        elif self.running and not self.replacing_active_var.get():
            self.running = False
            self.timer.cancel()

    def clipboard_loop2(self):
        if self.replacing_active_var.get():
            vxtwitter_converter.clipboard_scan_and_replace(self.config)

    def run(self):
        self.root = tk.Tk()
        # self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.mainloop()


class RepeatTimer(threading.Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


if __name__ == "__main__":
    app = Application()

    # Read config and set lines from it
    # config = vxtwitter_converter.read_config()
    for find_replace_rule in app.config['line_replace']:
        app.add_row('left',
                    first_text=find_replace_rule['find'],
                    second_text=find_replace_rule['replace'])

    for strip_partial_line_rule in app.config['line_partial_strip']:
        for url in strip_partial_line_rule['urls']:
            app.add_row('right',
                        first_text=url,
                        second_text=strip_partial_line_rule['characters_to_strip_after'])

    # running = False
    # while True:
    #     # app.update_idletasks()
    #     # app.update()
    #     if not running and app.replacing_active_var.get():
    #         running = True
    #         timer.start()
    #     elif running and not app.replacing_active_var.get():
    #         running = False
    #         timer.cancel()
    # app.after(0, app.clipboard_loop)
    app.run()
    app.clipboard_loop()

