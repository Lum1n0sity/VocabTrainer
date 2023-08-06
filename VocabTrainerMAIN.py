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

# Connect to db:
try:
    # Success Main Window:
    
    # Select db
    db = file = filedialog.askopenfilename(title="Datenbank auswählen!")

    # db Connection:
    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + db +';')
    cs = conn.cursor()
    
    # Mainwindow Configurations:
    mainwindow = ct.CTk()
    mainwindow.geometry("500x500+700+320")
    mainwindow.title("Vokabel Über")
    
    # word list:
    word_list_germanL = ct.CTkLabel(mainwindow, text="Wörterliste Deutsch:").grid(row=0, column=1)
    word_list_foreignL = ct.CTkLabel(mainwindow, text="Wörterliste Fremdsprache:").grid(row=2, column=1)

    txt_German = ct.CTkTextbox(mainwindow, state="disabled")
    txt_German.grid(row=1, column=1)
    txt_German.configure(state="disabled")

    txt_Foreign = ct.CTkTextbox(mainwindow, state="disabled")
    txt_Foreign.grid(row=3, column=1)

    # Word list auto laod:
    word_list_germanLoad = cs.execute('SELECT DeutscheVocab FROM Vocab WHERE Id < 99999999;')
    word_list_germanFETCH = cs.fetchone()
    word_list_germanCON = "{}".format(word_list_germanFETCH)

    txt_German.configure(state='normal')
    txt_German.insert('end', ', ' + word_list_germanCON)
    txt_German.configure(state='disabled')
    
    # Entry:
    entryGerman = ct.CTkEntry(mainwindow, placeholder_text="Deutsch")
    entryGerman.grid(row=1, padx=10)

    entryForgein = ct.CTkEntry(mainwindow, placeholder_text="Fremdsprache")
    entryForgein.grid(row=3, padx=10)

    # placeholders:
    placeholder1 = ct.CTkLabel(mainwindow, text="  ").grid(row=0)
    placeholder2 = ct.CTkLabel(mainwindow, text="  ").grid(row=2)



    def Save_Entry():
        # Entry Word List:
        
        # German:
        txt_German.configure(state="normal")
        txt_German.insert("end", ",     " + entryGerman.get())
        txt_German.configure(state="disabled")
        
        # Foreign:
        txt_Foreign.configure(state="normal")
        txt_Foreign.insert("end", ",    " + entryForgein.get())
        txt_Foreign.configure(state="disabled")

        # Entry db:
        entryvalue = (
            str(entryGerman.get()),
           str(entryForgein.get())
        )

        entryvalueiter = iter(entryvalue)
                    
        strValue=cs.execute("SELECT * FROM Vocab WHERE DeutscheVocab = ?;", entryGerman.get())
        
        rowsFetch = cs.fetchall()
        print(rowsFetch) 
        #print(rowsFetch.count())
        
        if len(rowsFetch) > 0:
            print("Bereits Vorhanden")
        else:
            cs.execute("INSERT INTO Vocab (DeutscheVocab, FremdspracheVocab) VALUES (?,?);", entryvalue)
            print("Gespeichert")
        # More quite important sql Code: FROM Vocab WHERE NOT EXISTS (SELECT 1 FROM Vocab WHERE DeutscheVocab = ?)

        conn.commit()
    
    # Save Vocab Button:
    savevocab = ct.CTkButton(mainwindow, text="Speichern",fg_color="transparent" , command=Save_Entry)
    savevocab.grid(row=4, pady=5)

    def start_training():
       # Vocab Random:
        cs.execute('SELECT * FROM Vocab ORDER BY Rnd();')
        random_vocab_german = cs.fetchone()
        
        # Vocab viewer:
        trainer = ct.CTk()
        trainer.geometry("300x200+800+400")

        ct.CTkLabel(trainer, text=random_vocab_german).pack()

        trainer.mainloop()

    start_train = ct.CTkButton(mainwindow, text="Start", fg_color="transparent", command=start_training)
    start_train.grid(row=4, column=1, padx=10)

    mainwindow.mainloop()

except pyodbc.Error as e:
    # Failed Error Window:
    error = ct.CTk()
    error.geometry("200x100+800+300")
    error.title("Error")

    errormessage = ct.CTkLabel(error, text="Failed to Connect", text_color="#f00")
    errormessage.pack(side="top")
    
    error.mainloop()