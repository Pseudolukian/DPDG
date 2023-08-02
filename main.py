from fakegenerator import FakeGenerator
from file_exporter import File_Exporter
from sql_exporter import SQL_exporter
from random import randint
from pathlib import Path
from web_exporter import Web_exporter


f_exp = File_Exporter()
sql_exp = SQL_exporter(sql_engine="sqlite", user="exporter", 
                       password="exporter", db_name="pers_data_test")
web_exp = Web_exporter()

for _ in range(2):
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
    sql_exp.buffer.add(pers, pas, ad, cont, exp, dip, bio, dr_l)   
    
sql_exp.dump_data(sql_buffer=sql_exp.buffer.buf)    
    

