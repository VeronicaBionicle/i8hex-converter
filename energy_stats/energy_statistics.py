import os
from utils import DATA_DIR, CHART_DIR
import numpy as np
#import matplotlib.pyplot as plt
from matplotlib.pyplot import clf, plot, title, grid, gcf, gca, xlabel, xlim, xticks, ylabel, ylim, yticks, hlines, savefig, show, subplots_adjust, get_current_fig_manager
import matplotlib.dates as mdates
from datetime import datetime

# func to decorate and plot graph
def plot_graph(x, y, plot_standart = True, fname = None):
    clf()
    # plot graph from real line voltages
    plot(x, y, linewidth=2, color='seagreen', linestyle='-', marker='.')
    '''
    #from scipy.interpolate import interp1d
    # averaged
    prep_x = x - min(x) 
    f = interp1d(prep_x, y, kind='cubic')
    xnew = np.linspace(min(prep_x), max(prep_x), 1000, endpoint=True)
    plot(xnew+min(x),f(xnew), linestyle='-', linewidth=2, color = 'red')
    '''
    # plot graph of standart voltage
    if plot_standart:
        standart_voltages = [220*0.9, 220, 220*1.1]
        for voltage in standart_voltages:
            hlines(voltage, min(x), max(x), linestyle='--', color = 'orangered')
    # decoration
    title("Данные о напряжении за период: " +  
            datetime.strftime(min(file_dates), "%d/%m/%Y") + ' - ' +   # first date from file
            datetime.strftime(max(file_dates), "%d/%m/%Y"), size ='xx-large')   # last date from file
    grid(True, linestyle='-', color='0.75')
    # Х axis
    xlabel("Дата", size = 'x-large')
    gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%y %H:%M'))   # format ticks 
    gca().xaxis.set_major_locator(mdates.HourLocator(interval = 1))  # interval of ticks - 1 hour
    gcf().autofmt_xdate()
    xticks(ha ='center', rotation=60)  
    xlim(min(x), max(x))
    # Y axis
    ylabel("Напряжение в сети, В", size ='x-large')
    yticks( np.arange(195, 245, 1), rotation='horizontal')
    ylim(195, 245)
    # saving file
    if (fname): # if name != None
        subplots_adjust(left=0.01, bottom=0.07, right=0.99, top=0.97)
        figure = gcf() # choose current graph
        figure.set_size_inches(len(x_dates)/6, 20) 
        savefig(os.path.join(CHART_DIR, fname), dpi = 72) 
    # adjust and fullscreen
    subplots_adjust(left=0.04, bottom=0.12, right=0.99, top=0.97)
    get_current_fig_manager().full_screen_toggle() # (f on keyboard)
    show()

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
file_name = None # "all.png"
plot_graph(x_dates, y, plot_standart = True, fname = file_name)