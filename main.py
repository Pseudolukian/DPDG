#=====Importing generator classes========
from fakegenerator import FakeGenerator # Main generator class.
from file_exporter import File_Exporter # Class for exporting data to various formats. 
from sql_exporter import SQL_exporter # Class for handling SQL dump logic.

f_exp = File_Exporter()

#=========Setting up SQL Exporter=============================#
# sql_engine -- parameter used to specify the SQL format. Current options: sqlite and postgresql.
# user and password -- parameters used exclusively for PostgreSQL connections.
# db_name -- parameter used for both SQLite and PostgreSQL databases. 
sql_exp = SQL_exporter(sql_engine="sqlite", user="exporter", 
                       password="exporter", db_name="pers_data_test")


#========Main data generation loop==========#
for _ in range(1):
    f_g = FakeGenerator() # Parameters like age, sex, and country can be customized here.
    pers = f_g.generator.personal()
    pas = f_g.generator.passport()
    cont = f_g.generator.contacts()
    exp = f_g.generator.experience()
    dip = f_g.generator.diploma()
    ad = f_g.generator.address()
    bio = f_g.generator.biometric()
    dr_l = f_g.generator.driver_license()
    
    f_exp.buffer.add(pers, pas, ad, cont, exp, dip, bio, dr_l) # Add data models to the file buffer.
    sql_exp.buffer.add(pers, pas, ad, cont, exp, dip, bio, dr_l) # Add data models to the SQL buffer.   

#To view the buffered data, you can run: print(f_exp.buffer.buf) or print(sql_exp.buffer.buf)
    
f_exp.json() # Dump data to JSON. The saving path for the JSON can be customized using the path_json= parameter.
sql_exp.dump_data(sql_buffer = sql_exp.buffer.buf) # Create a database and dump data from the SQL buffer.

    

