while True:
    inp1 = input("Pievienot/Atrast/Iziet\n")

    if inp1 == "Pievienot":
        inp2 = input("Cilvēka vārds: ")
        inp3 = input("Cilvēka telefona nummurs: ")
        try:
            f = open(f"{inp2}.txt", "x")
            with open(f"{inp2}.txt", "w") as f:
                f.write(inp3)
            continue
        except:
            print("Tāds vārds grāmatiņā jau eksistē!")
            continue
    elif inp1 == "Atrast":
        inp2 = input("Cilvēka vārds: ")
        try:
            with open(f"{inp2}.txt") as f:
                print(f.read())
            continue
        except:
            print("Nav atrasts tāds kontakts!")
            continue
    elif inp1 == "Iziet":
        print("Izeju no programmas...")
        break
    else:
        print("Uzraskti kaut ko no tā kas ir dots!")