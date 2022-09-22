import os.path
import tkinter as tk
import xml.dom.minidom
from datetime import datetime
from tkinter import LEFT, ttk, END, messagebox, NW, N
import tkinter.filedialog as fd

import pyperclip

import database
import fonts
import methods
import logging

g_xml_url = ''
g_experience_id = ''

application_title = 'S3D Accuracy Test Database Management'

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
        button_frame.pack(side="bottom", fill="both", expand=False)
        container.pack(side="top", fill="both", expand=True, anchor=N)

        p1.place(in_=container, x=190, y=0, anchor=N, relheight=1)
        p2.place(in_=container, x=190, y=0, anchor=N, relheight=1)
        # p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        button_first_page = tk.Button(button_frame, text='New Experience', command=p1.show)
        button_second_page = tk.Button(button_frame, text='Store Results', command=lambda: p2.show())

        button_open_db = tk.Button(button_frame, text='Open Database', command=lambda: database.open_db())
        button_quit_app = tk.Button(button_frame, text='Exit', command=lambda: methods.quit_app())

        button_first_page.pack(side=LEFT)
        button_second_page.pack(side=LEFT)
        button_open_db.pack(side=LEFT)
        button_quit_app.pack(side=LEFT)

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
        label = tk.Label(self, text='New Experience', font=fonts.NORMAL_FONT)
        label.grid(row=0, column=0, pady=10, padx=10, sticky="NSEW", columnspan=3)

        self.entry_device_sn = tk.Entry(self)
        self.entry_device_sn.grid(row=1, column=1, columnspan=2, padx=5, pady=5, ipadx=5, ipady=5, sticky="NSEW")

        self.cbb_department_str = tk.StringVar()
        self.cbb_department = ttk.Combobox(self, textvariable=self.cbb_department_str)
        self.cbb_department.bind('<<ComboboxSelected>>', self.cbb_list_operators)
        self.cbb_department.grid(row=2, column=1, columnspan=2, padx=5, pady=5, ipadx=5, ipady=5, sticky="NSEW")
        self.cbb_department['values'] = database.get_departments()
        self.cbb_department['state'] = 'readonly'

        self.cbb_operator_str = tk.StringVar()
        self.cbb_operator = ttk.Combobox(self, textvariable=self.cbb_operator_str)
        self.cbb_operator.grid(row=3, column=1, columnspan=2, padx=5, pady=5, ipadx=5, ipady=5, sticky="NSEW")
        self.cbb_operator['values'] = database.get_operators(self.cbb_department_str.get())
        self.cbb_operator['state'] = 'readonly'

        self.cbb_experience_type_str = tk.StringVar()
        self.cbb_experience_type = ttk.Combobox(self, textvariable=self.cbb_experience_type_str)
        self.cbb_experience_type.bind('<<ComboboxSelected>>', self.cbb_list_artefact_types)
        self.cbb_experience_type.grid(row=4, column=1, columnspan=2, padx=5, pady=5, ipadx=5, ipady=5, sticky="NSEW")
        self.cbb_experience_type['values'] = database.get_experience_types()
        self.cbb_experience_type['state'] = 'readonly'

        self.cbb_artefact_type_str = tk.StringVar()
        self.cbb_artefact_type = ttk.Combobox(self, textvariable=self.cbb_artefact_type_str)
        self.cbb_artefact_type.bind('<<ComboboxSelected>>', self.cbb_list_certificate_numbers)
        self.cbb_artefact_type.grid(row=5, column=1, columnspan=2, padx=5, pady=5, ipadx=5, ipady=5, sticky="NSEW")
        self.cbb_artefact_type['state'] = 'readonly'

        self.cbb_certificate_sn_str = tk.StringVar()
        self.cbb_certificate_sn = ttk.Combobox(self, textvariable=self.cbb_certificate_sn_str)
        self.cbb_certificate_sn.grid(row=6, column=1, padx=5, columnspan=2, pady=5, ipadx=5, ipady=5, sticky="NSEW")
        self.cbb_certificate_sn['state'] = 'readonly'

        self.text_subject = tk.Text(self, width=20, height=3)
        self.text_subject.grid(row=7, column=1, columnspan=2, padx=5, pady=7, ipadx=5, ipady=5, sticky="NSEW")

        self.entry_experience_id = tk.Entry(self)
        self.entry_experience_id.grid(row=10, column=1, rowspan=2, padx=5, pady=5, ipadx=5, ipady=5, sticky="NSEW")

        self.label_log_str = tk.StringVar()
        self.label_log = tk.Label(self, textvariable=self.label_log_str, text='csv')
        self.label_log.grid(row=13, column=0, columnspan=3, padx=5, pady=5, sticky="NSEW")

        label_device_sn = tk.Label(self, text="Device Serial No.:")
        label_device_sn.grid(row=1, column=0)
        label_operator = tk.Label(self, text="Operator")
        label_operator.grid(row=3, column=0)
        label_department = tk.Label(self, text="Department:")
        label_department.grid(row=2, column=0)
        label_experience_type = tk.Label(self, text="Experience Type:")
        label_experience_type.grid(row=4, column=0)
        label_artefact_type = tk.Label(self, text="Artefact Type:")
        label_artefact_type.grid(row=5, column=0)
        label_certificate_sn = tk.Label(self, text="Certificate No.:")
        label_certificate_sn.grid(row=6, column=0)
        label_subject = tk.Label(self, text="Subject:")
        label_subject.grid(row=7, column=0)
        label_experience_id = tk.Label(self, text="Experience ID:")
        label_experience_id.grid(row=10, column=0)

        self.button_fill_xml = tk.Button(self, text='Fill with XML', command=lambda: self.get_data_from_xml())
        self.button_fill_xml.grid(row=8, column=0, padx=5, pady=5, columnspan=3, sticky="NSEW")

        self.button_reset = tk.Button(self, command=lambda: self.reset_fields(), text='Reset All')
        self.button_reset.grid(row=12, column=0, columnspan=3, padx=5, pady=5, sticky="NSEW")

        self.button_copy = tk.Button(self, text='Copy', command=lambda: self.copy_experience_id())
        self.button_copy.grid(row=10, column=2, padx=5, pady=5, sticky="NSEW")

        self.button_create_experience = tk.Button(self, text='Generate Experience ID and Create Experience',
                                                  command=lambda: self.generate_experience_id())
        self.button_create_experience.grid(row=9, column=0, columnspan=3, padx=5, pady=5, sticky="NSEW")

        '''button_add_operator = tk.Button(self, text='Add operator', command=lambda: self.add_ops())
        button_add_operator.grid(row=2, column=2, padx=5, pady=5, sticky="NSEW")

        self.b_generate_experience_id = tk.Button(self, text='Generate Experience ID',
                                                          command=lambda: self.generate_experience_id())
        self.b_generate_experience_id.grid(row=9, column=2, padx=5, pady=5, sticky="NSEW")'''

    def generate_log(self, log):
        self.label_log_str.set(log)

    # Method: insert entries to database
    def insert_experience_to_database(self):
        try:
            device_sn = self.entry_device_sn.get()
            operator = self.cbb_operator_str.get()
            department = self.cbb_department_str.get()
            experience_type = self.cbb_experience_type_str.get()
            artefact_type = self.cbb_artefact_type_str.get()
            certificate_sn = self.cbb_certificate_sn_str.get()
            subject = self.text_subject.get('1.0', END)
            experience_id = self.entry_experience_id.get()
            if subject == "\n":
                subject = None
            if database.check_experience_id(experience_id) != 'exist':
                database.insert_experience(device_sn, operator, department, experience_type, artefact_type,
                                           certificate_sn, subject, experience_id)
            else:
                print('Database: Experience already exists in database!')
                self.generate_log('Database: Experience already exists in database!')
            self.button_create_experience.config(state='disabled')

        except:
            print('Database: Failed to insert experience in database!')
            self.generate_log('Database: Failed to insert experience in database!')

    # New window: to add new operator
    '''def add_operator(self):
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
        x = database.check_operator_id()
        if s == x or self.entry_person.get() == '':
            self.label_confirm['text'] = 'Nothing Added!'
            return True
        elif x == s + 1:
            self.label_confirm['text'] = 'Added Successfully!'
            x += 1
            return False

    # confirm new operator
    def add_operator_confirm(self):
        x = database.check_operator_id()
        a = self.entry_person.get()
        d = datetime.now().strftime('%d-%m-%y %H:%M')
        database.insert_operator(a, d)
        self.add_operator_check(x)
        self.cbb_operator.config(values=database.get_operators())'''

    # Dynamic refresh of the fields
    def cbb_list_operators(self, *args):
        # self.cbb_operator.config(values=['ss'])
        department = self.cbb_department_str.get()
        # self.cbb_operator.set('')
        operators = database.get_operators(department)
        self.cbb_operator.config(state='readonly')
        self.cbb_operator.config(values=operators)

    def cbb_list_artefact_types(self, *args):
        # self.cbb_artefact_type.config(values=[])
        m = self.cbb_experience_type_str.get()
        # self.cbb_artefact_type.set('')
        n = database.get_artefact_types(m)
        self.cbb_artefact_type.config(state='readonly')
        self.cbb_artefact_type.config(values=n)

    def cbb_list_certificate_numbers(self, *args):
        # self.cbb_certificate_sn.config(values=[])
        m = self.cbb_artefact_type_str.get()
        # self.cbb_certificate_sn.set('')
        n = database.get_certificate_nos(m)
        self.cbb_certificate_sn.config(state='readonly')
        self.cbb_certificate_sn.config(values=n)

    # Generate an experience id based on device SN and date
    def generate_experience_id(self):
        device_sn = str(self.entry_device_sn.get())
        experience_type = str(self.cbb_experience_type.get())
        if device_sn == '':
            print('Experience ID: Failed to generate! Device Serial Number is empty.')
            messagebox.showerror(application_title,
                                 "Experience ID: Failed to generate!\n\nDevice Serial Number is empty.")
            self.generate_log('Experience ID: Failed to generate!\n\nDevice Serial Number is empty.')
        elif experience_type == '':
            print('Experience ID: Failed to generate! Experience Type is empty.')
            messagebox.showerror(application_title, "Experience ID: Failed to generate!\n\nExperience Type is empty.")
            self.generate_log('Experience ID: Failed to generate!\n\nExperience Type is empty.')
        else:
            if device_sn[:8] == 'FreeScan':
                device_sn = device_sn[8:]
                months = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
                now = datetime.now()
                str_mth = now.strftime('%m').lstrip("0")
                month = months[int(str_mth) - 1]
                year = now.strftime('%y')
                e = 'FS-' + device_sn + '-' + year + month
                last_experience_id = database.get_experience_id(self.entry_device_sn.get())
                if last_experience_id == 'no experience':
                    id1 = '1000'
                    e = str(e) + id1
                else:
                    id2 = int(last_experience_id[-4:]) + 1
                    e = str(e) + str(id2)
                self.entry_experience_id.insert(0, e)
                self.entry_experience_id.config(state='disabled')
                global g_experience_id
                g_experience_id = e
            elif device_sn[:7] == 'EinScan':
                device_sn = device_sn[7:]
                months = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
                now = datetime.now()
                str_mth = now.strftime('%m').lstrip("0")
                month = months[int(str_mth) - 1]
                year = now.strftime('%y')
                e = 'ES-' + device_sn + '-' + year + month
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
                g_experience_id = e
            else:
                months = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
                now = datetime.now()
                str_mth = now.strftime('%m').lstrip("0")
                month = months[int(str_mth) - 1]
                year = now.strftime('%y')
                e = device_sn + '-' + year + month
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
            self.insert_experience_to_database()
            self.generate_log('Experience ID: Successfully generated! ' + g_experience_id)
            print('Experience ID: Successfully generated! ', g_experience_id)

    # Insert values to entries from xml file
    def insert_to_entries(self, device_sn, department, operator, experience_type, artefact_type):
        self.entry_device_sn.insert(0, device_sn)
        self.cbb_experience_type_str.set(experience_type)
        self.cbb_department_str.set(department)
        self.cbb_operator_str.set(operator)
        self.cbb_artefact_type.set(artefact_type)
        self.cbb_list_operators()
        self.cbb_list_artefact_types()
        self.cbb_list_certificate_numbers()

    # Get data from selected XML file
    def get_data_from_xml(self):
        self.reset_fields()
        from tkinter import filedialog
        global g_xml_url
        try:
            g_xml_url = filedialog.askopenfilename(
                initialdir='write_xml',
                title='Select File',
                filetypes=(('XML files', '*.xml'), ('All files', '*.*')))
            file = xml.dom.minidom.parse(g_xml_url)
            elements = file.getElementsByTagName('AutoTextCustomFieldValue')
            device_sn = elements[2].childNodes[0].nodeValue
            department = elements[0].childNodes[0].nodeValue
            operator = elements[1].childNodes[0].nodeValue
            experience_type = elements[3].childNodes[0].nodeValue
            artefact_type = elements[4].childNodes[0].nodeValue
            print(device_sn, department, operator, experience_type, artefact_type)
            self.insert_to_entries(device_sn, department, operator, experience_type, artefact_type)
            # messagebox.showinfo("Info", "XML correctly uploaded!\n\n\tDevice Serial Number:\t%s \n\tDepartment:\t\t%s "
            #                            "\n\tOperator:\t\t%s \n\tExperience Type:\t\t%s \n\tArtefact Type:\t\t%s" % (
            #                        device_sn, department, operator, experience_type, artefact_type))
            print('XML Template: Correctly uploaded!\n\t%s \n\t%s \n\t%s \n\t%s \n\t%s' % (
                device_sn, department, operator, experience_type, artefact_type))
            self.generate_log("XML Template: Correctly uploaded!")
        except:
            print("XML Template: File not selected.")
            messagebox.showwarning(application_title, "XML Template: File not selected!\n\nPlease select an XML file!")

    # Reset all entries.
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
        self.button_create_experience.config(state='normal')
        self.button_copy.config(state='normal')
        self.generate_log('All entries have been reset!')

    # Copy experience id.
    def copy_experience_id(self):
        if self.entry_experience_id.get() != "":
            pyperclip.copy(self.entry_experience_id.get())
            self.generate_log('Experience id copied!')
        else:
            messagebox.showerror(application_title, "Nothing to copy!")
            self.generate_log('Nothing to copy!')


# Page two
class PageClassTwo(PageClass):

    def __init__(self, *args, **kwargs):
        PageClass.__init__(self, *args, **kwargs)

        # Variables
        self.cbb_experience_id = None
        self.asc_date = None
        self.csv_url = None
        self.csv = None

        # Buttons, entries, labels
        label_title = tk.Label(self, text='Generate XML and Store Results', font=fonts.NORMAL_FONT)
        label_title.grid(row=0, column=0, pady=5, padx=5, ipadx=5, ipady=5, sticky="NSEW", columnspan=3)

        self.label_experience_id = tk.Label(self, text="ExperienceID:")
        self.label_experience_id.grid(row=1, column=0, padx=5, pady=5, ipadx=5, ipady=5, sticky="NSEW")

        self.cbb_experience_id_str = tk.StringVar()
        self.cbb_experience_id = ttk.Combobox(self, textvariable=self.cbb_experience_id_str)
        self.cbb_experience_id.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="NSEW")
        self.cbb_experience_id.config(state='normal')
        self.cbb_experience_id.config(values=self.cbb_list_experience_ids())

        button_paste = tk.Button(self, command=lambda: self.paste_experience_id(), text='Paste and Update List')
        button_paste.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="NSEW")

        b_copy = tk.Button(self, command=lambda: self.copy_experience_id(), text='Copy')
        b_copy.grid(row=2, column=2, padx=5, pady=5, ipadx=5, ipady=5, sticky="NSEW")

        button_save_xml = tk.Button(self, command=lambda: self.generate_xml(self.cbb_experience_id.get()),
                                    text='Save XML')
        button_save_xml.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="NSEW")

        '''
        sep_1 = ttk.Separator(self, orient='horizontal')
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
        separator_1.grid(row=8, column=0, columnspan=3, padx=5, pady=10, sticky="NSEW")

        button_select_csv = tk.Button(self, command=lambda: self.select_csv(), text='Select CSV file')
        button_select_csv.grid(row=9, column=0, columnspan=3, padx=5, pady=5, sticky="NSEW")

        self.label_selected_csv = tk.Label(self, text='Selected CSV file: ')
        self.label_selected_csv.grid(row=10, column=0, padx=5, pady=5, sticky="NSEW")

        self.label_selected_csv_str = tk.StringVar()
        self.label_selected_csv_dyn = tk.Label(self, textvariable=self.label_selected_csv_str)
        self.label_selected_csv_dyn.grid(row=10, column=1, columnspan=2, padx=5, pady=5, sticky="NSEW")

        self.label_content = tk.Label(self, text='Content: ')
        self.label_content.grid(row=11, column=0, padx=5, pady=5, sticky="NSEW")

        self.text_content = tk.Text(self, width=20, height=2)
        self.text_content.grid(row=11, column=1, columnspan=2, padx=5, pady=5, ipadx=5, ipady=5, sticky="NSEW")

        self.button_save_csv_content = tk.Button(self, command=lambda: self.store_csv_and_content(),
                                                 text='Store CSV and Content')
        self.button_save_csv_content.grid(row=12, column=0, columnspan=3, padx=5, pady=5, sticky="NSEW")

        self.label_log_str = tk.StringVar()
        self.label_log = tk.Label(self, textvariable=self.label_log_str, text='csv')
        self.label_log.grid(row=13, column=0, columnspan=3, padx=5, pady=5, sticky="NSEW")

    # Generate a new XML file from the entries.
    def generate_xml(self, experience_id):
        file = xml.dom.minidom.parse('write_xml/data.xml')
        x1 = file.getElementsByTagName('AutoTextCustomFieldValue')
        data = database.get_attributes_from_experience_id(experience_id)

        x1[2].childNodes[0].nodeValue = data[1]  # experience id - dev sn
        x1[1].childNodes[0].nodeValue = data[3]  # serial number-op
        x1[0].childNodes[0].nodeValue = data[2]  # dep
        x1[3].childNodes[0].nodeValue = data[4]  # operator-exptype
        x1[4].childNodes[0].nodeValue = data[5]  # experience type-arttype

        with open("write_xml/" + experience_id + '.xml', "w") as xml_template:
            file.writexml(xml_template)

        print('XML Template: Successfully generated! %s.xml' % experience_id)
        self.generate_log('XML Template: Successfully generated!\n\n%s.xml' % experience_id)
        messagebox.showinfo(application_title, 'XML Template: Successfully generated!\n\n%s.xml' % experience_id)

    def cbb_list_experience_ids(self, *args):
        self.cbb_experience_id.set('')
        experience_ids = database.get_experience_ids()
        return experience_ids

    def copy_experience_id(self):
        if self.cbb_experience_id.get() != "":
            pyperclip.copy(self.cbb_experience_id.get())
            self.generate_log('Successfully copied!')
        else:
            self.generate_log('Nothing to copy!')
            messagebox.showerror(application_title, "Nothing to copy!")

    # Paste the experience ID
    def paste_experience_id(self):
        self.cbb_experience_id.config(values=self.cbb_list_experience_ids())
        self.cbb_experience_id.set(g_experience_id)

    # Select CSV files to be merged and uploaded in database
    def select_csv(self):
        self.csv = fd.askopenfilenames(initialdir='write_csv\data_to_be_merged',
                                       title='Select Files',
                                       filetypes=(('CSV files', '*.csv'), ('All files', '*.*')))
        self.csv_url = self.csv[0]
        label = os.path.basename(self.csv_url)
        self.label_selected_csv_str.set(label)

    def store_csv_and_content(self):
        database.select_table_to_insert(self.csv_url, self.cbb_experience_id.get())
        database.insert_content(self.text_content.get('1.0', END), self.cbb_experience_id.get())

    def generate_log(self, log):
        self.label_log_str.set(log)

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
    main.pack(side='bottom', fill='both', expand=True)
    root.wm_title('Database Management Tool for Accuracy Tests')
    root.geometry("380x800+100+100")
    root.mainloop()
