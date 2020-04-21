import os
from utils import DATA_DIR, CHART_DIR
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# func to decorate and plot graph
def plot_graph(x, y, fname):
    #global x_name
   # global y_name
    plt.clf()
    # plot graph
    plt.plot(x, y, linewidth=2, color='seagreen', linestyle='-', marker='.', picker=True)  
    # decoration
    plt.title("Данные о напряжении за период: " +  
            datetime.strftime(min(file_dates), "%d/%m/%Y") + ' - ' +   # начальная дата из данных
            datetime.strftime(max(file_dates), "%d/%m/%Y"), size ='xx-large')   # конечная дата из данных
    plt.grid(True, linestyle='-', color='0.75') #сетка
    # Х axis
    plt.xlabel("Дата", size = 'x-large')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%y %H:%M'))   #форматирование в формате даты
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval = 1))  # интервал - 1 час
    plt.gcf().autofmt_xdate()
    plt.xticks(ha ='center', rotation=60)  
    plt.xlim(min(x), max(x))
    # Y axis
    plt.ylabel("Напряжение в сети, В", size ='x-large')
    plt.yticks( np.arange(200, np.floor(max(y)), 1), rotation='horizontal')
    plt.ylim(200, np.ceil(max(y)))
    # saving file
    if (fname): # if name != None
        plt.subplots_adjust(left=0.01, bottom=0.07, right=0.99, top=0.97)
        figure = plt.gcf() # choose current graph
        figure.set_size_inches(len(x_dates)/6, 20) 
        plt.savefig(os.path.join(CHART_DIR, fname), dpi = 72) 
    # adjust and fullscreen
    plt.subplots_adjust(left=0.04, bottom=0.12, right=0.99, top=0.97)
    plt.get_current_fig_manager().full_screen_toggle() # (f on keyboard)
    plt.show()

#parce data from txt -> 0 column - dates, 3 column - Line Voltage
file_dates, y_prices = np.loadtxt(
            os.path.join(DATA_DIR, 'Datalog_21_04_2020.txt'),
            delimiter = '	',
            dtype = object,
            converters={0: lambda x: datetime.strptime(x.decode("utf-8"), "%m/%d/%Y %H:%M:%S"), 3:float},  
            usecols=(0,3),
            unpack=True,
            skiprows = 1 #skip title
)
# formatting
x_dates = mdates.date2num(file_dates)   # format data objects to number of days from 0001-01-01
y = y_prices.astype(float)   # format to float
# output
file_name = "all.png"
plot_graph(x_dates, y, fname=file_name)