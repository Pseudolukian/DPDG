"""
file_models - A collection of Pydantic models to represent various data structures.

This package contains a range of data models designed to handle, validate, and structure
data for different requirements. Built upon the Pydantic library, each model is equipped with 
its own validation, serialization, and documentation logic.

Core Models:
- `persone`: Represents personal data like name, age, sex, and country.
- `passport`: Handles passport-related attributes like date of birth, issuing authority, etc.
- `address`: Captures various address details.
- `biometric`: Contains biometric-related information.
- `contacts`: Manages contact details.
- `diploma`: Represents academic qualifications and related data.
- `driverlicense`: Manages driving license-related details.
- `expirience`: Tracks professional experience and attributes.
- `job_specs`: A model to capture job-specific attributes like specialty, position, responsibilities.

Service Models:
- `OutputModel`: A composite model aggregating multiple other models for ease of data processing.
- `Buffer`: Serves as a data buffer, primarily used for holding and manipulating data.
- `SQL_buffer`: Similar to `Buffer`, but specifically tailored for SQL-based operations.

To ensure the proper functioning of these models, relevant JSON databases are required as they 
act as data sources for various attributes.

Usage:
from file_models import persone, passport, address, ...

Further details, attributes, and methods for each model can be discovered in their respective docstrings.
"""

from .address import address
from .biometric import biometric
from .contacts import contacts
from .diploma import diploma
from .driver_license import driverlicense
from .passport import passport
from .persone import persone
from .expirience import expirience
from .job_specs import job_specs
from .output_main_model import OutputModel
from .buffer import Buffer
from .sql_buffer import SQL_buffer