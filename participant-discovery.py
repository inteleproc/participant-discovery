#!/usr/bin/env python3
from hashlib import sha256
from base64 import b32encode 
from dns import resolver
import requests
import xml.dom.minidom
import sys

def create_bdxl_hash(participant):
    """
    Create the BDXL Hash for the participant, part of the DNS Name
    """

    # generate SHA256 Hash of the participant Identifier
    hashed_identifier = sha256(participant.encode("utf-8"))

    # get BASE32 of the hashed Identifier digest
    b32_hashed_identifier = b32encode(hashed_identifier.digest())

    # remove the trailing '=' characters 
    stripped_b32_hashed_identifier = b32_hashed_identifier.decode('utf8').replace("=","").strip()

    #return the BDXL Hash of participant Id
    return stripped_b32_hashed_identifier


def get_servicegroup(participant, domain):

    # get the bdxl hash of the participant
    hash = create_bdxl_hash(participant)
    print("Participant Hash: "+hash)

    # create the domain name
    domain = hash + ".iso6523-actorid-upis."+domain+"."
    print("BDXL Domain: "+domain)
    # get the NAPTR Record
    natpr_record = resolver.resolve(domain, 'NAPTR')
    # Check that we have a naptr record in the results
    if len(natpr_record) > 0:
        # getting the first record - for bdxl is typically only one record in response
        # Check that the service is Meta:SMP 
        if natpr_record[0].service.decode("utf-8") == "Meta:SMP":
            #in BDXL, the second part of the regexp (Replacement String) is the SMP URL
            smp_url = natpr_record[0].regexp.decode("utf-8").split("!")[2]

            #query the smp 
            result =  requests.get(smp_url+"/iso6523-actorid-upis::"+participant)
            print("SMP URL: "+result.url)

            if result.status_code == 200:
                return xml.dom.minidom.parseString(result.text).toprettyxml()
            raise Exception("Participant Record not found - SMP returned bad status code "+result.url)
        
        raise Exception("Participant Record not found - No Meta:SMP - "+ natpr_record[0].regexp.decode("utf-8"))
    
    raise Exception("Participant Record not found - No Naptr Record for "+ domain)

# Command line execution - Read the file (first argument) and check against domain (second argument)
if __name__ == '__main__':
    
    domain = "acc.edelivery.tech.ec.europa.eu"
    if len(sys.argv) < 4 and len(sys.argv) > 1:
        print("reading participants from "+sys.argv[1])

        if (len(sys.argv) == 3):
            print("domain: "+sys.argv[2])
            domain = sys.argv[2]
        
        participant_file = open(sys.argv[1], 'r')
        for line in participant_file:
            print("----------------")
            print(line)
            try:
                sg = get_servicegroup(line.strip(),domain) 
                print("Service Group:")
                print(sg)
            except Exception as e:
                print(e)

    else:
        print("Usage: "+sys.argv[0]+" <file with participants> <domain (optional)>")

