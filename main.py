from db_setup import SessionLocal
from skripta_za_bazu import Gym as GymORM, Osoba as OsobaORM, Korisnik as KorisnikORM, Admin as AdminORM
from gym import Gym
from korisnik import Korisnik
from admin import Admin

session = SessionLocal()

def dodaj_osobu():
    ime = input("Ime: ")
    prezime = input("Prezime: ")
    telefon = input("Telefon: ")
    email = input("Email: ")
    nova = OsobaORM(ime=ime, prezime=prezime, telefon=telefon, email=email)
    session.add(nova)
    session.commit()
    return nova

def dodaj_korisnika():
    osoba = dodaj_osobu()
    tezina = float(input("Težina (kg): "))
    visina = float(input("Visina (cm): "))
    dob = int(input("Dob: "))
    spol = input("Spol (M/F): ")

    novi = KorisnikORM(osoba_id=osoba.id, tezina=tezina, visina=visina, dob=dob, spol=spol)
    session.add(novi)
    session.commit()

def dodaj_admina():
    osoba = dodaj_osobu()
    novi = AdminORM(osoba_id=osoba.id)
    session.add(novi)
    session.commit()

def dodaj_gym():
    naziv = input("Naziv Gyma: ")
    novi = GymORM(naziv=naziv)
    session.add(novi)
    session.commit()

def izaberi_korisnika():
    korisnici = session.query(KorisnikORM).all()
    if not korisnici:
        print("Nema korisnika.")
        return None
    print("\n=== Popis korisnika ===")
    for k in korisnici:
        print(f"{k.id}: {k.osoba.ime} {k.osoba.prezime}")
    izbor = int(input("Unesite ID korisnika: "))
    return session.query(KorisnikORM).filter_by(id=izbor).one_or_none()

def izaberi_admina():
    admini = session.query(AdminORM).all()
    if not admini:
        print("Nema admina.")
        return None
    print("\n=== Popis admina ===")
    for a in admini:
        print(f"{a.id}: {a.osoba.ime} {a.osoba.prezime}")
    izbor = int(input("Unesite ID admina: "))
    return session.query(AdminORM).filter_by(id=izbor).one_or_none()

def izaberi_gym():
    gymovi = session.query(GymORM).all()
    if not gymovi:
        print("Nema gymova.")
        return None
    print("\n=== Dostupni Gymovi ===")
    for g in gymovi:
        print(f"{g.id}: {g.naziv}")
    izbor = int(input("Unesite ID gyma: "))
    return session.query(GymORM).filter_by(id=izbor).one_or_none()

def main():
    while True:
        print("\n=== GLAVNI IZBORNIK ===")
        print("1 - Dodaj Gym")
        print("2 - Dodaj Korisnika")
        print("3 - Dodaj Admina")
        print("4 - Prijava kao postojeći Korisnik")
        print("5 - Prijava kao postojeći Admin")
        print("0 - Izlaz")
        izbor = input("Odabir: ")

        if izbor == "1":
            dodaj_gym()
        elif izbor == "2":
            dodaj_korisnika()
        elif izbor == "3":
            dodaj_admina()
        elif izbor == "4":
            korisnik_orm = izaberi_korisnika()
            gym_orm = izaberi_gym()
            if korisnik_orm and gym_orm:
                Korisnik(korisnik_orm).korisnik_izbornik(Gym(gym_orm))
        elif izbor == "5":
            admin_orm = izaberi_admina()
            gym_orm = izaberi_gym()
            if admin_orm and gym_orm:
                Admin(admin_orm).admin_izbornik(Gym(gym_orm))
        elif izbor == "0":
            print("Izlazak...")
            break
        else:
            print("Pogrešan unos. Pokušajte ponovno.")

if __name__ == "__main__":
    main()
