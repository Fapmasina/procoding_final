import requests 

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import style

from bs4 import BeautifulSoup
from datetime import datetime

import tkinter
from tkinter import Tk,Button,ttk

from datetime import datetime, date

from choices import lista_gradova

style.use('ggplot')   

class App:

    def __init__(self, master):

        frame = tkinter.Frame(master)

        # Create 2 buttons
        self.label = ttk.Label(frame,text = "Izaberi grad: ")
        self.label.grid(row=0, column=1)
        self.drop = ttk.Combobox(frame,value=[i for i in lista_gradova.values()],width = 50, font = 12)
        self.drop.grid(row=0, column=2)
        self.button_left = tkinter.Button(frame,text="Odabir",command=self.sumpor_podaci )
        self.button_left.grid(row=0, column=3)

        # Create Figur
        self.fig = Figure(figsize = (5,5), dpi = 100) 
        self.ax = self.fig.add_subplot(111)
        self.ax.plot()  
        self.canvas = FigureCanvasTkAgg(self.fig,master=master)
        self.canvas.get_tk_widget().pack(side='bottom', fill='both', expand=1)
        
        frame.pack()

    def sumpor_podaci(self):
		
        izbor = self.drop.get()
        print(izbor)

        for id,grad in lista_gradova.items():
            if grad == izbor:
                pass_izbor = id
        url = requests.get('http://www.amskv.sepa.gov.rs/konektori/pregled_tabela.php?komponente%5B%5D=1&stanica={}&periodi%5B%5D=danas'.format(pass_izbor))
        bs = BeautifulSoup(url.text, 'html.parser')
        table = bs.table
        table_rows =table.find_all('tr')
        podaci = {}

        for th in table_rows[1:]:
            vreme = th.find_all('td')[0].text
            konvertovano_v = datetime.strptime(vreme, '%Y-%m-%d %H:%M:%S').time()
            vreme = str(konvertovano_v)     
            vrednosti = th.find_all('td')[1].text
              
            try:
                podaci[vreme] = float(vrednosti)
            except ValueError:
                vrednosti = 0
                podaci[vreme] = float(vrednosti)
        
        x = list(x for x in podaci.keys())
        y = list(x for x in podaci.values())
        print(podaci)
        self.ax.clear()
    
        self.fig.suptitle('{}\n datum: {}'.format(izbor,datetime.now().date()), fontsize = 15)
        self.ax.plot(x,y)
        self.ax.set_xlabel('Vreme ')
        self.ax.set_ylabel('Zagadjenje po jed. mere ')
        self.ax.tick_params(axis='x', labelrotation=90)
        self.canvas.draw()

def main():
    root = tkinter.Tk()
    root.geometry('1200x900')
    app = App(root)
    root.mainloop()

main()