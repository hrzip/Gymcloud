from db_setup import SessionLocal
from skripta_za_bazu import Gym as GymORM, Sprave as SpravaORM, VjezbaProgram as VjezbaProgramORM, Izvjestaj as IzvjestajORM, ListaGymIzvjestaj, ListaGymSprava, ListaGymVjezbi, VjezbaProgramSprave
from izvjestaj import IzvjestajWrapper

session = SessionLocal()

class Gym:
    def __init__(self, orm_gym):
        self.orm = orm_gym

    def prikazi_naziv(self):
        print(self.orm.naziv)

    def prikazi_izvjestaje_odabranog_korisnika(self, osoba_id):
        rezultati = session.query(IzvjestajORM).filter_by(osoba_id=osoba_id).all()
        return [IzvjestajWrapper(i) for i in rezultati]

    def prikazi_sve_korisnike(self):
        rezultati = session.query(IzvjestajORM).all()
        skup = set()
        for izv in rezultati:
            o = izv.osoba
            skup.add((o.ime, o.prezime, o.id))
        return skup

    def dodaj_izvjestaj_nakon_vjezbe(self, vjezba_programa, korisnik):
        iz = IzvjestajORM(
            id_vjezbe = vjezba_programa.id,
            osoba_id=korisnik.osoba.id,
            ime=korisnik.osoba.ime,
            prezime=korisnik.osoba.prezime,
            telefon=korisnik.osoba.telefon,
            email=korisnik.osoba.email,
            tezina=korisnik.orm.tezina,
            visina=korisnik.orm.visina,
            dob=korisnik.orm.dob,
            spol=korisnik.orm.spol,
        )
        session.add(iz)
        session.commit()

        veza = ListaGymIzvjestaj(id_gym=self.orm.id, id_izvjestaj=iz.id)
        session.add(veza)
        session.commit()

    def prikazi_sprave(self):
        for sprava in self.orm.sprave:
            print(sprava.naziv)

    def prikazi_vjezbe(self):
        session.expire_all()
        vjezbe = session.query(VjezbaProgramORM).all()

        for vjezba in vjezbe:
            print(vjezba.naziv)
            for spr in vjezba.sprave:
                veza = (
                    session.query(VjezbaProgramSprave)
                           .filter_by(id_vjezbe=vjezba.id, id_sprave=spr.id)
                           .one_or_none()
                )
                trajanje = veza.trajanje if veza else 0
                print(f"  Sprava: {spr.naziv} – trajanje: {trajanje} min")

    def dodaj_spravu(self, naziv, lokacija):
        nova = SpravaORM(naziv=naziv, lokacija=lokacija)
        session.add(nova)
        session.commit()
        veza = ListaGymSprava(id_gym=self.orm.id, id_sprave=nova.id)
        session.add(veza)
        session.commit()

    def dodaj_vjezbu(self, naziv):
        nova = VjezbaProgramORM(naziv=naziv)
        session.add(nova)
        session.commit()
        veza = ListaGymVjezbi(id_gym=self.orm.id, id_vjezbe=nova.id)
        session.add(veza)
        session.commit()

    def get_sprava_by_naziv(self, naziv):
        return next((s for s in self.orm.sprave if s.naziv.lower() == naziv.lower()), None)

    def ukloni_spravu(self, naziv_sprave):
        sprava = self.get_sprava_by_naziv(naziv_sprave)
        if sprava:
            veza = session.query(ListaGymSprava).filter_by(id_gym=self.orm.id, id_sprave=sprava.id).first()
            if veza:
                session.delete(veza)
            session.commit()

    def promijeni_lokaciju_sprave(self, naziv_sprave, nova_lokacija):
        sprava = self.get_sprava_by_naziv(naziv_sprave)
        if sprava:
            sprava.lokacija = nova_lokacija
            session.commit()

    def dodaj_spravu_u_vjezbu(self, naziv_programa, naziv_sprave, trajanje):
        vp = session.query(VjezbaProgramORM).filter(VjezbaProgramORM.naziv.ilike(naziv_programa)).first()
        spr = session.query(SpravaORM).filter(SpravaORM.naziv.ilike(naziv_sprave)).first()

        if not vp or not spr:
            print("Program ili sprava ne postoji.")
            return

        veza = VjezbaProgramSprave(id_sprave=spr.id, id_vjezbe=vp.id, trajanje=trajanje)
        session.add(veza)
        session.commit()

    def ukloni_spravu_iz_vjezbe(self, naziv_programa, naziv_sprave):
        vp = session.query(VjezbaProgramORM).filter(VjezbaProgramORM.naziv.ilike(naziv_programa)).first()
        spr = session.query(SpravaORM).filter(SpravaORM.naziv.ilike(naziv_sprave)).first()

        if not vp or not spr:
            print("Program ili sprava ne postoji.")
            return

        veza = session.query(VjezbaProgramSprave).filter_by(id_sprave=spr.id, id_vjezbe=vp.id).first()
        if veza:
            session.delete(veza)
            session.commit()
