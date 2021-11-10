import matplotlib.pyplot as plt
import numpy as np
import csv
from tkinter import *
from PIL import Image, ImageTk
import os
import shutil
import tkinter.font as tkFont
from tkinter.ttk import *
import zipfile

class Automobil:
    global recnik
    recnik = {}

    def __init__(self, marka, model, godiste, cena, datum):
        self.marka = marka
        self.model = model
        self.godiste = godiste
        self.cena = cena
        self.datum = datum

    def kreiraj_recnik(self):
        recnik["Marka"] = self.marka
        recnik["Model"] = self.model
        recnik["Godiste"] = self.godiste
        recnik["Cena"] = self.cena
        recnik["Datum"] = self.datum


def zipovanje():
    grafik_fajlovi = os.listdir("grafik_output")
    zip_fajl = zipfile.ZipFile("grafik_output\\zip_graf.zip", "w")
    
    for i in grafik_fajlovi:
        zip_fajl.write("grafik_output\\"+i, compress_type=zipfile.ZIP_DEFLATED)
        os.remove("grafik_output\\"+i)

    zip_fajl.close()


def provera_datum(d):
    datum_uslovi = []
    if d.count(".") != 3:
        datum_uslovi.append(False)
    else:
        datum_uslovi.append(True)
        date = d.split(".")
        date.remove("")

        if date[0].isdecimal() == False:
            datum_uslovi.append(False)
        else:
            datum_uslovi.append(True)

        if date[1].isdecimal() == False:
            datum_uslovi.append(False)
        else:
            datum_uslovi.append(True)     
        
        if date[2].isdecimal() == False or len(date[2]) != 4:
            datum_uslovi.append(False)
        else:
            datum_uslovi.append(True)

    return datum_uslovi


def provera_marka(x):
    return any (char.isdigit() for char in x)

def provera_unosa():
    unos_marka = marka.get()
    unos_model = model.get()
    unos_godiste = godiste.get()
    unos_cena = cena.get()
    unos_datum = datum.get()

    unos_marka_provera = provera_marka(unos_marka)
    unos_datum_provera = provera_datum(unos_datum)

    t_f = []

    if unos_marka == "" or unos_marka_provera == True:
        t_f.append(False)
    else:
        t_f.append(True)

    if unos_model == "":
        t_f.append(False)
    else:
        t_f.append(True)

    if unos_godiste == "" or unos_godiste.isdecimal() == False:
        t_f.append(False)
    else:
        t_f.append(True)

    if unos_cena == "" or unos_cena.isdecimal() == False:
        t_f.append(False)
    else:
        t_f.append(True)
    

    datum_ispunjeni_uslovi = True
    for i in unos_datum_provera:
        if i == False:  
            datum_ispunjeni_uslovi = False
            break


    if unos_datum == "" or datum_ispunjeni_uslovi == False:
        t_f.append(False)
    else:
        t_f.append(True)

    return t_f


def zatvori():
    root.destroy()

def uvecaj_zarada(x,y):
    plt.clf()
    plt.bar(x,y, label="Zarada u evrima", color="orange")
    plt.ylabel("Zarada u evrima")
    plt.xlabel("Godina")
    plt.title("Zarada od automobila svake godine")
    plt.grid()
    plt.legend()
    plt.show()

def uvecaj_broj(x,y):
    plt.clf()
    plt.bar(x,y, label="Broj prodatih automobila", color="#1c0480")
    plt.legend()
    plt.grid()
    plt.title("Broj prodatih automobila svake godine")
    plt.xlabel("Godine")
    plt.ylabel("Broj prodatih automobila")
    plt.show()


def statistika():
    podaci = open("auto.csv", "r", encoding="utf-8")
    reader_podaci = csv.reader(podaci)

    global ukupna_zarada, prodati_automobili
    ukupna_zarada = 0
    prodati_automobili = 0

    brojac = 1
    for i in reader_podaci:
        if brojac >= 2:
            prodati_automobili += 1
            ukupna_zarada += int(i[3])
        brojac += 1

    podaci.close()


def dugme_dodaj():
    output = provera_unosa()

    ispunjeni_uslovi = True
    for i in output:
        if i == False:
            ispunjeni_uslovi = False
            break

    if ispunjeni_uslovi == True:

        auto = Automobil(marka.get(), model.get(), godiste.get(), cena.get(), datum.get())
        auto.kreiraj_recnik()

        filee = open("auto.csv", "a", encoding="utf-8", newline="")
        writer_file = csv.writer(filee)
        writer_file.writerow([recnik["Marka"], recnik["Model"], recnik["Godiste"], recnik["Cena"], recnik["Datum"]])

        filee.close()

        #if os.path.exists("izvestaji_output") == False:
            #os.makedirs("izvestaji_output")

        txt_izvestaj = open("izvestaj.txt", "a", encoding="utf-8")
        txt_izvestaj.write("- Dana "+recnik["Datum"]+" je prodat automobil marke "+recnik["Marka"]+" "+recnik["Model"]+" "+recnik["Godiste"]+" godiste po ceni od "+recnik["Cena"]+" evra.\n")

        txt_izvestaj.close()


        prozor_izvestaj = Toplevel(root)
        izvestaj_naslov = Label(prozor_izvestaj, text="Uspešno ste dodali automobil u tabelu!", font = font_style_podnaslov, foreground="green")
        izvestaj_naslov.pack()

        izvestaj_tekst = Message(prozor_izvestaj, text="Uspešno ste dodali prodati automobil u tabelu. Na osnovu unetih karakteristika automobila, \nautomatski vam se kreirao i sačuvao izveštaj u txt fajlu poda nazivom izvestaj.txt", font = font_style1, background="green", foreground="white")
        izvestaj_tekst.pack()


        prozor_izvestaj.title("Dodavanje u tabelu")
        prozor_izvestaj.geometry("400x250")
        prozor_izvestaj.resizable(False, False)
        prozor_izvestaj.configure(background="green")

    else:
        prozor_greska = Toplevel(root)
        obavestenje = Label(prozor_greska, text="Greška prilikom unosa!\n\n", foreground="red", font=font_style_podnaslov)
        obavestenje.pack()

        upustvo = Message(prozor_greska, text=
        "Obratite pažnju na sledeće stvari: \n\n* Polje za unos marke automobila ne sme biti prazno i ne sme sadržati brojeve!\n\n* Polje za unos modela automobila ne sme da bude prazno!\n\n* Polje za unos godišta automobila ne sme biti prazno i ne sme sadržati slova!\n\n* Polje za unos cene automobila ne sme biti prazno i ne sme sadržati slova!\n\n* Polje za unos datuma prodaje automobila ne sme biti prazno i mora da bude u gramatičko ispravnom obliku\nPrimer: 1.10.2020.", 
        bg="red", fg="white", font=font_style1)
        upustvo.pack()

        prozor_greska.title("Greska")
        prozor_greska.resizable(False, False)
        prozor_greska.geometry("450x350")
        prozor_greska.configure(background="red")

def o_programu():
    oprogramu = Toplevel(root)
    tekst = Message(oprogramu, text="Ovaj program je napravljen za firme koje se bave prodajom automobila. Omogućava lakše praćenje statistika kao što su: Zarada, broj prodatih automobila, napredak firme itd. Kada se proda neki automobil, u prazna polja se unesu podaci koji se dalje koriste za statistiku. ", background="#1c0480", foreground="#e8fe82", font=font_style1)
    tekst.grid(row=0, column=0, columnspan=2)

    autor = Label(oprogramu, text="Autor: Pokoracki Darko", background="#1c0480", foreground="#e8fe82", font=font_style1)
    autor.grid(row=1, column=0, columnspan=2)

    instagram_izvor = Image.open("instagram.png")
    instagram_izvor = instagram_izvor.resize((60, 60), Image.ANTIALIAS)
    instagram = ImageTk.PhotoImage(instagram_izvor)
    instagram_slika = Label(oprogramu, image=instagram, background="#1c0480", foreground="#e8fe82")
    instagram_slika.image = instagram
    instagram_slika.grid(row=2, column=0)

    facebook_izvor = Image.open("facebook.png")
    facebook_izvor = facebook_izvor.resize((60, 60), Image.ANTIALIAS)
    facebook = ImageTk.PhotoImage(facebook_izvor)
    facebook_slika = Label(oprogramu, image=facebook, background="#1c0480", foreground="#e8fe82")
    facebook_slika.image = facebook
    facebook_slika.grid(row=3, column=0)

    gmail_izvor = Image.open("gmail.png")
    gmail_izvor = gmail_izvor.resize((60, 60), Image.ANTIALIAS)
    gmail = ImageTk.PhotoImage(gmail_izvor)
    gmail_slika = Label(oprogramu, image=gmail, background="#1c0480", foreground="#e8fe82")
    gmail_slika.image = gmail
    gmail_slika.grid(row=4, column=0)

    moj_instagram = Label(oprogramu, text="@darkopokoracki", background="#1c0480", foreground="#e8fe82", font=font_style1)
    moj_instagram.grid(row=2, column=1)

    moj_facebook = Label(oprogramu, text="Darko Pokoracki", background="#1c0480", foreground="#e8fe82", font=font_style1)
    moj_facebook.grid(row=3, column=1)

    moj_gmail = Label(oprogramu, text="darkopokypokoracki@gmail.com", background="#1c0480", foreground="#e8fe82",font=font_style1)
    moj_gmail.grid(row=4, column=1)

    oprogramu.grid_columnconfigure(0, minsize=100)
    oprogramu.grid_columnconfigure(1, minsize=200)

    oprogramu.grid_rowconfigure(0, minsize=150)
    oprogramu.grid_rowconfigure(1, minsize=62)
    oprogramu.grid_rowconfigure(2, minsize=62)
    oprogramu.grid_rowconfigure(3, minsize=62)
    oprogramu.grid_rowconfigure(4, minsize=62)

    oprogramu.title("O programu")
    oprogramu.geometry("300x400")
    oprogramu.configure(background="#1c0480")


def grafik_zarada():
    fajl_zarada = open("auto.csv", "r", encoding="utf-8")
    reader_zarada = csv.reader(fajl_zarada)

    godine = [2016, 2017, 2018, 2019, 2020]
    sume = [0,0,0,0,0]

    counter = 1
    for i in reader_zarada:

        if counter >= 2:
            datum = i[4].split(".")
            datum.remove("")

            if datum[2] == "2016":
                sume[0] += int(i[3])

            if datum[2] == "2017":
                sume[1] += int(i[3])

            if datum[2] == "2018":
                sume[2] += int(i[3])

            if datum[2] == "2019":
                sume[3] += int(i[3])

            if datum[2] == "2020":
                sume[4] += int(i[3])

        counter += 1

    fajl_zarada.close()

    if os.path.exists("grafik_output") == False:
        os.makedirs("grafik_output")

    plt.clf()
    plt.bar(godine, sume, label="Zarada u evrima", color="orange")
    plt.ylabel("Zarada u evrima")
    plt.xlabel("Godina")
    plt.grid()
    plt.title("Zarada od automobila svake godine")
    plt.legend()
    plt.savefig("grafik_output\\zarada.jpg")
    #plt.show()

    global zarada_slika
    zarada_izvor = Image.open("grafik_output\\zarada.jpg")
    zarada_izvor = zarada_izvor.resize((290, 230), Image.ANTIALIAS)
    zarada = ImageTk.PhotoImage(zarada_izvor)
    zarada_slika = Label(root, image = zarada)
    zarada_slika.image = zarada
    zarada_slika.grid(row=3, column=0, rowspan=6)

    global dugme_uvecaj_zarada
    dugme_uvecaj_zarada = Button(root, text="Uvećaj", command = lambda: uvecaj_zarada(godine, sume))
    dugme_uvecaj_zarada.grid(row=9, column=0)


def osvezi():
    data = open("auto.csv", "r", encoding="utf-8")
    reader_data = csv.reader(data)

    ukupna_zaradaa = 0
    prodati_automobilii = 0

    brojac = 1
    for i in reader_data:
        if brojac >= 2:
            prodati_automobilii += 1
            ukupna_zaradaa += int(i[3])
        brojac += 1

    data.close()    
    ukupnaZarada["text"] = f"Ukupna zarada: {ukupna_zaradaa} eu"
    prodatiAutomobili["text"] = f"Broj prodatih automobila: {prodati_automobilii}"

def grafik_broj():
    fajl_broj = open("auto.csv", "r", encoding="utf-8")
    reader_broj = csv.reader(fajl_broj)

    god = [2016, 2017, 2018, 2019, 2020]
    broj_auto = [0,0,0,0,0]

    counter = 1
    for i in reader_broj:
        if counter >= 2:
            datum = i[4].split(".")
            datum.remove("")   

            if datum[2] == "2016":
                broj_auto[0] += 1

            if datum[2] == "2017":
                broj_auto[1] += 1

            if datum[2] == "2018":
                broj_auto[2] += 1

            if datum[2] == "2019":
                broj_auto[3] += 1

            if datum[2] == "2020":
                broj_auto[4] += 1
        counter += 1

    fajl_broj.close()

    if os.path.exists("grafik_output") == False:
        os.makedirs("grafik_output")

    plt.clf()
    plt.bar(god, broj_auto, label="Broj prodatih automobila", color="#1c0480")
    plt.legend()
    plt.grid()
    plt.title("Broj prodatih automobila svake godine")
    plt.xlabel("Godine")
    plt.ylabel("Broj prodatih automobila")
    plt.savefig("grafik_output\\sellcars.jpg")
    #plt.show()

    global sellcars_slika
    sellcars_izvor = Image.open("grafik_output\\sellcars.jpg")
    sellcars_izvor = sellcars_izvor.resize((290, 230), Image.ANTIALIAS)
    sellcars = ImageTk.PhotoImage(sellcars_izvor)
    sellcars_slika = Label(root, image = sellcars)
    sellcars_slika.image = sellcars
    sellcars_slika.grid(row=3, column=4, rowspan=6)

    global dugme_uvecaj_broj
    dugme_uvecaj_broj = Button(root, text="Uvećaj", command = lambda: uvecaj_broj(god, broj_auto))
    dugme_uvecaj_broj.grid(row=9, column=4)



def obrisi():
    marka.delete(0, END)
    marka.insert(0, "")

    model.delete(0, END)
    model.insert(0, "")

    godiste.delete(0, END)
    godiste.insert(0, "")

    cena.delete(0, END)
    cena.insert(0, "")

    datum.delete(0, END)
    datum.insert(0, "")

    zarada_slika.destroy()
    sellcars_slika.destroy()

    dugme_uvecaj_zarada.destroy()
    dugme_uvecaj_broj.destroy()


statistika()
root = Tk()

font_style1 = tkFont.Font(size=10)
font_style_naslov = tkFont.Font(size=18)
font_style_podnaslov = tkFont.Font(size = 13)

#style = Style(root)
#style.configure("W.TButton", font=("calibri", 10, "bold", "underline"), foreground="red")

#Naslov
naslov = Label(root, text="Prodaja automobila", font = font_style_naslov, background="#e8fe82", foreground="#1c0480")
naslov.grid(row=0, column=1, columnspan=3)


#Opis
opis = Message(root, text="Program 'Prodaja automobila' će vam pomoći da vaša firma napreduje. Ovaj program vam tačno pokazuje neke bitne statistike koje će vam pomoći da u buduće vaša firma postane jača. ", font = font_style1, background="#e8fe82" ,foreground="#1c0480")
opis.grid(row=1, column=1, columnspan=3)


#Prva slika - novac
novac_izvor = Image.open("novac.png")
novac_izvor = novac_izvor.resize((290, 180), Image.ANTIALIAS)
novac = ImageTk.PhotoImage(novac_izvor)
novac_slika = Label(root, image = novac)
novac_slika.image = novac
novac_slika.grid(row=0, column=0, rowspan=2)


#Druga slika - Insignia
insignia_izvor = Image.open("insignia.jpg")
insignia_izvor = insignia_izvor.resize((290, 180), Image.ANTIALIAS)
insignia = ImageTk.PhotoImage(insignia_izvor)
insignia_slika = Label(root, image = insignia)
insignia_slika.image = insignia
insignia_slika.grid(row=0, column=4, rowspan=2)


#podnaslov
podnaslov = Label(root, text="Izveštaj o prodatom automobilu:", font = font_style_podnaslov, background="#e8fe82" ,foreground="#1c0480")
podnaslov.grid(row=2, column=1, columnspan=3)


#Dugme zarada
dugme_zarada = Button(root, text="Prikaži zaradu za svaku godinu", command=grafik_zarada)
dugme_zarada.grid(row=2, column=0)


#Dugme broj
dugme_broj = Button(root, text="Prikaži broj prodatih automobila", command=grafik_broj)
dugme_broj.grid(row=2, column=4)


#Unos - Marka
marka_tekst = Label(root, text="Marka :", background="#e8fe82", foreground="#1c0480")
marka_tekst.grid(row=3, column=1)

marka = Entry(root)
marka.grid(row=3, column=2, columnspan=2)


#Unos - Model
model_tekst = Label(root, text="Model :", background="#e8fe82", foreground="#1c0480")
model_tekst.grid(row=4, column=1)

model = Entry(root)
model.grid(row=4, column=2, columnspan=2)


#Unos - Godiste
godiste_tekst = Label(root, text="Godiste :", background="#e8fe82", foreground="#1c0480")
godiste_tekst.grid(row=5, column=1)

godiste = Entry(root)
godiste.grid(row=5, column=2, columnspan=2)


#Unos - Cena
cena_tekst = Label(root, text="Cena (eur) :", background="#e8fe82", foreground="#1c0480")
cena_tekst.grid(row=6, column=1)

cena = Entry(root)
cena.grid(row=6, column=2, columnspan=2)


#Unos - Datum prodaje
datum_tekst = Label(root, text="Datum prodaje:", background="#e8fe82", foreground="#1c0480")
datum_tekst.grid(row=7, column=1)

datum = Entry(root)
datum.grid(row=7, column=2, columnspan=2)


#Dugme dodaj 
dugme_dodaj = Button(root, text="Dodaj u tabelu", command=dugme_dodaj)
dugme_dodaj.grid(row=8, column=1, columnspan=2)


#Dugme obrisi
dugme_obrisi = Button(root, text="Obriši polja", command=obrisi)
dugme_obrisi.grid(row=8, column=3)


ukupnaZarada = Label(root, text=f"Ukupna zarada: {ukupna_zarada} eu", background="#e8fe82", foreground="#1c0480")
ukupnaZarada.grid(row=10, column=1, columnspan=3)


prodatiAutomobili = Label(root, text=f"Broj prodatih automobila: {prodati_automobili}", background="#e8fe82", foreground="#1c0480")
prodatiAutomobili.grid(row=11, column=1, columnspan=3)

#Dugme osvezi
dugme_osvezi = Button(root, text="Osveži", command=osvezi)
dugme_osvezi.grid(row=12, column=1, columnspan=3)

root.title("Prodaja automobila")

"""
###PODESAVANJA###
"""

#Velicina kolona
root.grid_columnconfigure(0, minsize=300)
root.grid_columnconfigure(1, minsize=100)
root.grid_columnconfigure(2, minsize=100)
root.grid_columnconfigure(3, minsize=100)
root.grid_columnconfigure(4, minsize=300)

#Velicina redova
root.grid_rowconfigure(0, minsize=50)
root.grid_rowconfigure(1, minsize=150)
root.grid_rowconfigure(2, minsize=31)
root.grid_rowconfigure(3, minsize=40)
root.grid_rowconfigure(4, minsize=40)
root.grid_rowconfigure(5, minsize=40)
root.grid_rowconfigure(6, minsize=40)
root.grid_rowconfigure(7, minsize=40)
root.grid_rowconfigure(8, minsize=40)
root.grid_rowconfigure(9, minsize=31)
root.grid_rowconfigure(10, minsize=31)
root.grid_rowconfigure(11, minsize=31)
root.grid_rowconfigure(12, minsize=31)

root.geometry("900x600")
root.resizable(False, False)

"""
MENI i PODMENI
"""
meni = Menu(root)
meni.add_command(label="O programu", command=o_programu)
root.config(menu=meni, bg="#e8fe82")
 


podmeni = Menu(meni, tearoff=0)
meni.add_cascade(label="Datoteka", menu=podmeni)
podmeni.add_command(label="Zipuj grafikone", command=zipovanje)
podmeni.add_command(label="Zatvori program", command=zatvori)



root.mainloop()
