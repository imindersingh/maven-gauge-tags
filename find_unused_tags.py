#!/usr/bin/env python

import xmltodict
import pprint
import re
import glob
from tabulate import tabulate
import sys

SPEC_FILE = '.spec'
POM_FILE = str(sys.argv[1])
SPECS_DIR = str(sys.argv[2])

def load_file(file):
    if file is POM_FILE:
        with open(file) as f:
            contents = f.read()
        return xmltodict.parse(contents)
    elif file.find(SPEC_FILE):
        with open(file) as f:
            contents = f.read().splitlines()
        return (contents)  
        
def get_all_tags_from_pom(file_path):
    xml_doc = load_file(file_path)
    doc_properties = xml_doc['project']['profiles']['profile']
    list_of_properties = [properties['properties']
                    for properties in doc_properties]
    list_of_tags = [tag['tags']
                    for tag in list_of_properties]
    
    return list(list_of_tags)

def get_tags_from_jenkinsfile(jenkinsfile):
    contents = load_file(jenkinsfile)
    for line in contents:
        pprint.pprint(line)

def filter_pom_tags(list_of_tags):
    flat_list_of_tags = []
    for sublist in list_of_tags:
        tag_list = re.findall(r'[\w\-]+(?<!\\n)', sublist)
        for tag in tag_list:
            flat_list_of_tags.append(tag.lower())
            
    return list(flat_list_of_tags)      
  
def get_unique_tags(tags_list):
    unique_list = list(set(tags_list))
    return list(unique_list)

def get_list_of_specs(dir_name):
    return list(glob.glob(dir_name + '/**/*.[sS][pP][eE][cC]', recursive=True)) 
    
def get_spec_tags(spec):
    spec_tags = []
    for line in spec:
        tags = "tags:"
        if tags in line.casefold():
            spec_tags = re.findall(r'(?!tags:)\b[\w\-]+', line.lower())                 
                
    unique_tags = get_unique_tags(spec_tags)       
    return list(unique_tags)     

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
    print(tabulate(table, headers=['Spec','Tags not in POM'], tablefmt="fancy_grid"))
    
         
def main():
    pom_tags = get_all_tags_from_pom(POM_FILE)
    clean_pom_tags = filter_pom_tags(pom_tags)
    unique_pom_tags = get_unique_tags(clean_pom_tags)
    list_of_specs = get_list_of_specs(SPECS_DIR)
    get_spec_tags_not_in_pom(unique_pom_tags, list_of_specs)

if __name__ == "__main__":
    main()
