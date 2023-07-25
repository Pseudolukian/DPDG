from fakegenerator import FakeGenerator
from exporter import Exporter

#=====Generation Fake Data=======================
f_g = FakeGenerator(sex= "F", country="USA", age=[30,70])
gen_pers = f_g.generator.personal()
gen_pas = f_g.generator.passport()
gen_address = f_g.generator.address()
gen_diploma = f_g.generator.diploma()
gen_exp = f_g.generator.experience()
gen_bio = f_g.generator.biometric()
gen_cont = f_g.generator.contacts()
gen_dr_lic = f_g.generator.driver_license()


#==========Export============================
exp = Exporter(gen_pers, gen_pas, gen_address)
print(exp.dict())