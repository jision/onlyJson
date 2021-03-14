"""
Name    : only_json.py
Author  : jision
Connect : jisionpc@gmail.com
Time    : 11-03-2021 4:00 PM
Desc    :
"""

import tkinter as tk
from tkinter import Tk
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter import PhotoImage
import tkinter.ttk as ttk
import tkinter.font as tkFont
import json
import datetime


# from PIL import ImageTk, Image
class Application(ttk.Frame):
    # default window width and height
    __thisWidth = 900
    __thisHeight = 700
    __resourcePath = ""
    __thisTextArea = ""
    __thisJsonBody = {}
    __cursor_info_bar = ""
    __lineNumberbar = ""
    __search_string = ""
    __search_string_area = ""
    file_name = False
    __json_info_bar = ""

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.get_resourcepath()  # setting up resource path
        self.setWindowParams()  # setting windows path

    def get_resourcepath(self):
        # convert to proper array based
        self.__resourcePath = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + "/resources/"
        print(self.__resourcePath)

    def setWindowParams(self):

        self.__lineNumberbar = Text(self.master, takefocus=0, fg='white', border=0,
                                    background='#282828',
                                    state='disabled',
                                    wrap='none',
                                    width=5)
        self.__thisTextArea = Text(self.master, undo=True)
        # Add the binding
        self.__thisTextArea.bind("<Control-Key-a>", self.__select_all)
        self.__thisTextArea.bind("<Control-Key-A>", self.__select_all)
        self.__thisTextArea.bind('<Any-KeyPress>', self.__on_content_changed)
        self.__thisTextArea.bind('<Control-F>', self.__find_text_focus)
        self.__thisTextArea.bind('<Control-f>', self.__find_text_focus)
        self.__thisTextArea.bind('<Control-S>', self.__save)
        self.__thisTextArea.bind('<Control-s>', self.__save)

        # menu options
        __thisMenuBar = Menu(self.master)
        __thisFileMenu = Menu(__thisMenuBar, tearoff=0)
        __thisHelpMenu = Menu(__thisMenuBar, tearoff=0)

        # file menu dropdown
        # To open new file
        __thisFileMenu.add_command(label="New", accelerator='Ctrl+N', command=self.__newFile)
        # To open a already existing file
        __thisFileMenu.add_command(label="Open", accelerator='Ctrl+O', command=self.__openFile)
        __thisFileMenu.add_command(label="Save", accelerator='Ctrl+S', command=self.__save)
        __thisFileMenu.add_command(label="Quit")

        # about menu
        __thisHelpMenu.add_command(label="About", command=self.__about)

        # menu bar setting
        __thisMenuBar.add_cascade(label="File", menu=__thisFileMenu)
        __thisMenuBar.add_cascade(label="Help", menu=__thisHelpMenu)
        self.master.config(menu=__thisMenuBar)  # sets the window to use this menubar

        # To add scrollbar
        __thisScrollBar = Scrollbar(self.__thisTextArea)

        # Center the window
        screenWidth = self.master.winfo_screenwidth()
        screenHeight = self.master.winfo_screenheight()

        # For left-align
        left = (screenWidth / 2) - (self.__thisWidth / 2)

        # For right-align
        top = (screenHeight / 2) - (self.__thisHeight / 2)

        # For top and bottom
        self.master.geometry('%dx%d+%d+%d' % (self.__thisWidth,
                                              self.__thisHeight,
                                              left, top))

        # To make the textarea auto resizable
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)

        self.master.tk.call('wm', 'iconphoto', self.master._w, tk.PhotoImage(file=self.__resourcePath + "titlebar.png"))
        # need to check zoom not allowed
        # self.master.state("zoomed")

        # title bar icon
        self.master.title("OnlyJSON")

        self.__lineNumberbar.grid(row=0, column=0,
                                  sticky="nsew")
        self.__lineNumberbar.tag_configure('line', justify='right')

        # Add controls (widget)
        self.__thisTextArea.grid(row=0, column=1, sticky=N + E + S + W)
        # adding cursor info label
        self.__cursor_info_bar = Label(self.__thisTextArea, text='Line: 1 | Column: 1')
        self.__cursor_info_bar.pack(expand='no', fill=None, side='right', anchor='se')

        # adding json info bar
        self.__json_info_bar = Label(self.__thisTextArea, text='')
        self.__json_info_bar.pack(fill=X, expand=True, side='right', anchor='ne', ipadx=1.0, ipady=0.0)

        # the label for search
        self.__search_string = Label(self.__thisTextArea, text="find").pack(fill=None, side='left', anchor='sw',
                                                                            ipadx=0.5,
                                                                            ipady=0.5)
        self.__search_string_area = Entry(self.__thisTextArea, width=30)  # this returns object onlines not always good
        self.__search_string_area.pack(fill=X, side='left', expand=True, anchor='sw', padx=6, pady=0)
        self.__search_string_area.bind('<Return>', self.__search_input)

    # menu functionality

    def __newFile(self):
        self.__file = {}
        self.__thisTextArea.delete(1.0, END)
        x = datetime.datetime.now()
        print(x.strftime("%c"))
        self.file_name = x.strftime("%c") + '.json'
        self.__json_info_bar.config(bg='grey', text="", fg='white')

    def __openFile(self):
        # need to set default home path
        self.__file = askopenfilename(
            defaultextension=".json",
            title="select a valid JSON file",
            filetypes=[("JSON files", "*.json"),
                       ("Text Documents", "*.txt")]
        )

        if self.__file == "":

            # no file to open
            self.__file = {}
        else:

            self.__thisTextArea.delete(1.0, END)

            file = open(self.__file, "r")

            print("adasdas")
            self.__thisTextArea.insert(1.0, file.read())
            file.close()
            self.__on_content_changed()

    def __save(self, event=None):

        if not self.file_name:
            self.__save_as()
        else:
            self.__write_to_file(self.file_name)
        return "break"

    def __save_as(self, event=None):
        input_file_name = asksaveasfilename(defaultextension=".json",
                                            filetypes=[("JSON files", "*.json"),
                                                       ("Text Documents", "*.txt")])
        if input_file_name:
            self.file_name = input_file_name
            self.__write_to_file(self.file_name)
            # root.title('{} - {}'.format(os.path.basename(file_name), 'OnlyJson'))
        return "break"

    def __write_to_file(self, file_name):
        try:
            content = self.__thisTextArea.get(1.0, 'end-1c')
            with open(file_name, 'w') as the_file:
                the_file.write(content)
        except IOError:
            pass

    def __about(self, event=None):
        showinfo("onlyJson", "Python app to visualize , edit & validate JSON data ~ jision")

    ##### Menufunctionality ends #########################

    # Select all the text in textbox
    def __select_all(self, event):
        self.__thisTextArea.tag_add(SEL, "1.0", END)
        self.__thisTextArea.mark_set(INSERT, "1.0")
        self.__thisTextArea.see(INSERT)
        return 'break'

    def __on_content_changed(self, event=None):
        self.__update_line_numbers()
        self.__update_cursor()
        self.__json_beautify()

    def __update_cursor(self, event=None):
        print(self.__thisTextArea.index)
        row, col = self.__thisTextArea.index(INSERT).split('.')
        line_num, col_num = str(int(row)), str(int(col) + 1)  # col starts at 0
        infotext = "Line: {0} | Column: {1}".format(line_num, col_num)
        self.__cursor_info_bar.config(text=infotext)

    def __get_line_numbers(self):
        output = ''
        row, col = self.__thisTextArea.index("end").split('.')
        for i in range(1, int(row)):
            output += str(i) + '\n'
        return output

    def __update_line_numbers(self, event=None):
        line_numbers = self.__get_line_numbers()
        self.__lineNumberbar.config(state='normal')
        self.__lineNumberbar.delete('1.0', 'end')
        self.__lineNumberbar.insert('1.0', line_numbers)
        self.__lineNumberbar.config(state='disabled')

    def __find_text_focus(self, event=None):

        self.__search_string_area.focus_set()

    def __search_input(self, event=None):
        print(self.__search_string_area.get() + " entered from search!!")
        # change this to tree level search
        self.__search_output(self.__search_string_area.get(), True)
        return 'break'

    def __search_output(self, needle, if_ignore_case):
        self.__thisTextArea.tag_remove('match', '1.0', END)
        matches_found = 0
        if needle:
            start_pos = '1.0'
            while True:
                start_pos = self.__thisTextArea.search(needle, start_pos, nocase=if_ignore_case, stopindex=END)
                if not start_pos:
                    break

                end_pos = '{} + {}c'.format(start_pos, len(needle))
                self.__thisTextArea.tag_add('match', start_pos, end_pos)
                matches_found += 1
                start_pos = end_pos
            self.__thisTextArea.tag_config('match', background='yellow', foreground='blue')

    def __json_beautify(self):

        jsonb = self.__thisTextArea.get(1.0, 'end-1c')

        print(jsonb)

        try:
            jsonb = json.loads(jsonb)
            self.__thisJsonBody = json.dumps(jsonb, indent=4, allow_nan=True)
            print("Is valid json? true")
            self.__json_info_bar.config(bg='green', text="Valid Json!!", fg='white')
            # dump to string

        except ValueError as e:
            print("Is valid json? false")
            print(e)
            # let the body be as it is
            self.__thisJsonBody = jsonb
            self.__json_info_bar.config(bg='red', text=e, fg='white')

        self.__thisTextArea.delete(1.0, END)
        # print(type(jsonb))
        # print(json.dumps(self.__thisJsonBody, indent=4, allow_nan=True))
        self.__thisTextArea.insert(1.0, self.__thisJsonBody)
        # adding cursor info label
