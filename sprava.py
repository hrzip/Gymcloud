class Sprava:
    def __init__(self, orm_sprava):
        self.orm = orm_sprava

    def promijeni_lokaciju(self, nova_lokacija):
        self.orm.lokacija = nova_lokacija
