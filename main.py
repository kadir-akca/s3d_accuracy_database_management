import os.path
import tkinter as tk
import xml.dom.minidom
from datetime import datetime
from tkinter import LEFT, ttk, END
import tkinter.filedialog as fd

import pyperclip

import database
import fonts
import methods
from database import open_db
import logging

g_xml_url = ''
g_experience_id = ''

logging.basicConfig(filename='file.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')


class PageClass(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


class DatabaseManagement(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        logging.debug('Application started.')

        p1 = PageClassOne(self)
        p2 = PageClassTwo(self)

        button_frame = tk.Frame(self)
        container = tk.Frame(self)
        button_frame.pack(side="bottom", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        button_first_page = tk.Button(button_frame, text='First Page', command=p1.show)
        button_second_page = tk.Button(button_frame, text='Second Page', command=lambda: p2.show())

        button_open_db = tk.Button(button_frame, text='Open Database', command=lambda: open_db())
        button_quit_app = tk.Button(button_frame, text='Exit', command=lambda: methods.quit_app())

        button_first_page.pack(side=LEFT)
        button_second_page.pack(side=LEFT)
        # b3.pack(side=LEFT)
        button_open_db.pack(side=LEFT)
        button_quit_app.pack(side=LEFT)
        # b_reset.pack(side=LEFT)
        p1.show()


# Page one
class PageClassOne(PageClass):

    def __init__(self, *args, **kwargs):
        PageClass.__init__(self, *args, **kwargs)

        # Variables
        self.label_confirm = None
        self.entry_person = None
        self.conn = None
        self.x = None
        self.date = None
        self.part_name = None
        self.part_number = None
        self.inspector_name = None
        self.department_name = None
        self.experience_id = None
        self.product_name = None
        self.filename = ''

        # Button, Entries, Labels
        label = tk.Label(self, text='New Test Page', font=fonts.NORMAL_FONT)
        label.grid(row=0, column=0, pady=10, padx=10, sticky="NSEW", columnspan=3)

        self.entry_device_sn = tk.Entry(self)
        self.entry_device_sn.grid(row=1, column=1, columnspan=2, padx=5, pady=5, ipadx=5, ipady=5, sticky="NSEW")

        self.cbb_operator_str = tk.StringVar()
        self.cbb_operator = ttk.Combobox(self, textvariable=self.cbb_operator_str)
        self.cbb_operator.grid(row=2, column=1, padx=5, pady=5, ipadx=5, ipady=5, sticky="NSEW")
        self.cbb_operator['values'] = database.get_operators()
        self.cbb_operator['state'] = 'readonly'

        self.cbb_department_str = tk.StringVar()
        self.cbb_department = ttk.Combobox(self, textvariable=self.cbb_department_str)
        self.cbb_department.grid(row=3, column=1, columnspan=2, padx=5, pady=5, ipadx=5, ipady=5, sticky="NSEW")
        self.cbb_department['values'] = database.get_departments()
        self.cbb_department['state'] = 'readonly'

        self.cbb_experience_type_str = tk.StringVar()
        self.cbb_experience_type = ttk.Combobox(self, textvariable=self.cbb_experience_type_str)
        self.cbb_experience_type.bind('<<ComboboxSelected>>', self.cbb_list_artefactSN)
        self.cbb_experience_type.grid(row=4, column=1, columnspan=2, padx=5, pady=5, ipadx=5, ipady=5, sticky="NSEW")
        self.cbb_experience_type['values'] = database.get_experience_type()
        self.cbb_experience_type['state'] = 'readonly'

        self.cbb_artefact_type_str = tk.StringVar()
        self.cbb_artefact_type = ttk.Combobox(self, textvariable=self.cbb_artefact_type_str)
        self.cbb_artefact_type.bind('<<ComboboxSelected>>', self.cbb_list_certificate_sn)
        self.cbb_artefact_type.grid(row=5, column=1, columnspan=2, padx=5, pady=5, ipadx=5, ipady=5, sticky="NSEW")
        self.cbb_artefact_type['state'] = 'readonly'
        self.cbb_artefact_type.config(state='normal')

        self.cbb_certificate_sn_str = tk.StringVar()
        self.cbb_certificate_sn = ttk.Combobox(self, textvariable=self.cbb_certificate_sn_str)
        self.cbb_certificate_sn.grid(row=6, column=1, padx=5, columnspan=2, pady=5, ipadx=5, ipady=5, sticky="NSEW")
        self.cbb_certificate_sn['state'] = 'readonly'
        self.cbb_certificate_sn.config(state='normal')

        self.text_subject = tk.Text(self, width=20, height=3)
        self.text_subject.grid(row=7, column=1, columnspan=2, padx=5, pady=7, ipadx=5, ipady=5, sticky="NSEW")

        self.entry_experience_id = tk.Entry(self)
        self.entry_experience_id.grid(row=10, column=1, rowspan=2, padx=5, pady=5, ipadx=5, ipady=5, sticky="NSEW")

        label_device_sn = tk.Label(self, text="Device SN:")
        label_device_sn.grid(row=1, column=0)
        label_operator = tk.Label(self, text="Operator")
        label_operator.grid(row=2, column=0)
        label_department = tk.Label(self, text="Department:")
        label_department.grid(row=3, column=0)
        label_experience_type = tk.Label(self, text="Experience Type:")
        label_experience_type.grid(row=4, column=0)
        label_artefact_type = tk.Label(self, text="Artefact SN:")
        label_artefact_type.grid(row=5, column=0)
        label_certificate_sn = tk.Label(self, text="Certificate SN:")
        label_certificate_sn.grid(row=6, column=0)
        label_subject = tk.Label(self, text="Subject:")
        label_subject.grid(row=7, column=0)
        label_experience_id = tk.Label(self, text="Experience ID:")
        label_experience_id.grid(row=10, column=0)

        self.button_fill_xml = tk.Button(self, text='Fill with XML', command=lambda: self.get_data_from_xml())
        self.button_fill_xml.grid(row=8, column=0, padx=5, pady=5, columnspan=3, sticky="NSEW")

        '''self.b_generate_experience_id = tk.Button(self, text='Generate Experience ID',
                                                  command=lambda: self.generate_experience_id())
        self.b_generate_experience_id.grid(row=9, column=2, padx=5, pady=5, sticky="NSEW")'''

        self.button_copy = tk.Button(self, text='Copy', command=lambda: self.copy_experience_id())
        self.button_copy.grid(row=10, column=2, padx=5, pady=5, sticky="NSEW")

        self.button_create_experience = tk.Button(self, text='Generate Experience ID and Create Experience',
                                                  command=lambda: self.generate_experience_id())
        self.button_create_experience.grid(row=9, column=0, columnspan=3, padx=5, pady=5, sticky="NSEW")

        button_add_operator = tk.Button(self, text='Add operator', command=lambda: self.add_operator())
        button_add_operator.grid(row=2, column=2, padx=5, pady=5, sticky="NSEW")

        self.button_reset = tk.Button(self, command=lambda: self.reset_fields(), text='Reset all')
        self.button_reset.grid(row=12, column=0, columnspan=3, padx=5, pady=5, sticky="NSEW")

    # Method: insert entries to database
    def db_insert_experience(self):
        try:
            device_sn = self.entry_device_sn.get()
            operator = self.cbb_operator_str.get()
            department = self.cbb_department_str.get()
            experience_type = self.cbb_experience_type_str.get()
            artefact_type = self.cbb_artefact_type_str.get()
            certificate_sn = self.cbb_certificate_sn_str.get()
            subject = self.text_subject.get('1.0', END)
            experience_id = self.entry_experience_id.get()
            if database.check_experience_id(experience_id) != 'exist':
                database.insert_experience(device_sn, operator, department, experience_type, artefact_type,
                                           certificate_sn, subject, experience_id)
                logging.info('Done! Success to insert experience in database! \n\tFollowing experience ID has been '
                             'added: ' + str(experience_id))
                print('Done! Success to insert experience in database! \n\tFollowing experience ID has been added: ',
                      experience_id)
            else:
                logging.info('Experience already exist')
            self.button_create_experience.config(state='disabled')
        except:
            print('Failed to insert experience in database')
            logging.error('Failed to insert experience in database')

    # New window: to add new operator
    def add_operator(self):
        window_add_user = tk.Toplevel(root)
        window_add_user.title('Add new operator')
        window_add_user.geometry('190x200')
        label_person = tk.Label(window_add_user, text='Person')
        label_person.grid(row=0, column=0, padx=5, pady=5, sticky="NSEW")
        self.entry_person = tk.Entry(window_add_user)
        self.entry_person.grid(row=0, column=1, sticky="NSEW")
        button_confirm = tk.Button(window_add_user, text='Confirm', command=lambda: self.add_operator_confirm())
        button_confirm.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="NSEW")
        self.label_confirm = tk.Label(window_add_user)
        self.label_confirm.grid(row=1, column=3, sticky="NSEW")
        button_close = tk.Button(window_add_user, text='Close',
                                 command=lambda: window_add_user.destroy() and self.add_operator_confirm())
        button_close.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="NSEW")

    # check if entered operator exists
    def add_operator_check(self, s):
        x = database.check_operator_number()
        if s == x or self.entry_person.get() == '':
            self.label_confirm['text'] = 'Nothing Added!'
            return True
        elif x == s + 1:
            self.label_confirm['text'] = 'Added Successfully!'
            x += 1
            return False

    # confirm new operator
    def add_operator_confirm(self):
        x = database.check_operator_number()
        a = self.entry_person.get()
        d = datetime.now().strftime('%d-%m-%y %H:%M')
        database.insert_operator(a, d)
        self.add_operator_check(x)
        self.cbb_operator.config(values=database.get_operators())

    # Dynamic refresh in list of artefactsn
    def cbb_list_artefactSN(self, *args):
        self.cbb_artefact_type.config(values=[])
        m = self.cbb_experience_type_str.get()
        n = database.get_artefact_sn(m)
        self.cbb_artefact_type.config(state='normal')
        self.cbb_artefact_type.config(values=n)

    # Dynamic refresh in list of artefactsn
    def cbb_list_certificate_sn(self, *args):
        self.cbb_certificate_sn.config(values=[])
        m = self.cbb_artefact_type_str.get()
        n = database.get_cert_sn(m)
        self.cbb_certificate_sn.config(state='normal')
        self.cbb_certificate_sn.config(values=n)

    # Generate an experience id based on device SN and date
    def generate_experience_id(self):
        dev = str(self.entry_device_sn.get())
        if dev == '':
            print('Device SN not defined')
            logging.error('Generate experience id failed, device sn not specified.')
            print('Failed, experience ID has not been generated!')
        elif dev[:8] == 'FreeScan':
            dev = dev[8:]
            months = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
            now = datetime.now()
            str_mth = now.strftime('%m').lstrip("0")
            month = months[int(str_mth) - 1]
            year = now.strftime('%y')
            e = 'FS-' + dev + '-' + year + month
            last_experience_id = database.get_experience_id(self.entry_device_sn.get())
            if last_experience_id == 'no experience':
                id1 = '1000'
                e = str(e) + id1
            else:
                id2 = int(last_experience_id[-4:]) + 1
                e = str(e) + str(id2)
            self.entry_experience_id.insert(0, e)
            self.entry_experience_id.config(state='disabled')
            # self.b_generate_experience_id.config(state='disabled')
            global g_experience_id
            g_experience_id = e
            logging.info(f'Experience id has been generated: {g_experience_id}')
            print('Done, experience ID for FreeScan product has been generated! ', e)
        elif dev[:7] == 'EinScan':
            dev = dev[7:]
            months = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
            now = datetime.now()
            str_mth = now.strftime('%m').lstrip("0")
            month = months[int(str_mth) - 1]
            year = now.strftime('%y')
            e = 'ES-' + dev + '-' + year + month
            last_experience_id = database.get_experience_id(self.entry_device_sn.get())
            if last_experience_id == 'no experience':
                id1 = '1000'
                e = str(e) + id1
            else:
                print(last_experience_id)
                id2 = int(last_experience_id[-4:]) + 1
                e = str(e) + str(id2)
            self.entry_experience_id.insert(0, e)
            self.entry_experience_id.config(state='disabled')
            # self.b_generate_experience_id.config(state='disabled')
            g_experience_id = e
            logging.info(f'Experience id has been generated: {g_experience_id}')
            print('Done, experience ID for EinScan product has been generated! ', e)
        else:
            months = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
            now = datetime.now()
            str_mth = now.strftime('%m').lstrip("0")
            month = months[int(str_mth) - 1]
            year = now.strftime('%y')
            e = dev + '-' + year + month
            last_experience_id = database.get_experience_id(self.entry_device_sn.get())
            if last_experience_id == 'no experience':
                id1 = '1000'
                e = str(e) + id1
            else:
                print(last_experience_id)
                id2 = int(last_experience_id[-4:]) + 1
                e = str(e) + str(id2)
            self.entry_experience_id.insert(0, e)
            self.entry_experience_id.config(state='disabled')
            # self.b_generate_experience_id.config(state='disabled')
            g_experience_id = e
            logging.info(f'Experience id has been generated: {g_experience_id}')
            print('Done, experience ID for an other product has been generated! ', e)

        self.db_insert_experience()

    # Insert values to entries from xml file
    def insert_to_entries(self, x, y, z, t, r):
        self.entry_device_sn.insert(0, x)
        self.cbb_experience_type_str.set(y)
        self.cbb_department_str.set(z)
        self.cbb_operator_str.set(t)
        self.cbb_artefact_type.set(r)
        logging.info(
            f'Following fields are filled with XML: {self.entry_device_sn.get()}, {self.cbb_experience_type_str.get()}, {self.cbb_department_str.get()}, {self.cbb_operator_str.get()}, {self.cbb_artefact_type.get()}')

    # Get data from selected XML file
    def get_data_from_xml(self):
        self.reset_fields()
        from tkinter import filedialog
        global g_xml_url
        try:
            g_xml_url = filedialog.askopenfilename(
                initialdir='C:/Users/shining3d/Desktop/s3d_db_management/test_write_xml',
                title='Select File',
                filetypes=(('XML files', '*.xml'), ('All files', '*.*')))
            file = xml.dom.minidom.parse(g_xml_url)
            elements = file.getElementsByTagName('AutoTextCustomFieldValue')
            dev = elements[2].childNodes[0].nodeValue
            etype = elements[3].childNodes[0].nodeValue
            dep = elements[0].childNodes[0].nodeValue
            op = elements[1].childNodes[0].nodeValue
            artsn = elements[4].childNodes[0].nodeValue
            self.insert_to_entries(dev, etype, dep, op, artsn)
        except:
            print('XML file not selected!')

    # Reset all entries
    def reset_fields(self):
        self.entry_device_sn.config(state='normal')
        self.cbb_operator_str.set('')
        self.cbb_department_str.set('')
        self.cbb_experience_type_str.set('')
        self.cbb_artefact_type_str.set('')
        self.cbb_certificate_sn_str.set('')
        self.entry_experience_id.config(state='normal')
        self.entry_device_sn.delete(0, END)
        self.entry_experience_id.delete(0, END)
        self.text_subject.delete(1.0, END)
        # self.b_generate_experience_id.config(state='normal')
        self.button_create_experience.config(state='normal')
        self.button_copy.config(state='normal')
        logging.info('Page has been reset.')

    def copy_experience_id(self):
        pyperclip.copy(self.entry_experience_id.get())
        self.button_copy.config(state='disabled')


# Page two
class PageClassTwo(PageClass):

    def __init__(self, *args, **kwargs):
        PageClass.__init__(self, *args, **kwargs)

        # Variables
        self.entry_experience_id = None
        self.asc_date = None
        self.csv_url = None
        self.csv = None
        self.asc_data = None
        self.cxproj_data = None

        # Buttons, entries, labels
        label_title = tk.Label(self, text='New Test Page', font=fonts.NORMAL_FONT)
        label_title.grid(row=0, column=0, pady=5, padx=5, ipadx=5, ipady=5, sticky="NSEW", columnspan=3)

        self.label_experience_id = tk.Label(self, text="ExperienceID:")
        self.label_experience_id.grid(row=1, column=0, padx=5, pady=5, ipadx=5, ipady=5, sticky="NSEW")

        self.entry_experience_id = tk.Entry(self)
        self.entry_experience_id.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="NSEW")

        button_paste = tk.Button(self, command=lambda: self.paste_experience_id(), text='Paste')
        button_paste.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="NSEW")

        b_copy = tk.Button(self, command=lambda: pyperclip.copy(g_experience_id), text='Copy Experience ID')
        b_copy.grid(row=2, column=2, padx=5, pady=5, ipadx=5, ipady=5, sticky="NSEW")

        button_save_xml = tk.Button(self, command=lambda: methods.generate_xml(self.entry_experience_id.get()),
                                    text='Save XML')
        button_save_xml.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="NSEW")

        '''sep_1 = ttk.Separator(self, orient='horizontal')
        sep_1.grid(row=3, column=0, columnspan=4, sticky="NSEW", pady=10, padx=5)

        b_select_asc_files = tk.Button(self, command=lambda: self.select_asc(), text='Select ASC files')
        b_select_asc_files.grid(row=4, column=0, rowspan=2, padx=5, pady=5, ipadx=5, ipady=2, sticky="NSEW")

        b_select_cxproj_files = tk.Button(self, command=lambda: self.select_cxproj(), text='Select CXProj files')
        b_select_cxproj_files.grid(row=6, column=0, rowspan=2, padx=5, pady=5, ipadx=5, ipady=2, sticky="NSEW")

        self.asc_l = tk.StringVar()
        self.asc_label = tk.Label(self, textvariable=self.asc_l, text='asc')
        self.asc_label.grid(row=4, column=1, rowspan=2, padx=5, pady=5, ipadx=5, ipady=2, sticky="NSEW")

        self.cxproj_l = tk.StringVar()
        self.cxproj_label = tk.Label(self, textvariable=self.cxproj_l, text='cxproj')
        self.cxproj_label.grid(row=6, column=1, rowspan=2, padx=5, pady=5, ipadx=5, ipady=2, sticky="NSEW")

        b_start_geomagic_cx = tk.Button(self, command=lambda: self.launch_cx(), text='Start CX Server')
        b_start_geomagic_cx.grid(row=4, column=3, padx=5, pady=5, ipadx=5, ipady=2, sticky="NSEW")

        b_start_batch = tk.Button(self, command=lambda: self.start_batch(), text='Start Batch')
        b_start_batch.grid(row=5, column=3, rowspan=3, padx=5, pady=5, ipadx=5, ipady=2, sticky="NSEW")
'''
        separator_1 = ttk.Separator(self, orient='horizontal')
        separator_1.grid(row=8, column=1, padx=5, pady=10, sticky="NSEW")

        button_select_csv = tk.Button(self, command=lambda: self.select_csv(), text='Select CSV files')
        button_select_csv.grid(row=9, column=0, padx=5, pady=5, sticky="NSEW")

        self.label_selected_csv_str = tk.StringVar()
        self.label_selected_csv = tk.Label(self, textvariable=self.label_selected_csv_str, text='csv')
        self.label_selected_csv.grid(row=9, column=1, padx=5, pady=5, sticky="NSEW")

        button_save_csv_results = tk.Button(self, command=lambda: database.insert_table_select(self.csv_url),
                                            text='Send to Database')
        button_save_csv_results.grid(row=9, column=2, padx=5, pady=5, sticky="NSEW")

        self.text_content = tk.Text(self, width=20, height=3)
        self.text_content.grid(row=10, column=0, columnspan=2, padx=5, pady=7, ipadx=5, ipady=5, sticky="NSEW")

        button_save_content = tk.Button(self, command=lambda: database.insert_content(self.text_content.get('1.0', END),
                                                                                      g_experience_id),
                                        text='Save Content')
        button_save_content.grid(row=10, column=2, padx=5, pady=5, sticky="NSEW")

    # Paste the experience ID
    def paste_experience_id(self):
        self.entry_experience_id.insert(0, g_experience_id)
        self.entry_experience_id.config(state='disabled')

    # Select CSV files to be merged and uploaded in database
    def select_csv(self):
        self.csv = fd.askopenfilenames(initialdir='/Users/kadirakca/git_projects/s3d_db_management/CSV/',
                                       title='Select Files',
                                       filetypes=(('CSV files', '*.csv'), ('All files', '*.*')))
        self.csv_url = self.csv[0]
        label = os.path.basename(self.csv_url)
        self.label_selected_csv_str.set(label)
        logging.info('Following CSV file is chosen: ' + label)

    # Field that will be done in future
    '''def select_cxproj(self):
        cxproj = fd.askopenfilenames(initialdir='/Users/kadirakca/git_projects/s3d_db_management/CXProj/',
                                     title='Select Files',
                                     filetypes=(('CXProj files', '*.CXProj'), ('All files', '*.*')))
        cxproj = os.path.basename(cxproj[0])
        self.cxproj_data = cxproj
        self.cxproj_l.set(cxproj)


    def launch_cx(self):
        # os.startfile("app path")
        pass

    def start_batch(self):
        methods.copypaste(self.cxproj_data, 0)
        for i in self.asc_data:
            methods.copypaste(i, 1)

    def select_asc(self):
        asc = fd.askopenfilenames(initialdir='/Users/kadirakca/git_projects/s3d_db_management/ASC/',
                                  title='Select Files',
                                  filetypes=(('ASC files', '*.asc'), ('All files', '*.*')))
        self.asc_data = asc
        print(self.asc_data)
        asc2 = ''
        for i in asc:
            ii = os.path.basename(i)
            if asc2 == '':
                asc2 = ii
            else:
                asc2 = asc2 + '\n' + ii

        self.asc_l.set(asc2)'''


# Run the application until exit
if __name__ == '__main__':
    root = tk.Tk()
    main = DatabaseManagement(root)
    main.pack(side='top', fill='both', expand=True)
    root.wm_title('Database Management Tool for Accuracy Tests')
    root.wm_geometry("350x600")
    root.mainloop()
