from fakegenerator import FakeGenerator
from file_exporter import File_Exporter
from pprint import pprint


f_exp = File_Exporter()

for _ in range(1):
    f_g = FakeGenerator()
    pers = f_g.generator.personal()
    pas = f_g.generator.passport()
    cont = f_g.generator.contacts()
    exp = f_g.generator.experience()
    dip = f_g.generator.diploma()
    ad = f_g.generator.address()
    bio = f_g.generator.biometric()
    dr_l = f_g.generator.driver_license()
    
    f_exp.buffer.add(pers, pas, ad, cont, exp, dip, bio, dr_l)

pprint(f_exp.dict())