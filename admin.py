from db_setup import SessionLocal

session = SessionLocal()

class Admin:
    def __init__(self, admin_orm):
        self.orm = admin_orm
        self.osoba = admin_orm.osoba

    def osvjezi_podatke(self):
        from skripta_za_bazu import Admin as AdminORM

        session.expire_all()  

        self.orm = session.query(AdminORM).filter_by(id=self.orm.id).one()
        self.osoba = self.orm.osoba

    def admin_izbornik(self, gym):
        while True:
            self.osvjezi_podatke()
            print()
            print("0. Prikaz izvještaja korisnika")            
            print("1. Promijeni lokaciju sprave")
            print("2. Dodaj spravu")
            print("3. Ukloni spravu")
            print("4. Promijeni vježbu (zamijeni spravu)")
            print("5. Ukloni spravu iz vježbe")
            print("6. Dodaj spravu u vježbu")
            print("7. Napravi novu vježbu (program)")
            print("8. Izbriši vježbu (program)")
            print("9. Prikaži sve sprave")
            print("10. Prikaži sve vježbe")
            print("11. Izlazak iz izbornika")

            try:
                izbor_admina = int(input("Što želite napraviti? UPIŠITE BROJ OPCIJE: "))
            except ValueError:
                print("Nevažeći unos.")
                continue

            print()

            if izbor_admina == 0:
                lista_korisnika = gym.prikazi_sve_korisnike()
                for korisnik in lista_korisnika:
                    print(f"ID korisnika: {korisnik[2]}, IME: {korisnik[0]}, PREZIME: {korisnik[1]}")
                
                odabir = int(input("Upišite ID korisnika za prikaz izvještaja: "))
                izvjestaji = gym.prikazi_izvjestaje_odabranog_korisnika(odabir)

                for izv in izvjestaji:
                    izv.prikaz_izvjestaja()
                    print()

            elif izbor_admina == 1:
                nova_lokacija = input("Upišite novu lokaciju: ")
                naziv_sprave = input("Upišite naziv sprave kojoj mijenjamo lokaciju: ")
                gym.promijeni_lokaciju_sprave(naziv_sprave, nova_lokacija)

            elif izbor_admina == 2:
                naziv = input("Upišite naziv nove sprave: ")
                lokacija = input("Upišite lokaciju nove sprave: ")
                gym.dodaj_spravu(naziv, lokacija)

            elif izbor_admina == 3:
                naziv = input("Upišite naziv sprave koju želite obrisati: ")
                gym.ukloni_spravu(naziv)

            elif izbor_admina == 4:
                gym.prikazi_vjezbe()
                naziv_vjezbe = input("Naziv vježbe za promjenu: ")
                naziv_stara = input("Naziv sprave za zamijeniti: ")

                gym.prikazi_sprave()
                naziv_nova = input("Naziv nove sprave: ")
                trajanje = int(input("Trajanje nove sprave (u minutama): "))

                gym.zamijeni_spravu_u_vjezbi(naziv_vjezbe, naziv_stara, naziv_nova, trajanje)

            elif izbor_admina == 5:
                gym.prikazi_vjezbe()
                naziv_vjezbe = input("Naziv vježbe iz koje uklanjate spravu: ")
                naziv_sprave = input("Naziv sprave za uklanjanje: ")
                gym.ukloni_spravu_iz_vjezbe(naziv_vjezbe, naziv_sprave)

            elif izbor_admina == 6:
                gym.prikazi_vjezbe()
                naziv_vjezbe = input("Naziv vježbe: ")
                gym.prikazi_sprave()
                naziv_sprave = input("Naziv sprave za dodavanje: ")
                trajanje = int(input("Trajanje (u minutama): "))
                gym.dodaj_spravu_u_vjezbu(naziv_vjezbe, naziv_sprave, trajanje)

            elif izbor_admina == 7:
                naziv = input("Naziv novog programa: ")
                gym.dodaj_vjezbu(naziv)

            elif izbor_admina == 8:
                naziv = input("Naziv vježbe za brisanje: ")
                gym.izbrisi_vjezbu(naziv)

            elif izbor_admina == 9:
                gym.prikazi_sprave()

            elif izbor_admina == 10:
                gym.prikazi_vjezbe()

            elif izbor_admina == 11:
                break

            else:
                print("Nevažeći izbor. Pokušajte ponovno.")
