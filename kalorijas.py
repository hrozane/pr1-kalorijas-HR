import sqlite3
# !!!

def main():
    print("Programma ļauj apskatīt edienreizu datubāzi un veikt dažādas darbības ar tās ierakstiem.")
    with sqlite3.connect("kalorijas.db") as conn:
        c = conn.cursor()
        izvele(c)

def izvele(c):
    while True:
        print("\nIzvēlnes iespējas:")
        print("1 - Aprēķināt nepieciešamās kalorijas")
        print("2 - Pievienot ēdienreizes")
        print("3 - Saglabāt ēdienreizes")
        print("4- apskatīt atlikušās dienas kalorijas")
        print("5- pārrestartēt dienu")
        print("6- mainīt lietotāja datus")

        print("0 - Iziet")
        
        choice = input("Izvēlies darbību: ")

        if choice == "1":
            aprekins_nep(c)
        elif choice == "2":
            ediens(c)
        elif choice == "3":
            reizes(c)
        #elif choice == "4":
            #atlikusas_kalorijas(c)
            
        elif choice == "0":
            print("Programma beidzas.")
            break
        else:
            print("Nederīga izvēle. Mēģini vēlreiz.")
    
def aprekins_nep(c):
    
    while True:
        try:
            id = int(input("Ievadi savu id:"))
            vards = input("Ievadi savu vārdu:")
            uzvards = input("Ievadi savu uzvārdu:")
            
            dzimums = input("Ievadi savu dzimumu:")
            dzimums = dzimums.lower()
            vecums = int(input("Ievadi savu vecumu:"))
            augums = int(input("Ievadi savu augumu centimetros:"))
            svars = float(input("Ievadi savu svaru kilogramos"))
            jauta = input("Kāds ir tavs aktivitātes līmenis?-Mazkustīgs,Viegls,Vidējs,Augsts,Ļoti augsts")
            jauta.capitalize()

            akt_limenis = {"Mazkustīgs": 1.2,"Viegls": 1.375,"Vidējs": 1.55,"Augsts": 1.725,"Ļoti augsts": 1.9}
            lvl = akt_limenis.get(f"{jauta}")
            
            
            
            if dzimums == "vīrietis":
                nep_kalorijas = lvl*(88.362+13.397*svars+4.799*augums-5.677*vecums)
                nep_kalorijas = round(nep_kalorijas)
            elif dzimums == "sieviete":
                nep_kalorijas =lvl*(447.593+9.247*svars+3.098*augums-4.33*vecums)
                nep_kalorijas = round(nep_kalorijas)
            else:
                print("Nepareizs dzimums.")
                continue

            
            vaic = f"INSERT INTO lietotajs (id, vards, uzvards, dzimums, vecums, augums, svars, akt_limenis, nep_kalorijas) VALUES ({id}, \"{vards}\" ,\"{uzvards}\", \"{dzimums}\" ,{vecums}, {augums}, {svars}, {lvl}, {nep_kalorijas})"
            print(vaic)
            print(nep_kalorijas)
            c.execute(vaic)
            turpinam = izvele(c)
            print(turpinam)
           
        except ValueError:
            print("Nepareiza ievade.Lūdzu mēģini vēlreiz!")




def ediens(c):
    edienu_saraksts = [{}]
    while True:
        try:
            id = int(input("Ievadi savu id:"))
            edienreize = input("Ievadi savu edienu:")
            
            ogh = int(input("Ievadi ogļhidrātu daudzumu:"))
            obv = int(input("Ievadi olbaltumvielu daudzumu:"))
            tauki = int(input("Ievadi tauku daudzumu ēdienā:"))

            ogh_daudz = ogh*4.2
            obv_daudz = obv*4.2
            tauku_daudz = tauki*9.3

            kalorijas_ediena = ogh_daudz+obv_daudz+tauku_daudz
            vaic = f"INSERT INTO ediens = {id} \"{edienreize}\"\"{ogh}\"\"{obv}\"\"{tauki}\"\"{kalorijas_ediena}\""
            print(f"Tu esi paēdis {edienreize}, kurās bija {kalorijas_ediena} kalorijas.")

            c.execute(vaic)
            turpinam = izvele(c)
            print(turpinam)
            edienu_saraksts.append({"id": id, "edienreize": edienreize,"kalorijas": kalorijas_ediena})
            print(edienu_saraksts)
        
        except ValueError:
            print("Kļūda datu ievadē!")
        reizes(c,id, edienreize, kalorijas_ediena)




def reizes(c, id,edienreize, kalorijas_ediena):

    for id, edienreize, kalorijas_ediena in ediens:
        c.execute(f"INSERT INTO Reizes (id, edienreize, kalorijas_ediena) VALUES \"{id}\" \"{edienreize}\"\"{kalorijas_ediena}\"")
    
    
#def atlikusas_kalorijas(c,nep_kalorijas,kalorijas_ediena):

    #atlikusas = nep_kalorijas-kalorijas_ediena
    


if __name__ == "__main__":
    main()