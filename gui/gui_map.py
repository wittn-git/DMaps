import json
from tkinter import Tk, Frame, Button
import tkinter
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from descartes import PolygonPatch

def get_countries():
    file = open('../data/countries.json')
    file_content = file.read()
    return json.loads(file_content)

def get_polygons(data):
    color_red, color_blue = '#FF4040', '#6699cc'
    polygons = []
    for key in data:
         if 'geometry' in data[key]: 
            current_color = color_blue
            if data[key]['visited'] is True: current_color = color_red
            polygon = PolygonPatch(data[key]['geometry'], fc=current_color, ec=current_color, alpha=0.5)
            polygons.append(polygon)
    return polygons

def plot_polygons(polygons): 
    fig = plt.figure() 
    ax = fig.gca() 
    for polygon_patch in polygons:
        ax.add_patch(polygon_patch)
    ax.axis('scaled')
    plt.axis('off')
    fig.add_axes(ax)
    fig.subplots_adjust(left=-0.04, bottom=-0.23, right=1.04, top=1.2, wspace=0, hspace=0)
    return fig

def get_map():
    data = get_countries()
    polygons = get_polygons(data)
    return plot_polygons(polygons)

root = tkinter.Tk()
root.wm_title("DMaps")
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))

canvas = FigureCanvasTkAgg(get_map(), master=root)
canvas.draw()
canvas.get_tk_widget().pack(fill='both', expand=True)

root.mainloop()