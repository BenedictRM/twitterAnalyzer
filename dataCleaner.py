import re
import json

def readFile():   
    data = parse_json_file('top_100_contractors.json')
    return data

def cleanCompanies(data):
    outfile = 'results/companies.txt'
    for line in data:
        #lower case
        d = line["Global Vendor Name"].lower()
        #replace undesired strings and punctuation
        d = d.replace('corporation','')
        d = d.replace('holdings','')
        d = d.replace('international','')
        d = d.replace('company','')
        d = d.replace('limited','') 
        with open(outfile, 'a') as f:
            f.write(d + "\n")       
        print(d)
#returns a json object
def parse_json_file(filename):
    with open(filename, 'r') as d:
        data = json.loads(d.read())
    return data

if __name__ == '__main__':
    data = readFile()
    cleanCompanies(data)