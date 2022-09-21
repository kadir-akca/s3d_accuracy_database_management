# Basic methods

# Libraries
import logging
from tkinter import messagebox


# Quit the application.
def quit_app():
    logging.info('Application has been closed.')
    msgbox = messagebox.askquestion('Database Management', 'Are you sure you want to exit the application?', icon='warning')
    if msgbox == 'yes':
        quit()
