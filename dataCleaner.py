import re
import json

def readFile():   
    data = parse_json_file('all_companies.json')
    return data

def writeOutsourcingCompanies():
    f = open('outsourcing_companies.txt', 'r+')
    target = open('outsourcing_companies_edited.txt', 'w')
    for line in f:
        json_line = '{"Global Vendor Name":"' +line.rstrip()+'"},'
        target.write(json_line)
        print json_line
    f.close()
    target.close()

def cleanCompanies(data):
    #Undesired string array
    arr = ['inc.','inc','corporation', 'company', 'corp', 'corp.', 'co.', 'international', 'l.l.c.', 'llc', 'limited', 'llp', 'lp', 'l.p.', 'lls', 'l.l.s.', 'plc', 'holdings', 'holding', 'group']
    for line in data:
        for string in arr:
            line["Global Vendor Name"] = re.sub(r'\s'+string+'\s', '', line["Global Vendor Name"], flags=re.IGNORECASE)
            #'$' marks the end of a string
            line["Global Vendor Name"] = re.sub(r'\s'+string+'$', '', line["Global Vendor Name"], flags=re.IGNORECASE)
        line["Global Vendor Name"] = re.sub(r'the\s', '', line["Global Vendor Name"], flags=re.IGNORECASE)
        line["Global Vendor Name"] = line["Global Vendor Name"].replace(',','')
        line["Global Vendor Name"] = line["Global Vendor Name"].replace("'", "")
        line["Global Vendor Name"] = line["Global Vendor Name"].lower() #lower case for easier parsing
        #encode as ascii to avoid character parsing issues
        line["Global Vendor Name"] = line["Global Vendor Name"].encode('ascii', 'ignore')
        #throw company name into file
        outfile = 'results/companies.txt'
        with open(outfile, 'a') as f:
            f.write(line["Global Vendor Name"] + "\n")       

#returns a json object
def parse_json_file(filename):
    with open(filename, 'r') as d:
        data = json.loads(d.read())
    return data

if __name__ == '__main__':
    data = readFile()
    cleanCompanies(data)
    #writeOutsourcingCompanies()