# GUI imports:
import customtkinter as ct
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.filedialog import askopenfilename

# Other tools:
import random
import pyodbc


# Window Main Options:
ct.set_appearance_mode("system")
ct.set_default_color_theme("blue")

try:
    # Main Window:
    
    # Select db
    db = file = filedialog.askopenfilename(title="Datenbank auswählen!")

    # db Connection:
    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + db +';')
    cs = conn.cursor()

    #Main Window Configuration
    window = ct.CTk()
    window.geometry("500x500+700+320")
    window.title("Vokabel Über")

    tabview = ct.CTkTabview(master=window,width=0, height=350)
    tabview.place(x=10, y=-50, relwidth=1.0, relheight=1.0, relx=-0.02, rely=0.1)

    new_vocab = tabview.add("Neue Vokabeln")
    train_vocab = tabview.add("Vokabeln üben")
    tabview.set("Neue Vokabeln")

    entry_new_ge = ct.CTkEntry(master=new_vocab, placeholder_text='Neue Deutsch Vokabel', width=150)
    entry_new_ge.place(x=10, y=-50, relx=0.1, rely=0.12)

    entry_new_en = ct.CTkEntry(master=new_vocab, placeholder_text='Neue Englisch Vokabel', width=150)
    entry_new_en.place(x=10, y=-50, relx=0.55, rely=0.12)

    word_list_germanL = ct.CTkLabel(master=new_vocab, text="Wörterliste Deutsch:").place(x=10, y=-50, relx=0.13, rely=0.2)
    word_list_foreignL = ct.CTkLabel(master=new_vocab, text="Wörterliste Fremdsprache:").place(x=10, y=-50, relx=0.55, rely=0.2)

    txt_German = ct.CTkTextbox(master=new_vocab, state="disabled")
    txt_German.place(x=10, y=-50, relx=0.05, rely=0.27)

    txt_Foreign = ct.CTkTextbox(master=new_vocab, state="disabled")
    txt_Foreign.place(x=10, y=-50, relx=0.50, rely=0.27)

    def new_vocab_fnk():
        entryvalue = (
            str(entry_new_ge.get()),
           str(entry_new_en.get())
        )

        entryvalueiter = iter(entryvalue)
                    
        strValue=cs.execute("SELECT * FROM Vocab WHERE DeutscheVocab = ?;", entryGerman.get())
    
    add_btn = ct.CTkButton(master=new_vocab, text="Vokabeln Hinzufügen",command=new_vocab_fnk)
    add_btn.place(x=10, y=-50, relx=0.34, rely=0.75)

    def resize(event):
    # When the window is resized, reposition the text widget so it remains below the button
        #text.place(x=10, y=50, relwidth=1.0, relheight=1.0, relx=0, rely=0.1)
        pass

    # Bind the resize event to the root window
    window.bind("<Configure>", resize)

    window.mainloop()
except pyodbc.Error as e:
    # Failed Error Window:
    error = ct.CTk()
    error.geometry("200x100+800+300")
    error.title("Error")

    errormessage = ct.CTkLabel(error, text="Failed to Connect", text_color="#f00")
    errormessage.pack(side="top")

    error.mainloop()