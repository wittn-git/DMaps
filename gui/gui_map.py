import json
from tkinter import Tk, Frame, Button
import tkinter
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from descartes import PolygonPatch

root = tkinter.Tk()
root.wm_title("DMaps")
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))

class MapFigure:
    def __init__(self, size):
        self.countries = self.get_countries()
        self.figure = self.create_figure()

    def get_countries(self):
        file = open('../data/countries.json')
        file_content = file.read()
        return json.loads(file_content)

    def create_polygons(self):
        color_red, color_blue = '#FF4040', '#6699cc'
        polygons = []
        for key in self.countries:
            current_color = color_blue
            if self.countries[key]['visited'] == 'true': 
                current_color = color_red
            if self.countries[key]['hovered'] == 'true': 
                current_color = color_red
            polygon = self.create_polygon(self.countries[key]['geometry'], current_color)
            polygons.append(polygon)
        return polygons
    
    def create_polygon(self, geometry, current_color):
        return PolygonPatch(geometry, fc=current_color, ec=current_color, alpha=0.5)

    def get_figure(self):
        return self.figure

    def create_figure(self): 
        polygons = self.create_polygons()
        try:
            self.figure.clf()
            fig = self.figure
        except:
            fig = plt.figure()
        ax = fig.gca() 
        for polygon_patch in polygons:
            ax.add_patch(polygon_patch)
        ax.axis('scaled')
        plt.axis('off')
        fig.add_axes(ax)
        fig.subplots_adjust(left=-0.04, bottom=-0.23, right=1.04, top=1.2, wspace=0, hspace=0)
        return fig

    def refresh(self, point):
        for key in self.countries:
            polygon = self.create_polygon(self.countries[key]['geometry'], '#6699cc')
            if polygon.contains_point(point):
                self.countries[key]['hovered'] = 'true'
            else:
                self.countries[key]['hovered'] = 'false'
        self.figure = self.create_figure()

class Canvas:
    def __init__(self, parent):
        self.map_figure = MapFigure((w, h))
        self.figure = self.map_figure.get_figure()
        self.canvas = FigureCanvasTkAgg(self.figure, master=parent)
        self.canvas.get_tk_widget().config(width=w,height=h)
        #self.canvas.get_tk_widget().pack(fill='both', expand=True)
        self.canvas.get_tk_widget().pack()
        self.canvas.draw()

    def refresh(self, parent, point):
        self.map_figure.refresh(point)
        self.canvas.figure = self.map_figure.get_figure()
        self.canvas.draw()

    def get_size(self):
        return self.canvas.get_width_height()
            
def motion(event):
    x_gap, y_gap = w-canvas.get_size()[0], h-canvas.get_size()[1]
    x, y = event.x-x_gap, event.y-y_gap
    canvas.refresh(root, (x, y))

canvas = Canvas(root)
root.bind('<Motion>', motion)
root.mainloop()