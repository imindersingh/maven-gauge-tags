#!/usr/bin/env python

import xmltodict
import re
import glob
from tabulate import tabulate
import sys

SPEC_FILE = '.spec'
POM_FILE = str(sys.argv[1])
SPECS_DIR = str(sys.argv[2])

def load_file(file):
    try:
        if file is POM_FILE:
            with open(file) as f:
                contents = f.read()
            return xmltodict.parse(contents)
        elif file.find(SPEC_FILE):
            with open(file) as f:
                contents = f.read().splitlines()
            return (contents)    
    except:
        print ("Something went in load_file",sys.exc_info())
        sys.exit()
      
def get_artifact_id(xml_doc):
    try:
        return xml_doc['project']['artifactId']
    except:
        print ("Something went in get_artifact_id", sys.exc_info())
        sys.exit()
        
def get_all_tags_from_pom(file_path):
    xml_doc = load_file(file_path)
    list_of_tags = []
    try:    
        doc_properties = xml_doc['project']['profiles']['profile']
        list_of_properties = [properties['properties']
                        for properties in doc_properties]
        list_of_tags.extend([tag['tags']
                        for tag in list_of_properties])
        
        return list(list_of_tags)         
    except:
        print ("Something went wrong in get_all_tags_from_pom. ", sys.exc_info())
        sys.exit()

def filter_pom_tags(list_of_tags):
    flat_list_of_tags = []
    try:
        for sublist in list_of_tags:
            tag_list = re.findall(r'[\w\-]+(?<!\\n)', sublist)
            for tag in tag_list:
                flat_list_of_tags.append(tag.lower())      
        return list(flat_list_of_tags)
    except:
        print ("Something went wrong in filter_pom_tags", sys.exc_info())
        sys.exit()      
  
def get_unique_tags(tags_list):
    try:
        unique_list = list(set(tags_list))
        return (unique_list)       
    except:
        print ("Something went wrong in get_unique_tags", sys.exc_info())
        sys.exit()      

def get_list_of_specs(dir_name):
    try:
        return list(glob.glob(dir_name + '/**/*.[sS][pP][eE][cC]', recursive=True)) 
    except:
        print("Something went wrong in get_list_of_specs", sys.exc_info())
        sys.exit()
             
def get_spec_tags(spec):
    spec_tags = []
    list_of_specs_with_no_tags = []
    try:
        for line in spec:
            tags = "tags:"
            if tags in line.casefold():
                spec_tags = re.findall(r'(?!tags:)\b[\w\-]+', line.lower())                               
        
        unique_tags = get_unique_tags(spec_tags)       
        return (unique_tags)
    except:
        print ("Something went wrong in get_spec_tags", sys.exc_info())
        sys.exit()        

def get_specs_with_no_tags(list_of_specs):
    list_of_specs_with_no_tags = []
    try:
        for spec in list_of_specs:
            contents = load_file(spec)
            if not re.findall(r'(?i)(tags:)', ''.join(contents)):
                list_of_specs_with_no_tags.append(spec)
            
        if list_of_specs_with_no_tags:
            print (tabulate([spec.split(',') for spec in list_of_specs_with_no_tags], headers=['SPECS WITH NO TAGS'], tablefmt="fancy_grid"))
        else:
            print ("Specs with no tag were not found")
    except:
        print ("Something went wrong in get_specs_with_no_tags", sys.exc_info())
        sys.exit()       
        
def get_spec_tags_not_in_pom(pom_tags, list_of_specs):
    table = []
    for spec in list_of_specs:
        contents = load_file(spec)
        spec_tags = get_spec_tags(contents)
        list_of_tags_not_in_pom = []
        for tag in spec_tags:
            if tag not in pom_tags:
                list_of_tags_not_in_pom.append(tag)
        if list_of_tags_not_in_pom:
            table.append([spec, ', '.join(list_of_tags_not_in_pom)])  
    if table:
        print (tabulate(table, headers=['SPEC','SPEC TAGS NOT IN POM.XML'], tablefmt="fancy_grid"))
    else:
        print ("There aren't any specs which contain tags different to the pom.xml tags. Let's keep it this way!")

def main():
    pom_tags = get_all_tags_from_pom(POM_FILE)
    clean_pom_tags = filter_pom_tags(pom_tags)
    unique_pom_tags = get_unique_tags(clean_pom_tags)
    list_of_specs = get_list_of_specs(SPECS_DIR)
    get_spec_tags_not_in_pom(unique_pom_tags, list_of_specs)
    get_specs_with_no_tags(list_of_specs)

if __name__ == "__main__":
    main()
