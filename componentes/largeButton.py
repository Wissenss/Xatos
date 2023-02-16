import tkinter as tk

class LargeButton(tk.Frame):
    def __init__(self, owner, text, file, command, hoverEffect = True):
        super().__init__(owner)
        self.command = command

        self.image = tk.PhotoImage(file=file)
        self.image_label = tk.Label(self, image=self.image)
        self.image_label.pack(side=tk.TOP, padx=5, pady=5)

        self.text_label = None
        if text!="":
            self.text_label = tk.Label(self, text=text)
            self.text_label.pack(side=tk.BOTTOM, padx=5, pady=(0, 5)); 
            self.text_label.bind("<Button-1>", self.click_event)

        self.bind("<Button-1>", self.click_event)
        self.image_label.bind("<Button-1>", self.click_event)

        if hoverEffect:
            self.bind("<Enter>", self.enter_event)
            self.bind("<Leave>", self.leave_event)

    def click_event(self, event):
        self.command()

    def enter_event(self, event):
        onHoverColor = "#dedede"
        self.config(background=onHoverColor)
        self.image_label.config(bg=onHoverColor)

        if self.text_label != None:
            self.text_label.config(bg=onHoverColor)

    def leave_event(self, event):
        self.config(background="SystemButtonFace")
        self.image_label.config(bg="SystemButtonFace")

        if self.text_label != None:
            self.text_label.config(bg="SystemButtonFace")