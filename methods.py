# Basic methods

# Libraries
import logging
import os
import platform
import time
import xml.dom.minidom
from datetime import datetime
import database


# Quit the application.
def quit_app():
    logging.info('Application has been closed.')
    quit()


# Generate a new XML file from the entries.
def generate_xml(exp):
    file = xml.dom.minidom.parse('data.xml')
    x1 = file.getElementsByTagName('AutoTextCustomFieldValue')
    print('exp', exp)
    data = database.get_attributes_from_experience_id(exp)
    print('gen_xml', data)
    x1[2].childNodes[0].nodeValue = data[0]
    x1[1].childNodes[0].nodeValue = data[1]
    x1[0].childNodes[0].nodeValue = data[2]
    x1[3].childNodes[0].nodeValue = data[3]
    x1[4].childNodes[0].nodeValue = data[4]

    with open("test_write_xml/" + exp + '.xml',
              "w") as xml_template:
        file.writexml(xml_template)


def creation_date(path_to_file):
    if platform.system() == 'Windows':
        return time.ctime(os.path.getctime(path_to_file))
    else:
        stat = os.stat(path_to_file)
        try:
            x = stat.st_birthtime
            y = datetime.fromtimestamp(x)
            return y
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime
