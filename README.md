# Unused Tags

This script will:

- Find all unused tags in the specs that are not in the pom.xml
- Find all specs which don't have any tags (meaning they are probably not being run anywhere!)

## Requirements 

- Python3
- Pip

## Usage

Run the following command in the terminal to install the script dependencies:

``sudo pip install -r requirements.txt``

Run the script as follows:

``python find_unused_tags.py <PATH TO POM> <SPECS DIR>``

For example:

``python find_unused_tags.py ~/projects/maven-gauge-project/pom.xml ~/projects/maven-gauge-project/specs``
