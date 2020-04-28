import os
from utils import DATA_DIR, CHART_DIR
import numpy as np
from matplotlib.pyplot import clf, plot, title, grid, gcf, gca, xlabel, xlim, xticks, ylabel, ylim, yticks, hlines, savefig, show, subplots_adjust, get_current_fig_manager
import matplotlib.dates as mdates
from datetime import datetime

# func to plot lines of nominal voltages
def plot_standart_voltage (min_x, max_x, nominal_voltage=220, margin = 0.1):
    standart_voltages = [nominal_voltage*(1-margin), nominal_voltage, nominal_voltage*(1+margin)]
    for voltage in standart_voltages:
        hlines(voltage, min_x, max_x, linestyle='--', color = 'orangered')

# func to decorate and plot graph
def graph_decoration(min_x, max_x, data_type = "dict", plot_standart = True, fname = None):
    # plot graph of standart voltage
    if plot_standart:
        plot_standart_voltage(min_x, max_x)
    # decoration
    grid(True, linestyle='-', color='0.75')
    # Х axis
    if (data_type == "dict"):
        xlabel("Часы", size = 'x-large')
        gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))   # format ticks 
        gca().xaxis.set_major_locator(mdates.HourLocator(interval = 1))  # interval of ticks - 1 hour
        global data
        title("Данные о напряжении за " + str(len(data)) + ' дней', size ='xx-large')   
    else:   #for raw data
        xlabel("Дата", size = 'x-large')
        gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%y %H:%M'))   # format ticks
        gca().xaxis.set_major_locator(mdates.DayLocator(interval = 1))  # interval of ticks - 1 day
        title("Данные о напряжении за период: " +  
            datetime.strftime(min(file_dates), "%d/%m/%Y") + ' - ' +  # first date from file
            datetime.strftime(max(file_dates), "%d/%m/%Y"), size ='xx-large')   # last date from file
    gcf().autofmt_xdate()
    xticks(ha ='center', rotation=60)  
    xlim(min_x, max_x)
    # Y axis
    ylabel("Напряжение в сети, В", size ='x-large')
    yticks( np.arange(195, 245, 1), rotation='horizontal')
    ylim(195, 245)
    # saving file
    if (fname): # if name != None
        subplots_adjust(left=0.01, bottom=0.07, right=0.99, top=0.97)  
        figure = gcf() # choose current graph
        if (data_type == "dict"):
            fig_size = 40
        else:
            fig_size = len(x_dates)/6
        figure.set_size_inches(fig_size, 20) 
        savefig(os.path.join(CHART_DIR, fname), dpi = 72) 
    # adjust and fullscreen
    subplots_adjust(left=0.04, bottom=0.12, right=0.99, top=0.97)
    get_current_fig_manager().full_screen_toggle() # (f on keyboard)
    show()

# func to plot graph from 2 lists
def plot_raw_data(x, y, plot_standart = True, fname = None):
    clf()
    min_x = min(x)
    max_x = max(x)
    # plot graph from real line voltages
    plot(x, y, linewidth=2, color='seagreen', linestyle='-', marker='.')
    graph_decoration(min_x, max_x, None, plot_standart, fname)

# func to plot graph from dictionary
def plot_data(data, plot_standart = True, fname = None):
    clf()
    min_x = 737519
    max_x = min_x+1
    colors = ['b','g','r','c','m','y','k','orange', 'seagreen', 'purple']
    #plot original data
    for i, key in enumerate(data.keys()):
        plot(data[key][0]+min_x, data[key][1], linewidth=2, color=colors[i%10], linestyle=':', marker='.')
    # calculate and plot averaged data
    average_data(data, min_points = 24*6)
    plot(data["Average"][0]+min_x, data["Average"][1], linewidth=2, color='black', linestyle='-')
    graph_decoration(min_x, max_x, "dict", plot_standart, fname)

#function to made dict (key -> date, info -> lists with points of this date)
def make_dict (raw_x, y):
    x = mdates.num2date(raw_x)
    current_day = 0
    current_month = 0
    dict = {}
    for i, date in enumerate(x):
        if (date.day != current_day) or (date.month != current_month):
            current_day = date.day
            current_month = date.month
            current_x = np.array([mdates.date2num(x) for x in x if (x.day == current_day and x.month == current_month)])
            current_x -= min(current_x)
            dict[int(mdates.date2num(date))] = [current_x, np.array(y[i: i+len(current_x)]) ]
    return dict

#function to delete unappropriate data from dict
def delete_partial_data(dict, min_points=144):
    dates_to_delete = []
    for key in dict.keys():   
        if (len(dict[key][0]) < min_points):
            try:
                dates_to_delete.append(key) 
            except KeyError:
                print("Key not found")  
    [dict.pop(date, None) for date in dates_to_delete]
    return dict

# function to find averaged data
def average_data (data_dict, min_points = 144):
    avg_x = np.zeros(min_points)
    avg_y = np.zeros(min_points)
    for i in range(min_points):    
        for key in data_dict.keys():
            avg_x[i] += data_dict[key][0][i]
            avg_y[i] += data_dict[key][1][i]
    avg_x/=len(data_dict)
    avg_y/=len(data_dict)
    data_dict["Average"] = [avg_x, avg_y]

#parce data from txt -> 0 column - dates, 3 column - Line Voltage
file_dates, y_prices = np.loadtxt(
            os.path.join(DATA_DIR, 'Datalog_28_04_2020.txt'),
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
#make a dict from data -> keys are dates, col[0] -> x (time), col[1] -> voltage at moment x
data = make_dict (x_dates, y)

if (False):
    print(data.keys()) #dict_keys
    for key in data.keys():
        print(datetime.strftime(mdates.num2date(key), "%d/%m/%Y"), " -> ", len(data[key][0]), "data points")


data = delete_partial_data(data, min_points=24*60/10)    # sampling each 10 minutes
# output
file_name = None # "all.png"
#plot_raw_data(x_dates, y, plot_standart = True, fname = file_name)
plot_data(data, plot_standart = True, fname = file_name)