from fakegenerator import FakeGenerator
from exporter import Exporter
from pprint import pprint


exp = Exporter()

for _ in range(10):
    f_g = FakeGenerator()
    pers = f_g.generator.personal()
    pas = f_g.generator.passport()
    cont = f_g.generator.contacts()
    exp = f_g.generator.experience()
    dip = f_g.generator.diploma()
    ad = f_g.generator.address()
    bio = f_g.generator.biometric()
    
    exp.buffer.add(pers, pas, ad, cont, exp, dip, bio)

pprint(exp.xls())