import customtkinter as ctk
import os
from pathlib import Path

app = ctk.CTk()
app.title("Telefona nummuru grāmatiņa")
app.geometry("390x370")
app.resizable(width=False, height=False)

main_path = Path.home() / "Documents"
folder_path = main_path / "Kontakti"

os.makedirs(folder_path, exist_ok=True)

def pievienot():
    global tagad
    tagad = "name"
    txt.configure(text="Ievadiet lototāju!")
    buttApst.place(x=160, y=65)
    
def atrast():
    global tagad
    tagad = "atrast"
    txt.configure(text="Ievadiet vārdu!")
    buttApst.place(x=160, y=65)
    
def izdzest():
    global tagad
    tagad = "izdzest"
    txt.configure(text="Ievadiet vārdu kuru izdzēst!")
    buttApst.place(x=160, y=65)

def visi():
    names = []
    for file in os.listdir(folder_path):
        name, ext = os.path.splitext(file)
        if ext.lower() == ".txt":
            names.append(name)
    if names:
        conTxt.configure(text="Visi kontakti:\n" + "\n".join(sorted(names)))
    else:
        conTxt.configure(text="Kontaktu vēl nav.")
        
def turp():
    global tagad, name, number, file_path
    if tagad == "name":
        name = inp.get().strip().lower()
        inp.delete(0, "end")
        txt.configure(text="Ievadiet telefona numuru!")
        tagad = "number"
    elif tagad == "number":
        number = inp.get().strip().lower()
        inp.delete(0, "end")
        try:
            file_path = os.path.join(folder_path, f"{name}.txt")
            with open(file_path, "x") as f:
                f.write(number)
            txt.configure(text="Jūs pievienojāt jaunu litotāja nummuru")
        except FileExistsError:
            txt.configure(text="Tāds vārds jau eksistē!")
        tagad = "name"
        buttApst.grid_remove()
    elif tagad == "atrast":
        try:
            name = inp.get().strip().lower()
            inp.delete(0, "end")
            file_path = os.path.join(folder_path, f"{name}.txt")
            with open(file_path) as f:
                txt.configure(text=f.read())
            buttApst.grid_remove()
        except:
            txt.configure(text="Notika kaut kāda kļūda!")
    elif tagad == "izdzest":
        try:
            name = inp.get().strip().lower()
            inp.delete(0, "end")
            file_path = os.path.join(folder_path, f"{name}.txt")
            if os.path.exists(file_path):
                txt.configure(text=f"Tiešām izdēst kontaktu: {name}?")
                tagad = "yes"
            else:
                txt.configure(text="Fails neeksistē!")
                buttApst.grid_remove()
        except:
            txt.configure(text="Kaut kas sagāja greizi!")
            buttApst.grid_remove()
    elif tagad == "yes":
        os.remove(file_path)
        txt.configure(text="Kontakts tika izdzēsts!")

txt = ctk.CTkLabel(app, text="", font=("Arial", 20))
txt.place(relx=0.5, y=20, anchor="n")

buttApst = ctk.CTkButton(app, text="✅", command=turp, width=35, height=35, fg_color="transparent")
buttApst.grid_remove()

inp = ctk.CTkEntry(app, justify="center", placeholder_text="", width=150, height=35)
inp.place(x=5, y=65)

btnPie = ctk.CTkButton(app, text="Pievienot nummuru", command=pievienot, height=35, width=150)
btnPie.place(x=5, y=110)

btnAtr = ctk.CTkButton(app, text="Atrast nummuru", command=atrast, height=35, width=150)
btnAtr.place(x=5, y=155)

btnIzdz = ctk.CTkButton(app, text="Izdzēst kontaktu", command=izdzest, height=35, width=150)
btnIzdz.place(x=5, y=200)

btnVisi = ctk.CTkButton(app, text="Visi kontakti", command=visi, height=35, width=150)
btnVisi.place(x=5, y=245)

conTxt = ctk.CTkLabel(app, text="", font=("Arial", 20))
conTxt.place(x=220, y=65)

app.mainloop()