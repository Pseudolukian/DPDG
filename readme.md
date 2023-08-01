# About FPDG
FPDG is Fake Persone Data Generator. This is a comprehensive package designed to generate realistic, yet fake data. Its primary objective is to facilitate hands-on exercises with databases and enable users to hone their skills in data handling and manipulation. Whether you're learning database management, testing a new database design, or simply need a vast amount of structured data for a project, FPDG has got you covered.

# Features

## Logically Connected Data Generation
Unlike many other fake data generators, FPDG emphasizes the generation of data that's logically coherent. It understands the intricate relations between various data points and ensures they make sense in real-world scenarios. For instance:

- **Driving License Expiration**: The expiration date of a driving license is calculated based on the issuance date, ensuring a realistic time frame.
- **Email Generation**: Rather than generating random strings, the email is generated based on a nickname. This nickname, in turn, correlates with factors like gender and country. Thus, if a user's name is "John" from the USA, the email might resemble "john.usa@example.com".

## Granular Control over Data Streams
FPDG provides an unprecedented level of control over data generation streams, allowing for custom-tailored datasets based on your specific needs:

- **Restrict and Mutate Data Streams**: Depending on where you wish to save your data (be it files or SQL databases), FPDG allows you to fix certain parameters. For instance, you can set a specific country or gender for data intended for file storage while letting these parameters vary for SQL database storage.
- **Adaptive Generation**: With the ability to mutate and adapt data streams on-the-fly, FPDG can cater to a myriad of use-cases, be it for testing, development, or analytical purposes.

Such features ensure that FPDG is not just a data generator but a comprehensive tool that caters to the nuanced needs of its users.

# Generated Data Formats
With versatility in mind, FPDG supports a wide array of output formats to ensure compatibility with various platforms and systems:

- **JSON**: A widely recognized data interchange format that is both human-readable and easy to parse programmatically.
- **CSV**: Comma-separated values, suitable for spreadsheet applications and simple data analyses.
- **XLS**: Excel spreadsheet format, ideal for more complex data representation and analysis.
- **SQL**: Directly save the generated data to SQL databases, ensuring seamless integration and usage in database management systems.

# Example & Walkthrough
In this section, we provide a practical example of how to use the FPDG (Fake Persone Data Generator) along with the associated exporters for file and SQL storage. This example showcases the power and simplicity of FPDG in generating complex, logically related datasets and how easily this data can be stored in various formats.

```
# Import necessary modules and classes
from fakegenerator import FakeGenerator
from file_exporter import File_Exporter
from sql_exporter import SQL_exporter

# Initialize exporters: one for file storage and another for SQL storage
f_exp = File_Exporter()
sql_exp = SQL_exporter(sql_engine="postgresql", user="exporter", 
                       password="exporter", db_name="pers_data_test")

# Loop to generate data (set to run once in this example)
for _ in range(1):
    # Create an instance of FakeGenerator
    f_g = FakeGenerator()
    
    # Generate various data using FakeGenerator's methods
    pers = f_g.generator.personal()
    pas = f_g.generator.passport()
    cont = f_g.generator.contacts()
    exp = f_g.generator.experience()
    dip = f_g.generator.diploma()
    ad = f_g.generator.address()
    bio = f_g.generator.biometric()
    dr_l = f_g.generator.driver_license()
    
    # Add generated data to SQL exporter's buffer
    sql_exp.buffer.add(pers, pas, ad, cont, exp, dip, bio, dr_l)
    
    # Add selected data (personal and passport info) to file exporter's buffer
    f_exp.buffer.add(pers, pas)

# Dump the data from SQL exporter's buffer to the PostgreSQL database
sql_exp.dump_data(sql_buffer=sql_exp.buffer.buf)
```

# Dependencies
FPDG utilizes several state-of-the-art libraries to provide a robust and efficient data generation experience. Here's a list of these dependencies and a brief overview of their roles:

- **Pydantic**: Leveraged for data validation and serialization, ensuring the generated data adheres to predefined standards.
- **SQLModel**: A bridge between Pydantic and SQLAlchemy, it allows for ORM-based interactions and data modeling.
- **SQLAlchemy**: A SQL toolkit and Object-Relational Mapping (ORM) library, facilitates interactions with SQL databases.
- **pathlib**: Provides an Object-Oriented interface to the file system, simplifying file and path operations.
- **Pandas**: An indispensable library for data analysis, it offers data structures and operations essential for cleaning, aggregating, and processing structured data.
- **numpy**: Underpins Pandas and many other libraries, offering support for large, multi-dimensional arrays and matrices, along with a vast collection of mathematical functions to operate on these arrays.
- **psycopg2-binary**: A PostgreSQL adapter for Python, it ensures smooth interactions with PostgreSQL databases.
- **email-validator**: As the name suggests, it's used for robust email address validation.
- **openpyxl**: Enables Python to read/write Excel files, essential for the XLS data output format.

Remember, it's crucial to ensure you have these dependencies installed when using FPDG to avoid any hiccups in functionality.
