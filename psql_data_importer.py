from session import get_db
from data_structures.sql_models.base_sql_model import *
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, update, insert, join
from fakegenerator import FakeGenerator # Main generator class.
import asyncio

async def  psql_import_data(session: AsyncSession, pers: FakeGenerator, pas:FakeGenerator, 
                     dr_l:FakeGenerator, ad:FakeGenerator,
                     cont:FakeGenerator, dip:FakeGenerator,
                     exp:FakeGenerator, bio:FakeGenerator):
    persone_data = persone(**pers.__dict__)
    
    passport_data = passport(**pas.__dict__)
    passport_data.to_personal_id = persone_data.personal_id
    
    driverlicense_data = driverlicense(**dr_l.__dict__)
    driverlicense_data.to_personal_id = persone_data.personal_id
    
    address_data = address(**ad.__dict__)
    address_data.to_personal_id = persone_data.personal_id
    
    contacts_data = contacts(**cont.__dict__)
    contacts_data.to_personal_id = persone_data.personal_id

    diploma_data = diploma(**dip.__dict__)
    diploma_data.to_personal_id = persone_data.personal_id

    expirience_data = expirience(**exp.__dict__)
    expirience_data.to_personal_id = persone_data.personal_id

    biometric_data = biometric(**bio.__dict__)
    biometric_data.to_personal_id = persone_data.personal_id

    
    session.add_all([
        persone_data,
        passport_data,
        driverlicense_data,
        address_data,
        contacts_data,
        diploma_data,
        expirience_data,
        biometric_data
    ])
            
                       
async def main():
    async with get_db() as session:
        for _ in range(1000):
            f_g = FakeGenerator() # Parameters like age, sex, and country can be customized here.
            pers = f_g.generator.personal()
            pas = f_g.generator.passport()
            cont = f_g.generator.contacts()
            exp = f_g.generator.experience()
            dip = f_g.generator.diploma()
            ad = f_g.generator.address()
            bio = f_g.generator.biometric()
            dr_l = f_g.generator.driver_license()

            await psql_import_data(session, pers, pas, dr_l, ad, cont, dip, exp, bio)
        await session.commit()

asyncio.run(main())            
    
    

