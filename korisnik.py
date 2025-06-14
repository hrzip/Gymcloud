from db_setup import SessionLocal
from skripta_za_bazu import VjezbaProgram as VjezbaProgramORM, ListaKorisnikovihPrograma, Izvjestaj as IzvjestajORM, VjezbaProgramSprave, Sprave
from izvjestaj import IzvjestajWrapper


session = SessionLocal()

class Korisnik:
    def __init__(self, korisnik_orm):
        self.orm = korisnik_orm
        self.osoba = korisnik_orm.osoba  
        latest = (
            session.query(IzvjestajORM)
            .filter_by(osoba_id=self.osoba.id)
            .order_by(IzvjestajORM.id.desc())
            .first()
        )

        self.zadnji_izvjestaj = IzvjestajWrapper(latest) if latest else None

    def osvjezi_podatke(self):
        from skripta_za_bazu import Korisnik as KorisnikORM

        session.expire_all() 
        self.orm = session.query(KorisnikORM).filter_by(id=self.orm.id).one()
        self.osoba = self.orm.osoba

    def prikazi_podatke(self):
        print(f"Ime: {self.osoba.ime}")
        print(f"Prezime: {self.osoba.prezime}")
        print(f"Telefon: {self.osoba.telefon}")
        print(f"Email: {self.osoba.email}")
        print(f"Težina: {self.orm.tezina} kg")
        print(f"Visina: {self.orm.visina} cm")
        print(f"Godine: {self.orm.dob}")
        print(f"Spol: {self.orm.spol}")
        print(f"Broj programa: {len(self.orm.programi)}")
        for program in self.orm.programi:
            print(f"- {program.naziv}")

        print("\n")

    def izaberi_program(self, vjezba_orm):
        from skripta_za_bazu import ListaKorisnikovihPrograma
        nova_veza = ListaKorisnikovihPrograma(korisnik_id=self.orm.id, id_programa=vjezba_orm.id)
        session.add(nova_veza)
        session.commit()

    def ukloni_program(self, vjezba_orm):
        veza = session.query(ListaKorisnikovihPrograma).filter_by(
            korisnik_id=self.orm.id, id_programa=vjezba_orm.id
        ).one_or_none()
        if veza:
            session.delete(veza)
            session.commit()

    def vjezbaj(self, gym):
        print("Ponuđeni programi: ")
        programi = self.orm.programi

        for i, program in enumerate(programi):
            print(f"{i+1} - {program.naziv}")


        unos = int(input("Izaberi broj programa: "))
        odabrani_program = programi[unos - 1]


        sprave_vezane = (
        session.query(VjezbaProgramSprave, Sprave)
        .join(Sprave, VjezbaProgramSprave.id_sprave == Sprave.id)
        .filter(VjezbaProgramSprave.id_vjezbe == odabrani_program.id)
        .all()
        )

        for veza, sprava in sprave_vezane:
            print(f"Vaše vježbe su: {sprava.naziv} - trajanje: {veza.trajanje} minuta")


        if input("Želite krenuti sa programom? Da / Ne: ").lower() == "da":
            for veza, sprava in sprave_vezane:
                print(f"Započeli ste sa vježbom {sprava.naziv}")
                input("Kada ste gotovi sa vježbom upišite bilo što: ")
                print(f"{self.osoba.ime} {self.osoba.prezime} vježbao/la je {veza.trajanje} min na {sprava.naziv} ({sprava.lokacija})\n")


            print("Bravo! Vježbanje završeno.")
            gym.dodaj_izvjestaj_nakon_vjezbe(odabrani_program, self)
            self.zadnji_izvjestaj = IzvjestajWrapper(session.query(IzvjestajORM).order_by(IzvjestajORM.id.desc()).first())



    def korisnik_izbornik(self, gym):
        while True:
            print("""
0. KRENI VJEŽBATI
1. Promijeni težinu
2. Promijeni visinu
3. Promijeni dob
4. Promijeni ime
5. Promijeni prezime
6. Promijeni email
7. Promijeni telefon
8. Promijeni spol
9. Odaberi novi program vježbanja
10. Ukloni program vježbanja
11. Prikaži izvještaj vježbanja
12. Prikaži moje podatke
13. Izlazak iz izbornika
""")
            izbor = input("Što želite napraviti? ")
            print()
            self.osvjezi_podatke()
            if izbor == "0":
                self.vjezbaj(gym)
            elif izbor == "1":
                self.orm.tezina = float(input("Nova težina: "))
            elif izbor == "2":
                self.orm.visina = float(input("Nova visina: "))
            elif izbor == "3":
                self.orm.dob = int(input("Nova dob: "))
            elif izbor == "4":
                self.osoba.ime = input("Novo ime: ")
            elif izbor == "5":
                self.osoba.prezime = input("Novo prezime: ")
            elif izbor == "6":
                self.osoba.email = input("Novi email: ")
            elif izbor == "7":
                self.osoba.telefon = input("Novi telefon: ")
            elif izbor == "8":
                self.orm.spol = input("Novi spol: ")
            elif izbor == "9":
                gym.prikazi_vjezbe()
                naziv = input("Naziv programa za dodati: ")
                vjezba = session.query(VjezbaProgramORM).filter_by(naziv=naziv).first()
                if vjezba:
                    self.izaberi_program(vjezba)
            elif izbor == "10":
                for i, veza in enumerate(self.orm.vjezbe_vezani):
                    print(f"{i+1} - {veza.vjezba.naziv}")
                unos = int(input("Broj programa za uklanjanje: "))
                self.ukloni_program(self.orm.vjezbe_vezani[unos - 1].vjezba)
            elif izbor == "11":
                if self.zadnji_izvjestaj:
                    self.zadnji_izvjestaj.prikaz_izvjestaja()
                else:
                    print("Još nema izvještaja.")
            elif izbor == "12":
                self.prikazi_podatke()
            elif izbor == "13":
                session.commit()
                break
            else:
                print("Nevažeći unos.")
