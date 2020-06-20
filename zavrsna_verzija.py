from bs4 import BeautifulSoup
import requests 

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
from matplotlib import style

import tkinter
from tkinter import Tk,Button,ttk

from datetime import datetime, date

from choices import town_list

from zipfile import ZipFile

import os

style.use('ggplot')   

class Application:

    def __init__(self, master):

        frame = tkinter.Frame(master)

        # Create buttons
        self.label = ttk.Label(frame,text = "Izaberi grad: ")
        self.label.grid(row=0, column=1,padx=10, pady=10)
        self.drop = ttk.Combobox(frame,value=[i for i in town_list.values()],width = 50, font = 12)
        self.drop.grid(row=0, column=2,padx=10, pady=10)
        self.data_button = tkinter.Button(frame,text="Prikazi Podatke",command=self.collect_and_deliver )
        self.data_button.grid(row=0, column=3,padx=10, pady=10)
        self.save_button = tkinter.Button(frame,text="Sacuvaj Podatke",command=self.creating_folder )
        self.save_button.grid(row=0, column=4,padx=10, pady=10)
        self.zip_button = tkinter.Button(frame,text="Zip Podatke",command=self.zip_all_files )
        self.zip_button.grid(row=0, column=5,padx=10, pady=10)

        # Create Figure
        self.fig = Figure(dpi = 90) 
        self.ax = self.fig.add_subplot(111)
        self.ax.plot()  
        self.canvas = FigureCanvasTkAgg(self.fig,master=master)
        self.canvas.get_tk_widget().pack(side='bottom', fill='both', expand=1)

        self.toolbar = NavigationToolbar2Tk(self.canvas, master)
        self.toolbar.update()
        
        self.web_data = {}

        frame.pack()


    def collect_and_deliver(self):
        """ 
            Collecting data from web with requests and BeautifulSoup and storing them in dict() obj
            Data will be represented by matplotlib.plot and integrated in tkinter 
        """
        drop_choice = self.drop.get()

        # Find chosen data in town_list.dict and return id  
        for id,town in town_list.items():
            if town == drop_choice:
                pass_choice = id
        # Pass Id to requested URL
        url = requests.get('http://www.amskv.sepa.gov.rs/konektori/pregled_tabela.php?komponente%5B%5D=1&stanica={}&periodi%5B%5D=danas'.format(pass_choice))
        bs = BeautifulSoup(url.text, 'html.parser')
        # Web data are packed in table
        table = bs.table
        # Exctract data from web table
        table_rows = table.find_all('tr')
        for th in table_rows[1:]:
            date_time = th.find_all('td')[0].text
            # Convert str to time 
            konvertovano_v = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S').time()
            # And reverse it to drop date and keep only the time
            date_time = str(konvertovano_v)     
            so2_values = th.find_all('td')[1].text
            # If results from web table are '', add them value of 0   
            try:
                self.web_data[date_time] = float(so2_values)
            except ValueError:
                so2_values = 0
                self.web_data[date_time] = float(so2_values)
        # Add data to x,y axces (data need to be float, int ...)
        x = list(x for x in self.web_data.keys())
        y = list(x for x in self.web_data.values())
        # New Figure will replace initial one with new data
        self.ax.clear()# Important, destroy first old figure
        self.fig.suptitle('{}\n Datum: {}'.format(drop_choice,datetime.now().date()), fontsize = 15)
        self.ax.plot(x,y)
        self.ax.set_xlabel('Vreme')
        self.ax.set_ylabel('Zagadjenje po jed. mere za SO2')
        self.ax.tick_params(axis='x', labelrotation=90)
        self.canvas.draw()
    

    def creating_folder(self): 
        """ 
            Creating folder and saving the presented data inside 
        """
        drop_choice = self.drop.get() 
        #check drop-down box results
        if drop_choice == '':
            pass
        else:
            dirname = 'rezultati'
            try:
                # Create new Directory
                os.mkdir(dirname)
            except FileExistsError:
                pass
            # Path for new directory   
            script_dir = os.path.dirname(os.path.abspath(__file__))# Current file location
            dest_dir = os.path.join(script_dir, dirname)# New direct location

            # Create file and pass to destination
            filename = drop_choice +'.txt'
            file_path = os.path.join(dest_dir, filename)
            # Write data to a file
            with open(file_path, 'w') as f:
                print('SO2 = {}'.format(self.web_data), file = f )
            
            msg  = 'File name: {}'.format(filename)
            
            self.pop_up_msg(msg)


    def zip_all_files(self):
        """ 
            Zip all files from target directory, created by user
        """ 
        file_paths = []
        # path to folder which needs to be zipped 
        directory = './rezultati'

        for root, directories, files in os.walk(directory): 
            for filename in files: 
                filepath = os.path.join(root, filename) 
                file_paths.append(filepath) 
    
        # writing files to a zipfile 
        with ZipFile('zip_rezultati.zip','w') as zip: 
            for file in file_paths:     
                zip.write(file)
        
        msg  = 'Uspesno je kreiran zip fajl'
            
        self.pop_up_msg(msg) 
    

    def pop_up_msg(self,msg):

        pop_up = Tk()

        pop_up.title('')
        pop_up.geometry('300x100+500+400')

        label_1 = ttk.Label(pop_up, text = msg,font = 15)
        label_1.pack(padx=10, pady=10)

        pop_up_button = tkinter.Button(pop_up, text="Ok",command=pop_up.destroy, width = 40)
        pop_up_button.pack(padx=10, pady=10)

        pop_up.mainloop()


def main():
    root = tkinter.Tk()
    root.geometry('1200x900+400+400')
    root.title('ZAGADJENJE VAZDUHA')
    app = Application(root)
    root.mainloop()

main()