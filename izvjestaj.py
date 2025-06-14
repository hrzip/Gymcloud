class IzvjestajWrapper:
    def __init__(self, izvjestaj_orm):
        self.orm = izvjestaj_orm

    def prikaz_izvjestaja(self):
        osoba = self.orm.osoba
        print(f"Ime: {osoba.ime}")
        print(f"Prezime: {osoba.prezime}")
        print(f"Telefon: {osoba.telefon}")
        print(f"Email: {osoba.email}")
        print(f"Težina: {self.orm.tezina} kg")
        print(f"Visina: {self.orm.visina} cm")
        print(f"Godine: {self.orm.dob}")
        print(f"Spol: {self.orm.spol}")

        vjezba = self.orm.vjezba
        print(f"Program: {vjezba.naziv}")

        for sprava in vjezba.sprave:
            from skripta_za_bazu import VjezbaProgramSprave
            from db_setup import SessionLocal
            
            session = SessionLocal()

            veza = session.query(VjezbaProgramSprave).filter_by(
                id_vjezbe=vjezba.id, id_sprave=sprava.id
            ).first()

            trajanje = veza.trajanje if veza else "?"
            print(f"Sprava: {sprava.naziv} – trajanje: {trajanje} min")
