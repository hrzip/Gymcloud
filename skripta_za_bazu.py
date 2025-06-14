import sqlalchemy as db
from sqlalchemy.orm import declarative_base, relationship, backref, sessionmaker, mapper, Session
from sqlalchemy import Column, Integer, String, ForeignKey, Float, create_engine, MetaData, PrimaryKeyConstraint

Base = declarative_base()

class Osoba(Base):
    __tablename__ = "Osoba"
    id = Column(Integer, primary_key = True, autoincrement = True)
    ime = Column(String, nullable = False) # da bude obavezan upis sam stavio nullable = False
    prezime = Column(String, nullable = False)
    telefon = Column(String, nullable = False)
    email= Column(String, nullable = False)

    korisnik = relationship("Korisnik", uselist=False, back_populates="osoba")
    admin    = relationship("Admin",    uselist=False, back_populates="osoba")



class VjezbaProgram(Base):
    __tablename__ = "VjezbaProgram"
    id = Column(Integer, primary_key = True, autoincrement = True)
    naziv = Column(String, nullable = False)

    korisnici = relationship(
        "Korisnik",
        secondary="ListaKorisnikovihPrograma",
        back_populates="programi"
    )
    gyms = relationship("Gym", secondary="ListaGymVjezbi", back_populates="vjezbe")
    sprave = relationship(       "Sprave",secondary="VjezbaProgramSprave",  back_populates="programi"    )

class Sprave(Base):
    __tablename__ = "Sprave"
    id = Column(Integer, primary_key = True, autoincrement = True)
    naziv = Column(String, nullable = False)
    lokacija = Column(String, nullable = False)
    programi  = relationship(      "VjezbaProgram", secondary="VjezbaProgramSprave",     back_populates="sprave"       )
    gyms = relationship("Gym", secondary="ListaGymSprava", back_populates="sprave")




class Gym(Base):
    __tablename__ = "Gym"
    id = Column(Integer, primary_key = True, autoincrement = True)
    naziv = Column(String, nullable = False)
    vjezbe = relationship("VjezbaProgram", secondary="ListaGymVjezbi", back_populates="gyms")

    sprave      = relationship(
                     "Sprave",
                     secondary="ListaGymSprava",
                     back_populates="gyms"
                  )
    izvjestaji  = relationship(
                     "Izvjestaj",
                     secondary="ListaGymIzvjestaj",
                     back_populates="gyms"
                  )



class Admin(Base):
    __tablename__ = "Admin"
    id = Column(Integer, primary_key = True, autoincrement = True)
    osoba_id = Column(Integer, ForeignKey("Osoba.id") ) # iz tablice pod nazivom Osoba vuče ID vrijednost
    osoba     = relationship("Osoba", back_populates="admin")



class Korisnik(Base):
    __tablename__ = "Korisnik"
    id = Column(Integer, primary_key = True, autoincrement = True)
    osoba_id = Column(Integer, ForeignKey("Osoba.id"))
    tezina = Column(Float, nullable = False)
    visina = Column(Float, nullable = False)
    dob = Column(Integer, nullable = False)
    spol = Column(String, nullable = False)
    osoba = relationship("Osoba", back_populates="korisnik", uselist=False)
    programi  = relationship(
                   "VjezbaProgram",
                   secondary="ListaKorisnikovihPrograma",
                   back_populates="korisnici"
                )


class Izvjestaj(Base):
    __tablename__= "Izvjestaj"
    id = Column(Integer, primary_key = True, autoincrement = True)
    id_vjezbe = Column(Integer, ForeignKey("VjezbaProgram.id"))
    osoba_id = Column(Integer, ForeignKey("Osoba.id"))
    ime = Column(String, nullable = False) # da bude obavezan upis sam stavio nullable = False
    prezime = Column(String, nullable = False)
    telefon = Column(String, nullable = False)
    email= Column(String, nullable = False)
    tezina = Column(Float, nullable = False)
    visina = Column(Float, nullable = False)
    dob = Column(Integer, nullable = False)
    spol = Column(String, nullable = False)

    vjezba     = relationship("VjezbaProgram")
    osoba      = relationship("Osoba")
    gyms      = relationship(
                  "Gym",
                  secondary="ListaGymIzvjestaj",
                  back_populates="izvjestaji"
               )



class ListaKorisnikovihPrograma(Base):
    __tablename__ = "ListaKorisnikovihPrograma"
    korisnik_id = Column(Integer, ForeignKey("Korisnik.id"))
    id_programa = Column(Integer, ForeignKey("VjezbaProgram.id"))
    PrimaryKeyConstraint(korisnik_id, id_programa) # id dobivamo iz spoja korisnik id i id programa i onda znamo da je taj id costraint unikatan baš za ListaKorisnikovihPrograma

class VjezbaProgramSprave(Base):
    __tablename__ = "VjezbaProgramSprave"
    id_sprave = Column(Integer, ForeignKey("Sprave.id"))
    id_vjezbe = Column(Integer, ForeignKey("VjezbaProgram.id"))
    trajanje = Column(Integer, nullable = False)
    PrimaryKeyConstraint(id_sprave, id_vjezbe)


class ListaGymVjezbi(Base):
    __tablename__ = "ListaGymVjezbi"
    id_gym = Column(Integer, ForeignKey("Gym.id"))
    id_vjezbe = Column(Integer, ForeignKey("VjezbaProgram.id"))
    PrimaryKeyConstraint(id_gym, id_vjezbe)


class ListaGymSprava(Base):
    __tablename__ = "ListaGymSprava"
    id_gym = Column(Integer, ForeignKey("Gym.id"))
    id_sprave = Column(Integer, ForeignKey("Sprave.id"))
    PrimaryKeyConstraint(id_gym, id_sprave)


class ListaGymIzvjestaj(Base):
    __tablename__ = "ListaGymIzvjestaj"
    id_gym = Column(Integer, ForeignKey("Gym.id"))
    id_izvjestaj = Column(Integer, ForeignKey("Izvjestaj.id"))
    PrimaryKeyConstraint(id_gym, id_izvjestaj)


