import tkinter as tk

class LargeButton(tk.Frame):
    def __init__(self, owner, text, file, command):
        super().__init__(owner)
        self.command = command

        self.image = tk.PhotoImage(file=file)
        self.image_label = tk.Label(self, image=self.image)
        self.image_label.pack(side=tk.TOP, padx=5, pady=5)

        if text!="":
            self.text_label = tk.Label(self, text=text)
            self.text_label.pack(side=tk.BOTTOM, padx=5, pady=(0, 5)); 
            self.text_label.bind("<Button-1>", self.click_event)

        self.bind("<Button-1>", self.click_event)
        self.image_label.bind("<Button-1>", self.click_event)

    def click_event(self, event):
        self.command()