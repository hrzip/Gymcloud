class VjezbaProgram:
    def __init__(self, orm_vjezba):
        self.orm = orm_vjezba

    def get_index_sprave(self, naziv_sprave):
        for i, veza in enumerate(self.orm.sprave_vezani):
            if naziv_sprave.lower() == veza.sprava.naziv.lower():
                return i
        return -1

    def promjena_vjezbe(self, naziv_sprave, nova_sprava_orm, trajanje):
        index = self.get_index_sprave(naziv_sprave)
        if index >= 0:
            self.orm.sprave_vezani[index].sprava = nova_sprava_orm
            self.orm.sprave_vezani[index].trajanje = trajanje

    def ukloni_spravu(self, naziv_sprave):
        index = self.get_index_sprave(naziv_sprave)
        if index >= 0:
            veza = self.orm.sprave_vezani[index]
            self.orm.sprave_vezani.remove(veza)

    def dodaj_spravu(self, sprava_orm, trajanje):
        if self.get_index_sprave(sprava_orm.naziv) >= 0:
            print("Ta sprava već postoji, odaberite drugu.")
        else:
            from skripta_za_bazu import VjezbaProgramSprave
            nova_veza = VjezbaProgramSprave(sprava=sprava_orm, vjezba=self.orm, trajanje=trajanje)
            self.orm.sprave_vezani.append(nova_veza)
