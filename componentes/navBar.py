import tkinter as tk
from tkinter import ttk
try:
    from largeButton import LargeButton
except:
    from componentes.largeButton import LargeButton

#NavBar dictionary structure
#
#Dict = {
# "Section  _1" : [
#   ("button text", "button image addres", function obj),
#   ("button text", "button image addres", function obj)
#   ]
# "Section_2" : [
#   ("button text", "button image addres", function obj),
#   ("button text", "button image addres", function obj)
#   ]
# .
# .
# .
# }
class NavBar(tk.Frame):
    def __init__(self, owner, content:dict={}, section_titles=True):
        super().__init__(owner) # relief="solid", bd=2
        self.content = content
        self.section_titles = section_titles

    def add_section(self, section_name):
        self.content[section_name] = []

    def add(self, button_tuple, section):
        self.content[section].append(button_tuple)

#   This method handles the layout of all components in the 
#   self.content dictionary
#   [][][]|[][][]|[][][]
#    name   name   name
    def render(self):
        pos = 0
        for i, section in enumerate(self.content):
            for j, button_tuple in enumerate(self.content[section]):
                LargeButton(self, button_tuple[0], button_tuple[1], button_tuple[2]).grid(row=0, column=pos, sticky="nswe")
                pos+=1
            if i != len(self.content)-1: 
                print("debug")
                SectionDiv = ttk.Separator(self, orient=tk.VERTICAL)
                SectionDiv.grid(row=0, column=pos, sticky="nswe", rowspan=2, pady=5, padx=5)
                pos+=1 
            if self.section_titles:
                tk.Label(self, text=section).grid(row=1, column=pos, columnspan=len(self.content[section]), sticky="nsew")

        # ttk.Separator(self, orient=tk.HORIZONTAL).grid(row=3, column=0, columnspan=pos, sticky="nwe")

