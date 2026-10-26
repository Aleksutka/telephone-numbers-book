import customtkinter as ctk
import os
from pathlib import Path

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Kontaktu grāmatiņa")
app.geometry("760x520")
app.minsize(680, 480)

main_path = Path.home() / "Documents"
folder_path = main_path / "Kontakti"

os.makedirs(folder_path, exist_ok=True)

tagad = ""
name = ""
file_path = ""


def set_status(message):
    txt.configure(text=message)


def start_action(action, prompt):
    global tagad
    tagad = action
    set_status(prompt)
    inp.delete(0, "end")
    inp.configure(placeholder_text="Ievadiet vārdu")
    buttApst.configure(text="Turpināt")
    buttApst.grid()
    inp.focus()


def pievienot():
    start_action("name", "Pievienojiet jaunu kontaktu")


def atrast():
    start_action("atrast", "Meklējiet kontaktu pēc vārda")


def izdzest():
    start_action("izdzest", "Ievadiet dzēšamā kontakta vārdu")


def visi():
    names = []
    for file in os.listdir(folder_path):
        name, ext = os.path.splitext(file)
        if ext.lower() == ".txt":
            names.append(name)

    conTxt.configure(state="normal")
    conTxt.delete("1.0", "end")
    if names:
        conTxt.insert("1.0", "\n".join(f"•  {contact}" for contact in sorted(names)))
    else:
        conTxt.insert("1.0", "Kontaktu vēl nav.\nPievienojiet savu pirmo kontaktu.")
    conTxt.configure(state="disabled")
    contact_count.configure(text=f"{len(names)} kontakti")


def finish_action(message):
    global tagad
    tagad = ""
    set_status(message)
    inp.delete(0, "end")
    inp.configure(placeholder_text="Izvēlieties darbību")
    buttApst.grid_remove()
    buttApst.configure(text="Turpināt")


def turp():
    global tagad, name, number, file_path
    if tagad == "name":
        name = inp.get().strip().lower()
        if not name:
            set_status("Lūdzu, ievadiet vārdu.")
            return
        inp.delete(0, "end")
        inp.configure(placeholder_text="Ievadiet telefona numuru")
        set_status("Tagad ievadiet telefona numuru")
        tagad = "number"
    elif tagad == "number":
        number = inp.get().strip().lower()
        if not number:
            set_status("Lūdzu, ievadiet telefona numuru.")
            return
        inp.delete(0, "end")
        try:
            file_path = os.path.join(folder_path, f"{name}.txt")
            with open(file_path, "x") as f:
                f.write(number)
            finish_action(f"Kontakts “{name}” veiksmīgi pievienots.")
            visi()
        except FileExistsError:
            finish_action("Šāds vārds jau eksistē.")
    elif tagad == "atrast":
        name = inp.get().strip().lower()
        if not name:
            set_status("Lūdzu, ievadiet vārdu.")
            return
        file_path = os.path.join(folder_path, f"{name}.txt")
        try:
            with open(file_path) as f:
                number = f.read()
            finish_action(f"{name}\n{number}")
        except FileNotFoundError:
            finish_action(f"Kontakts “{name}” nav atrasts.")
    elif tagad == "izdzest":
        name = inp.get().strip().lower()
        if not name:
            set_status("Lūdzu, ievadiet vārdu.")
            return
        file_path = os.path.join(folder_path, f"{name}.txt")
        if os.path.exists(file_path):
            inp.delete(0, "end")
            set_status(f"Vai tiešām dzēst kontaktu “{name}”?")
            tagad = "yes"
            buttApst.configure(text="Dzēst kontaktu")
        else:
            finish_action(f"Kontakts “{name}” nav atrasts.")
    elif tagad == "yes":
        os.remove(file_path)
        finish_action(f"Kontakts “{name}” tika dzēsts.")
        visi()


app.grid_columnconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=1)

header = ctk.CTkFrame(app, fg_color="transparent")
header.grid(row=0, column=0, sticky="ew", padx=28, pady=(24, 12))
header.grid_columnconfigure(0, weight=1)

title = ctk.CTkLabel(
    header,
    text="Kontaktu grāmatiņa",
    font=ctk.CTkFont(family="Arial", size=27, weight="bold"),
)
title.grid(row=0, column=0, sticky="w")

subtitle = ctk.CTkLabel(
    header,
    text="Vienkārši pārvaldiet savus kontaktus",
    text_color=("gray40", "gray70"),
    font=ctk.CTkFont(size=13),
)
subtitle.grid(row=1, column=0, sticky="w", pady=(3, 0))

content = ctk.CTkFrame(app, fg_color="transparent")
content.grid(row=1, column=0, sticky="nsew", padx=28, pady=(4, 24))
content.grid_columnconfigure(0, weight=1, uniform="cards")
content.grid_columnconfigure(1, weight=1, uniform="cards")
content.grid_rowconfigure(0, weight=1)

actions_card = ctk.CTkFrame(content, corner_radius=16)
actions_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
actions_card.grid_columnconfigure((0, 1), weight=1)

actions_title = ctk.CTkLabel(
    actions_card,
    text="Darbības",
    font=ctk.CTkFont(size=18, weight="bold"),
)
actions_title.grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(20, 12))

btnPie = ctk.CTkButton(
    actions_card, text="＋  Pievienot kontaktu", command=pievienot, height=42
)
btnPie.grid(row=1, column=0, columnspan=2, sticky="ew", padx=20, pady=5)

btnAtr = ctk.CTkButton(
    actions_card,
    text="⌕  Atrast kontaktu",
    command=atrast,
    height=40,
    fg_color=("gray82", "gray25"),
    text_color=("gray10", "gray90"),
    hover_color=("gray75", "gray32"),
)
btnAtr.grid(row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=5)

btnIzdz = ctk.CTkButton(
    actions_card,
    text="Dzēst kontaktu",
    command=izdzest,
    height=40,
    fg_color="transparent",
    border_width=1,
    text_color=("gray20", "gray85"),
)
btnIzdz.grid(row=3, column=0, columnspan=2, sticky="ew", padx=20, pady=5)

txt = ctk.CTkLabel(
    actions_card,
    text="Izvēlieties darbību, lai sāktu.",
    font=ctk.CTkFont(size=13),
    text_color=("gray40", "gray70"),
    wraplength=290,
    justify="left",
    anchor="w",
)
txt.grid(row=4, column=0, columnspan=2, sticky="ew", padx=20, pady=(15, 8))

inp = ctk.CTkEntry(
    actions_card,
    placeholder_text="Izvēlieties darbību",
    height=40,
    corner_radius=10,
)
inp.grid(row=5, column=0, sticky="ew", padx=(20, 5), pady=(0, 20))
inp.bind("<Return>", lambda event: turp())

buttApst = ctk.CTkButton(
    actions_card,
    text="Turpināt",
    command=turp,
    width=100,
    height=40,
    corner_radius=10,
)
buttApst.grid(row=5, column=1, sticky="ew", padx=(5, 20), pady=(0, 20))
buttApst.grid_remove()

contacts_card = ctk.CTkFrame(content, corner_radius=16)
contacts_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
contacts_card.grid_columnconfigure(0, weight=1)
contacts_card.grid_rowconfigure(1, weight=1)

contacts_heading = ctk.CTkLabel(
    contacts_card,
    text="Jūsu kontakti",
    font=ctk.CTkFont(size=18, weight="bold"),
)
contacts_heading.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 0))

contact_count = ctk.CTkLabel(
    contacts_card,
    text="Atjauniniet sarakstu",
    text_color=("gray45", "gray65"),
    font=ctk.CTkFont(size=12),
)
contact_count.grid(row=0, column=1, sticky="e", padx=20, pady=(20, 0))

conTxt = ctk.CTkTextbox(
    contacts_card,
    corner_radius=10,
    border_width=0,
    font=ctk.CTkFont(size=14),
    wrap="word",
)
conTxt.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=16, pady=16)
conTxt.insert("1.0", "Nospiediet “Visi kontakti”, lai parādītu saglabātos kontaktus.")
conTxt.configure(state="disabled")

btnVisi = ctk.CTkButton(
    contacts_card,
    text="Atjaunināt kontaktu sarakstu",
    command=visi,
    height=38,
    fg_color=("gray82", "gray25"),
    text_color=("gray10", "gray90"),
    hover_color=("gray75", "gray32"),
)
btnVisi.grid(row=2, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 16))

app.mainloop()