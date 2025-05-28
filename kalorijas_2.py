import sqlite3

# !!!

def main():

    print("Programma ļauj apskatīt edienreizu datubāzi un veikt dažādas darbības ar tās ierakstiem.")#lietotāju iepazīstina ar programmu

    with sqlite3.connect("kalorijas_db.db") as conn: #šo kodu savienu ar datubāzi

        c = conn.cursor()

        izvele(c)

def izvele(c):

    while True:

        print("\nIzvēlnes iespējas:") #lietotājam piedāvā izvēlēties veicamo darbību

        print("1 - Aprēķināt nepieciešamās kalorijas")

        print("2 - Pievienot ēdienreizes")

        print("3 - apskatīt atlikušās dienas kalorijas")

        print("4 - Iziet")

       

        choice = input("Izvēlies darbību: ")# lietotāja izvēle tiks novirzīta uz konkrēto funkciju

        if choice == "1":  

            aprekins_nep(c)

        elif choice == "2":

            ediens(c)

        elif choice == "3":

            atlikusas_kalorijas(c)

        elif choice == "4":

            print("Programma beidzas.") #Vairāk tālākas darbības nenotiek

            break

        else:

            print("Nederīga izvēle. Mēģini vēlreiz.") #Strādā, kad ievadīta kļūdaina informācija

   

def aprekins_nep(c):

   

    while True:

        try: #lietotājam uzdod jautājumus un ievāc informāciju, ko saglabā datubāzē

            id = int(input("Ievadi savu id:"))

            vards = input("Ievadi savu vārdu:")

            uzvards = input("Ievadi savu uzvārdu:")

           

            dzimums = input("Ievadi savu dzimumu:")

            dzimums = dzimums.lower()

            vecums = int(input("Ievadi savu vecumu:"))

            augums = int(input("Ievadi savu augumu centimetros:"))

            svars = float(input("Ievadi savu svaru kilogramos"))

            jauta = input("Kāds ir tavs aktivitātes līmenis?-Mazkustīgs,Viegls,Vidējs,Augsts,Ļoti augsts").capitalize()


            akt_limenis = {"Mazkustīgs": 1.2,"Viegls": 1.375,"Vidējs": 1.55,"Augsts": 1.725,"Ļoti augsts": 1.9}#Vārdnīca ar koeficientiem, ko izmantosim priekš aprēķiniem

            lvl = akt_limenis.get(f"{jauta}")

           

           

           

            if dzimums == "vīrietis": #Programma aprēķina nepieciešamās uzņemamās kalorijas dienas laikā

                nep_kalorijas = lvl*(88.362+13.397*svars+4.799*augums-5.677*vecums)

                nep_kalorijas = round(nep_kalorijas)

            elif dzimums == "sieviete":

                nep_kalorijas =lvl*(447.593+9.247*svars+3.098*augums-4.33*vecums)

                nep_kalorijas = round(nep_kalorijas)

            else:

                print("Nepareizs dzimums.")#Tiek izsaukta, ja iepriekš ievadīta kļūdaina informācija

                continue

           

            vaic = f"INSERT INTO lietotajs (id, vards, uzvards, dzimums, vecums, augums, svars, akt_limenis, nep_kalorijas) VALUES ({id}, \"{vards}\" ,\"{uzvards}\", \"{dzimums}\" ,{vecums}, {augums}, {svars}, {lvl}, {nep_kalorijas})"

            print(vaic) #Programma norāda lietotāja ievadīto un programmas izrēķināto informāciju

            print(nep_kalorijas)

            c.execute(vaic)#Lietotāja ievadītie dati tiek ievietoti datubāzē
            c.connection.commit()#Visiem INSERT,UPDATE utt beigās pieraksti šito

            turpinam = izvele(c)#Lietotājam pasniedz sākotnējo izvēlni.

            print(turpinam)

           

        except ValueError:

            print("Nepareiza ievade.Lūdzu mēģini vēlreiz!") #Programma rāda, ja ievadītā informācija neatbilst prasītajam

def ediens(c):

    edienu_saraksts = [{}]

    while True:

        try: #Lietotājs ievada prasīto informāciju

            id = int(input("Ievadi savu id:"))

            edienreize = input("Ievadi savu edienu:")

           

            ogh = int(input("Ievadi ogļhidrātu daudzumu:"))

            obv = int(input("Ievadi olbaltumvielu daudzumu:"))

            tauki = int(input("Ievadi tauku daudzumu ēdienā:"))

            ogh_daudz = ogh*4.2 #Programma izrēķina kaloriju daudzumu ēdienā

            obv_daudz = obv*4.2

            tauku_daudz = tauki*9.3

            kalorijas_ediena = ogh_daudz+obv_daudz+tauku_daudz

            vaic = f"INSERT INTO ediens  (id,edienreize,ogh,obv,tauki,kalorijas_ediena) VALUES ({id} ,\"{edienreize}\",{ogh},{obv},{tauki},{kalorijas_ediena})" #programma pievieno lietotāja ievadīto informāciju datubāzei

            print(f"Tu esi paēdis {edienreize}, kurās bija {kalorijas_ediena} kalorijas.") #Parāda lietotājam cik kalorijas ir tā ēdienā
            print(vaic)

            c.execute(vaic)
            c.connection.commit()

            turpinam = izvele(c) #Izsauc sākuma izvēlni

            print(turpinam)

            edienu_saraksts.append({"id": id, "edienreize": edienreize,"kalorijas": kalorijas_ediena})

            print(edienu_saraksts)

       

        except ValueError:

            print("Kļūda datu ievadē!")

#def reizes(c, id,edienreize, kalorijas_ediena):

    #for id, edienreize, kalorijas_ediena in ediens:

        #c.execute(f"INSERT INTO Reizes (id, edienreize, kalorijas_ediena) VALUES \"{id}\" \"{edienreize}\"\"{kalorijas_ediena}\"")

   

   

def atlikusas_kalorijas(c):

    try:

        id = int(input("Ievadi savu id: "))

        c.execute(f"SELECT nep_kalorijas FROM lietotajs WHERE id = {id}")#Programma sameklē lietotāja nepieciešamo kalorijas daudzumu dienā no datubāzes

        rez = c.fetchone()

        if rez:
 #Programma saskaita visas kalorijas no konkrētās dienas ēdieniem
            nep_kalorijas = rez[0]

            c.execute(f"SELECT SUM(kalorijas_ediena) FROM ediens")
            sum_rez = c.fetchone()
            uznemtas_kalorijas = sum_rez[0] if sum_rez[0] is not None else 0
            

            atlikusas = nep_kalorijas - uznemtas_kalorijas

            
            print(f"Atlikušās dienas kalorijas: {atlikusas}")#Programma parāda un aprēķina cik kalorijas vēl lietotājs var ēst

        else:

            print("Lietotājs nav atrasts.")

    except ValueError:

        print("Kļūda datu ievadē!")

   

#def parrestartet_dienu(c):

    #try:

        #id = int(input("Ievadi savu id: "))

        #c.execute(f"DELETE FROM Reizes WHERE id = {id}) #programma izdzēš visu informāciju par iepriekšējās dienas ēšanas paradumiem.")

        #print("Diena veiksmīgi pārstartēta.")

    #except ValueError:

        #print("Kļūda datu ievadē!")

if __name__ == "__main__":

    main()
