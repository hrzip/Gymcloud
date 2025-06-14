class Osoba:
    def __init__(self, osoba_orm):
        self.orm = osoba_orm

    def prikaz(self):
        print(f"Ime: {self.orm.ime}")
        print(f"Prezime: {self.orm.prezime}")
        print(f"Telefon: {self.orm.telefon}")
        print(f"Email: {self.orm.email}")
