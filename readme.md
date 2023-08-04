<p align="center">
  <img src="./logo" alt="DPDG">
</p>

# About FPDG
FPDG (Fake Person Data Generator) is a versatile package crafted to generate realistic yet fictitious data. It's the ideal tool for hands-on exercises with databases, enabling users to refine their data manipulation and handling skills. Whether you're a novice learning database management, testing a new database structure, or in need of a substantial amount of structured data for a project, FPDG is up to the task.

# Features

## Logically Connected Data Generation
What sets FPDG apart from many other data generators is its focus on producing logically coherent data. It captures the intricate relationships between various data points to mirror real-world scenarios. For example:

- **Driving License Expiration**: The expiration date of a driving license is deduced from its issuance date, ensuring a logical timeframe.
- **Email Generation**: Instead of random strings, emails are crafted based on nicknames which correlate with attributes like gender and country. E.g., for a user named "John" from the USA, the email might be "john.usa@example.com".

## Granular Control over Data Streams
FPDG offers unparalleled control over data streams, enabling users to create custom datasets:

- **Restrict and Mutate Data Streams**: Tailor data parameters as per the storage medium. For example, define a specific country or gender for data stored in files while allowing variability for SQL storage.
- **Adaptive Generation**: FPDG's capability to modify data streams real-time makes it versatile across various use cases like testing, development, or analytics.

These features position FPDG as more than just a data generator; it's a tailored solution for diverse user requirements.

# Generated Data Formats
FPDG boasts a broad spectrum of output formats, ensuring compatibility across various platforms:

- **JSON**: A universally accepted data format that's both readable by humans and easily parsed.
- **CSV**: Comma-separated values, perfect for spreadsheet tools and rudimentary data studies.
- **XLS**: Excel format, suited for intricate data visualization and analysis.
- **SQL**: Directly save data into SQL databases, facilitating smooth integration with database management systems.
- **PostgreSQL**: Generate and populate tables within the database.

The result? You can generate vast datasets in multiple formats with ease.

# Usage

FPDG offers two modes of operation:
 
- **Manual Terminal Mode**: Grants you control over data model options and storage paths. You can also redirect data as needed. To operate in this mode, execute the `main.py` file in the project root.
- **Web Port Mode**: This mode offers data visualization options and lets you download the generated datasets at your convenience. To initiate this mode, run the `web.py` file in the project root.

# Installation
To get started, clone the project onto your server using the git clone command. Once cloned, install `pipenv` and activate the virtual environment within the project directory. From here, you can work with FPDG in either mode: manual or web.

Alternatively, use Google Colaboratory notebooks. This method is straightforward and user-friendly. The web application starts automatically.
