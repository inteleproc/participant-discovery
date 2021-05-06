# participant-discovery

This python script implements the dynamic discovery process of BDXL to find a SMP ServiceGroup of a participant, registered in a specific BDXL Domain

# Pre-requisites
The script is written in python 3 and requires the dnspython and requests module, available through Pypi. You can install these modules by using pip as follows:

    pip install -f requirements.txt

# Execution - Getting Results

The script expects the following arguments:

    ./participant-discovery.py <participants-file> <domain (optional)>
    
Where:
* **Participants-file:**  A text file that contains a participant identifier in every line
* **Domain:** The domain of the BDXL to make the NAPTR query. The default is the acceptance environment of the European Commission


