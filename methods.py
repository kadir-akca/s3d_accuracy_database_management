# Basic methods

# Libraries
import logging
import os
import platform
import time
import xml.dom.minidom
from datetime import datetime
from tkinter import messagebox

import database
import main


# Quit the application.
def quit_app():
    logging.info('Application has been closed.')
    msgbox = messagebox.askquestion('Database Management', 'Are you sure you want to exit the application?', icon='warning')
    if msgbox == 'yes':
        quit()


# Generate a new XML file from the entries.
def generate_xml(exp):
    file = xml.dom.minidom.parse('write_xml/data.xml')
    x1 = file.getElementsByTagName('AutoTextCustomFieldValue')
    data = database.get_attributes_from_experience_id(exp)

    x1[2].childNodes[0].nodeValue = data[1] # experience id - dev sn
    x1[1].childNodes[0].nodeValue = data[3] # serial number-op
    x1[0].childNodes[0].nodeValue = data[2] # dep
    x1[3].childNodes[0].nodeValue = data[4] # operator-exptype
    x1[4].childNodes[0].nodeValue = data[5] # experience type-arttype

    with open("write_xml/" + exp + '.xml',
              "w") as xml_template:
        file.writexml(xml_template)

    messagebox.showinfo(main.application_title, 'The XML file has been generated.\n\n%s.xml' % exp)