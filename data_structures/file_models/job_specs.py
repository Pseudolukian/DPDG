from pydantic import BaseModel

class job_specs(BaseModel):
    """
    Represents specific job details, dynamically populated using predefined data from a configuration file.
    
    The class is mainly utilized by the `rand_spec_pos_resp` function, which randomly selects attributes from 
    a predefined dataset to generate a job profile. This includes its specialty, position, and associated responsibilities.

    Attributes:
        - specialty (str): The specific domain or field of the job, randomly selected from the dataset.
        - position (str): Designation or job title corresponding to the chosen specialty.
        - responsibilities (str): List of job responsibilities tied to the position, limited to a subset from the dataset.
    
    Typical usage is via the `rand_spec_pos_resp` function, which returns an instance of this class with attributes populated.

    Example usage in rand_spec_pos_resp:
        >>> def rand_spec_pos_resp(self)
        >>> specs_out = job_specs()
        >>> specs_out.specialty = rand_spec
        >>> specs_out.position = rand_job_pos
        >>> specs_out.responsibilities = rand_resp 
        >>> return specs_out
    Note:
        - While the attributes can be manually set, they are primarily intended to be populated by the aforementioned function.
    """
    specialty:str = None
    position:str = None
    responsibilities:str = None