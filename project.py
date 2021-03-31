import tkinter
import os
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import random
try:

    import tkinter.ttk as ttk
    import tkinter.font as font
except ImportError: # Python 2
    import Tkinter as Tk
    import ttk
    import tkFont as font


class txtDoc:

    __root = Tk()

    # default window width and height
    __thisWidth = 6000
    __thisHeight = 6000
    __thisTextArea = Text(__root)
    __thisMenuBar = Menu(__root)
    __thisFileMenu = Menu(__thisMenuBar, tearoff=0)
    __thisEditMenu = Menu(__thisMenuBar, tearoff=0)
    __thisFontMenu = Menu(__thisMenuBar, tearoff=0)
    __thisAboutMenu = Menu(__thisMenuBar, tearoff=0)

    # To add scrollbar
    __thisScrollBar = Scrollbar(__thisTextArea)
    __file = None

    def __init__(self, **kwargs):

        # Set icon
        try:
            self.__root.wm_iconbitmap("txtDoc.ico")
        except:
            pass

        # Set window size (the default is 300x300)

        try:
            self.__thisWidth = kwargs["width"]
        except KeyError:
            pass

        try:
            self.__thisHeight = kwargs["height"]
        except KeyError:
            pass

        # Set the window text
        self.__root.title("COMP 216 Project - Group 2 - txtDoc")

        # Center the window
        screenWidth = self.__root.winfo_screenwidth()
        screenHeight = self.__root.winfo_screenheight()
        MyFont = font.Font(family='Helvetica', size=20, weight='bold')

        # For left-alling
        left = (screenWidth / 2) - (self.__thisWidth / 2)

        # For right-allign
        top = (screenHeight / 2) - (self.__thisHeight / 2)

        # For top and bottom
        self.__root.geometry(
            "%dx%d+%d+%d" % (self.__thisWidth, self.__thisHeight, left, top)
        )

        # To make the textarea auto resizable
        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)

        # Add controls (widget)
        self.__thisTextArea.grid(sticky=N + E + S + W)

        # To open new file
        self.__thisFileMenu.add_command(label="New", command=self.__newFile)

        # To open a already existing file
        self.__thisFileMenu.add_command(label="Open", command=self.__openFile)

        # To save current file
        self.__thisFileMenu.add_command(label="Save", command=self.__saveFile)

        # To saveAs current file
        self.__thisFileMenu.add_command(label="SaveAs", command=self.__saveAsFile)

        # To create a line in the dialog
        self.__thisFileMenu.add_separator()
        self.__thisFileMenu.add_command(label="Exit", command=self.__quitApplication)
        self.__thisMenuBar.add_cascade(label="File", menu=self.__thisFileMenu)

        #------------------------------------------------------        

        # To give a feature of cut
        self.__thisEditMenu.add_command(label="Delete", command=self.__delete)

        # to give a feature of copy
        self.__thisEditMenu.add_command(label="Copy", command=self.__copy)

        # To give a feature of paste
        self.__thisEditMenu.add_command(label="Paste", command=self.__paste)

        # To give a feature of undo
        self.__thisEditMenu.add_command(label="Undo", command=self.__undo)

        # To give a feature of editing
        self.__thisMenuBar.add_cascade(label="Edit", menu=self.__thisEditMenu)

        self.__thisMenuBar.add_cascade(label="Font", menu=self.__thisFontMenu)       

        # To create a feature of description of the txtDoc
        self.__thisAboutMenu.add_command(label="About txtDoc", command=self.__showAbout)
        self.__thisMenuBar.add_cascade(label="About", menu=self.__thisAboutMenu)

        self.__root.config(menu=self.__thisMenuBar)

        self.__thisScrollBar.pack(side=RIGHT, fill=Y)

        # Scrollbar will adjust automatically according to the content
        self.__thisScrollBar.config(command=self.__thisTextArea.yview)
        self.__thisTextArea.config(yscrollcommand=self.__thisScrollBar.set)

    def __quitApplication(self):
        self.__root.destroy()
        # exit()

    def __showAbout(self):
        showinfo("Group Project 216 Group 2 ")

    def __openFile(self):

        self.__file = askopenfilename(
            defaultextension=".txt",
            filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")],
        )

        if self.__file == "":

            # no file to open
            self.__file = None
        else:

            # Try to open the file
            # set the window title
            self.__root.title(os.path.basename(self.__file) + " - txtDoc")
            self.__thisTextArea.delete(1.0, END)

            file = open(self.__file, "r")

            self.__thisTextArea.insert(1.0, file.read())

            file.close()

    def __newFile(self):
        self.__root.title("Untitled - txtDoc")
        self.__file = None
        self.__thisTextArea.delete(1.0, END)

    def __saveFile(self):

        if self.__file == None:
            # Save as new file
            self.__file = asksaveasfilename(
                initialfile="Untitled.txt",
                defaultextension=".txt",
                filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")],
            )

            if self.__file == "":
                self.__file = None
            else:

                # Try to save the file
                file = open(self.__file, "w")
                file.write(self.__thisTextArea.get(1.0, END))
                file.close()

                # Change the window title
                self.__root.title(os.path.basename(self.__file) + " - txtDoc")

        else:
            file = open(self.__file, "w")
            file.write(self.__thisTextArea.get(1.0, END))

                # SaveAs

    def __saveAsFile(self):

        if self.__file == None:
            # Save as new file
            self.__file = asksaveasfilename(
                initialfile="TestText.txt",
                defaultextension=".txt",
                filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")],
            )

            if self.__file == "":
                self.__file = None
            else:

                # Try to save the file
                file = open(self.__file, "w")
                file.write(self.__thisTextArea.get(1.0, END))
                file.close()

                # Change the window title
                self.__root.title(os.path.basename(self.__file) + " - txtDoc")

        else:
            file = open(self.__file, "w")
            file.write(self.__thisTextArea.get(1.0, END))
            file.close()


    def __paste(self):
        self.__thisTextArea.event_generate("<<Paste>>")
    def __copy(self):
        self.__thisTextArea.event_generate("<<Copy>>")
    def __delete(self):
        self.__thisTextArea.event_generate("<<Clear>>")
    def __undo(self):
        self.__thisTextArea.event_generate("<<Undo>>")
        root.mainloop()
    def run(self):

        # Run main application
        self.__root.mainloop()


# Run main application
txtDoc = txtDoc(width=1000, height=800)
txtDoc.run()
