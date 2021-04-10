import os
from tkinter import *
from tkinter import font
from tkinter.messagebox import *
from tkinter.filedialog import *
import tkinter as tk
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os.path
import pathlib
    
class txtDoc:

    __root = tk.Tk()

    #button.pack() # Displaying the button

    # default window width and height
    __thisWidth = 6000
    __thisHeight = 6000
    __thisTextArea = tk.Text(__root)
    __thisMenuBar = Menu(__root)
    __thisFileMenu = Menu(__thisMenuBar, tearoff=0)
    __thisEditMenu = Menu(__thisMenuBar, tearoff=0)
    __thisFontMenu = Menu(__thisMenuBar, tearoff=0)
    __thisFontFamilyMenu = Menu(__thisFontMenu, tearoff=0)
    __thisFontWeightMenu = Menu(__thisFontMenu, tearoff=0)
    __thisFontSizeMenu = Menu(__thisFontMenu, tearoff=0)
    __thisThemesMenu = Menu(__thisFontMenu, tearoff=0)
    __thisShareMenu = Menu(__thisMenuBar, tearoff=0)
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
        self.__root.title("TxtPad - COMP216 Project, Group 2")

        # Center the window
        screenWidth = self.__root.winfo_screenwidth()
        screenHeight = self.__root.winfo_screenheight()

        # defining the font-size and type 
        self.customFont = font.Font(family="Helvetica", size=12)

        # assigning the defined fonts to the textArea
        self.__thisTextArea = tk.Text(self.__root, font=self.customFont, undo=True)

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

        # self.__thisFileMenu.add_command(label="Theme", command=self.__changeTheme)

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

        # To give a feature of undo
        self.__thisEditMenu.add_command(label="Undo", command=self.__thisTextArea.edit_undo)

        # To give a feature of redo
        self.__thisEditMenu.add_command(label="Redo", command=self.__thisTextArea.edit_redo)        

        # To give a feature of cut
        self.__thisEditMenu.add_command(label="Cut", command=self.__delete)

        # to give a feature of copy
        self.__thisEditMenu.add_command(label="Copy", command=self.__copy)

        # To give a feature of paste
        self.__thisEditMenu.add_command(label="Paste", command=self.__paste)

        ''' # To give a feature of cut
        self.__thisEditMenu.add_command(label="Cut", command=self.__cut) '''

        self.__thisEditMenu.add_separator()

        # To give a feature of paste
        self.__thisEditMenu.add_command(label="Find", command=self.__find)

        # To give a feature of paste
        self.__thisEditMenu.add_command(label="Replace", command=self.__replace)

        # To give a feature of editing
        self.__thisMenuBar.add_cascade(label="Edit", menu=self.__thisEditMenu)

        # To give a feature of font operations
        self.__thisMenuBar.add_cascade(label="Font", menu=self.__thisFontMenu) 
        # To share a file via gmail
        self.__thisMenuBar.add_cascade(label="Share",command=self.__showShare)
        # To bold the fonts
        self.__thisFontMenu.add_cascade(label="Font Family", menu=self.__thisFontFamilyMenu)

        for i in ("Arial Black", "Verdana", "Times New Roman"):
            if (i == "Arial Black"):
                self.__thisFontFamilyMenu.add_command(label=i, command=self.__onArial)
            if (i == "Verdana"):
                self.__thisFontFamilyMenu.add_command(label=i, command=self.__onVerdana)
            if (i == "Times New Roman"):
                self.__thisFontFamilyMenu.add_command(label=i, command=self.__onTimes)

        # To italic the fonts
        self.__thisFontMenu.add_cascade(label="Font Weight", menu=self.__thisFontWeightMenu)

        for i in ("Bold", "Italic", "Underline"):
            if (i == "Bold"):
                self.__thisFontWeightMenu.add_command(label=i, command=self.__onBold)
            if (i == "Italic"):
                self.__thisFontWeightMenu.add_command(label=i, command=self.__onItalic)
            if (i == "Underline"):
                self.__thisFontWeightMenu.add_command(label=i, command=self.__onUnderline)

        # To increase the size of the fonts
        self.__thisFontMenu.add_cascade(label="Font Size", menu=self.__thisFontSizeMenu)

        for i in ("12", "14", "16", "18", "20"):
            if (i == "12"):
                self.__thisFontSizeMenu.add_command(label=i, command=self.__onTwelve)
            if (i == "14"):
                self.__thisFontSizeMenu.add_command(label=i, command=self.__onFourteen)
            if (i == "16"):
                self.__thisFontSizeMenu.add_command(label=i, command=self.__onSixteen)
            if (i == "18"):
                self.__thisFontSizeMenu.add_command(label=i, command=self.__onEighteen)
            if (i == "20"):
                self.__thisFontSizeMenu.add_command(label=i, command=self.__onTwenty)
        
        # To change the theme the background and the font color 
        
        self.__thisFontMenu.add_cascade(label="Themes", menu=self.__thisThemesMenu)

        for i in("Blue Color", "Yellow Color","Green Color"):
            if(i=="Blue Color"):
                self.__thisThemesMenu.add_command(label=i, command=self.__onChangeBlue)
            if(i=="Yellow Color"):
                self.__thisThemesMenu.add_command(label=i, command=self.__onChangeYellow)
            if(i=="Green Color"):
                self.__thisThemesMenu.add_command(label=i, command=self.__onChangeGreen)
            
        self.__thisFontMenu.add_separator()
        self.__thisFontMenu.add_command(label="Increase Font Size", command=self.__onBigger)

        # To decrease the size of the fonts
        self.__thisFontMenu.add_command(label="Decrease Font Size", command=self.__onSmaller)      

        # To create a feature of description of the TxtPad
        self.__thisAboutMenu.add_command(label="About TxtPad 1.0", command=self.__showAbout)
        self.__thisMenuBar.add_cascade(label="About", menu=self.__thisAboutMenu)

        self.__root.config(menu=self.__thisMenuBar)

        self.__thisScrollBar.pack(side=RIGHT, fill=Y)

        # Scrollbar will adjust automatically according to the content
        self.__thisScrollBar.config(command=self.__thisTextArea.yview)
        self.__thisTextArea.config(yscrollcommand=self.__thisScrollBar.set)

    def __quitApplication(self):
        self.__root.destroy()
        # exit()

    def __find(self):
        window = Tk()
        window.title("Find")
        windowWidth = window.winfo_reqwidth() + 300 
        windowHeight = window.winfo_reqheight()
        positionRight = int(window.winfo_screenwidth()/2 - windowWidth/2) 
        positionDown = int(window.winfo_screenheight()/2 - windowHeight/2)
        window.geometry("+{}+{}".format(positionRight, positionDown))
        window.geometry('250x100')
        lblFind = Label(window, text='Find')
        lblFind.grid(column = 0, row = 0, sticky = (W, E), padx = 20, pady = 10)
        txtFind = Entry(window)
        txtFind.grid(column = 1, row = 0, sticky = (W))
        def find(*args):
            self.__thisTextArea.tag_remove('Find', '1.0', END)
            findText = txtFind.get()
            if (findText):
                index = '1.0'
                while True:
                    index = self.__thisTextArea.search(findText, index, stopindex = END)
                    if not index :
                        break
                    last = '% s+% dc' % (index, len(findText))
                    self.__thisTextArea.tag_add('Find', index, last)
                    index = last
                self.__thisTextArea.tag_config('Find', foreground = 'green')
        btnFind = Button(window, text='Find', command = find)
        btnFind.grid(column = 1, row = 1, sticky = (W, E), padx = 5, pady = 10)
        window.mainloop()


    def __replace(self):
        window = Tk()
        window.title("Replace")
        windowWidth = window.winfo_reqwidth() + 300 
        windowHeight = window.winfo_reqheight()
        positionRight = int(window.winfo_screenwidth()/2 - windowWidth/2) 
        positionDown = int(window.winfo_screenheight()/2 - windowHeight/2)
        window.geometry("+{}+{}".format(positionRight, positionDown))
        window.geometry('300x150')
        lblFind = Label(window, text='Find')
        lblFind.grid(column = 0, row = 0, sticky = (W, E), padx = 10, pady = 10)
        txtFind = Entry(window)
        txtFind.grid(column = 1, row = 0, sticky = (W))
        lblReplace = Label(window, text='Replace with')
        lblReplace.grid(column = 0, row = 1, sticky = (W, E), padx = 10, pady = 10)
        txtReplace = Entry(window)
        txtReplace.grid(column = 1, row = 1, sticky = (W))
        def replace(*args):
            self.__thisTextArea.tag_remove('Replace', '1.0', END)
            findText = txtFind.get()
            replaceText = txtReplace.get()
            if (findText and replaceText):
                index = '1.0'
                while True:
                    index = self.__thisTextArea.search(findText, index, stopindex = END)
                    if not index :
                        break
                    l = '% s+% dc' % (index, len(findText))
                    self.__thisTextArea.delete(index, l)
                    self.__thisTextArea.insert(index, replaceText)
                    last = '% s+% dc' % (index, len(replaceText))
                    self.__thisTextArea.tag_add('Replace', index, last)
                    index = last
                self.__thisTextArea.tag_config('Replace', foreground = 'blue')
        btnReplace = Button(window, text='Replace', command = replace)
        btnReplace.grid(column = 1, row = 2, sticky = (W, E), padx = 5, pady = 10)
        window.mainloop()

    def __changeTheme(self):
        self.__thisTextArea.configure(bg='blue')

    def __onArial(self):
        arial_font = font.Font(self.__thisTextArea, self.__thisTextArea.cget("font"))
        arial_font.configure(family="Arial Black")

        self.__thisTextArea.tag_configure("arial", font=arial_font)

        current_tags = self.__thisTextArea.tag_names("sel.first")

        if "arial" in current_tags:
            self.__thisTextArea.tag_remove("arial", "sel.first", "sel.last")
        else:
            self.__thisTextArea.tag_add("arial", "sel.first", "sel.last")

    def __onVerdana(self):
        verdana_font = font.Font(self.__thisTextArea, self.__thisTextArea.cget("font"))
        verdana_font.configure(family="Verdana")

        self.__thisTextArea.tag_configure("verdana", font=verdana_font)

        current_tags = self.__thisTextArea.tag_names("sel.first")

        if "verdana" in current_tags:
            self.__thisTextArea.tag_remove("verdana", "sel.first", "sel.last")
        else:
            self.__thisTextArea.tag_add("verdana", "sel.first", "sel.last")

    def __onTimes(self):
        times_font = font.Font(self.__thisTextArea, self.__thisTextArea.cget("font"))
        times_font.configure(family="Times New Roman")

        self.__thisTextArea.tag_configure("times", font=times_font)

        current_tags = self.__thisTextArea.tag_names("sel.first")

        if "times" in current_tags:
            self.__thisTextArea.tag_remove("times", "sel.first", "sel.last")
        else:
            self.__thisTextArea.tag_add("times", "sel.first", "sel.last")

    def __onBold(self):
        # make the fonts bold
        bold_font = font.Font(self.__thisTextArea, self.__thisTextArea.cget("font"))
        bold_font.configure(weight="bold")

        self.__thisTextArea.tag_configure("bold", font=bold_font)

        current_tags = self.__thisTextArea.tag_names("sel.first")

        if "bold" in current_tags:
            self.__thisTextArea.tag_remove("bold", "sel.first", "sel.last")
        else:
            self.__thisTextArea.tag_add("bold", "sel.first", "sel.last")

    def __onItalic(self):
        italic_font = font.Font(self.__thisTextArea, self.__thisTextArea.cget("font"))
        italic_font.configure(slant="italic")

        self.__thisTextArea.tag_configure("italic", font=italic_font)

        current_tags = self.__thisTextArea.tag_names("sel.first")

        if "italic" in current_tags:
            self.__thisTextArea.tag_remove("italic", "sel.first", "sel.last")
        else:
            self.__thisTextArea.tag_add("italic", "sel.first", "sel.last")

    def __onUnderline(self):
        underline_font = font.Font(self.__thisTextArea, self.__thisTextArea.cget("font"))
        underline_font.configure(underline = True)

        self.__thisTextArea.tag_configure("underline", font=underline_font)

        current_tags = self.__thisTextArea.tag_names("sel.first")

        if "underline" in current_tags:
            self.__thisTextArea.tag_remove("underline", "sel.first", "sel.last")
        else:
            self.__thisTextArea.tag_add("underline", "sel.first", "sel.last")

    def __onTwelve(self):
        self.customFont.configure(size=12)

    def __onFourteen(self):
        self.customFont.configure(size=14)

    def __onSixteen(self):
        self.customFont.configure(size=16)

    def __onEighteen(self):
        self.customFont.configure(size=18)

    def __onTwenty(self):
        self.customFont.configure(size=20)
    
    def __onChangeBlue(self):
        self.__root.config(bg="lightgreen")
        self.__thisTextArea.config(bg="lightBlue",fg="black")

    def __onChangeGreen(self):
        self.__root.config(bg="lightgreen")
        self.__thisTextArea.config(bg="lightGreen",fg="black")

    def __onChangeYellow(self):
        self.__root.config(bg="lightgreen")
        self.__thisTextArea.config(bg="lightYellow",fg="black")

    def __onBigger(self):
        '''Make the font 2 points bigger'''
        size = self.customFont['size']
        self.customFont.configure(size=size+2)

    def __onSmaller(self):
        '''Make the font 2 points smaller'''
        size = self.customFont['size']
        self.customFont.configure(size=size-2)

    def __showAbout(self):
        showinfo(title="TxtPad 1.0", message="COMP216 Project, Group 2")
    def __showShare(self):
        root1 = Tk()

        windowWidth = root1.winfo_reqwidth() + 300 
        windowHeight = root1.winfo_reqheight()
        positionRight = int(root1.winfo_screenwidth()/2 - windowWidth/2) 
        positionDown = int(root1.winfo_screenheight()/2 - windowHeight/2)
        root1.geometry("+{}+{}".format(positionRight, positionDown))
        root1.geometry('400x200')
        #Providing title to the form
        root1.title('Sent email ')
        #this creates 'Label' widget for Email and uses place() method.
        lblEmail = Label(root1, text='Email')
        lblEmail.grid(column = 0, row = 0, sticky = (W, E), padx = 20, pady = 10, ipadx=20,ipady=10)
        txtEmail = Entry(root1)
        #txtEmail.place()
        txtEmail.grid(column = 1, row = 0, sticky = (W), ipadx = 20, ipady = 10)
       
        def SendMail(*args):
            sender_email = "network216comp@gmail.com"
            receiver_email = txtEmail.get()
            message = MIMEMultipart()
            message=MIMEMultipart()
            message["From"] = sender_email
            message['To'] = receiver_email
            message['Subject'] = "sending mail using python"
            
            name=os.path.basename(self.__file)
            path=os.path.dirname(self.__file)

            file = path+"\\"+name
            attachment = open(file,'rb')

            obj = MIMEBase('application','octet-stream')

            obj.set_payload((attachment).read())
            encoders.encode_base64(obj)
            obj.add_header('Content-Disposition',"attachment; filename= "+file)

            message.attach(obj)
           
            my_message = message.as_string()
            email_session = smtplib.SMTP('smtp.gmail.com',587)
            email_session.starttls()
            email_session.login(sender_email,"Comp216005")
            
            email_session.sendmail(sender_email,receiver_email,my_message)
            email_session.quit()
            print("YOUR MAIL HAS BEEN SENT SUCCESSFULLY")


        btnEmail = Button(root1, text='Send', command = SendMail)
        btnEmail.grid(column = 1, row = 1, sticky = (W, E), padx = 5, pady = 10)

        root1.mainloop()
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
        self.__root.title("Untitled - TxtPad")
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
                self.__root.title(os.path.basename(self.__file) + " - TxtPad")

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
                self.__root.title(os.path.basename(self.__file) + " - TxtPad")

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

    ''' def __cut(self):
        if self.__thisTextArea.selection_get():
            selected = self.__thisTextArea.selection_get()
            self.__thisTextArea.delete("sel.first", "sel.last") '''      

    def run(self):

        # Run main application
        self.__root.mainloop()
        
# Run main application
txtDoc = txtDoc(width=800, height=450)
txtDoc.run()