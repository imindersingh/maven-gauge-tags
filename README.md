# Unused Tags

This script finds all unused tags in the specs that are not in the pom.xml

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
