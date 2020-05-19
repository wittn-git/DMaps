from tkinter import Tk
import json
import matplotlib.pyplot as plt 
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
    plt.show()

data = get_countries()
polygons = get_polygons(data)
plot_polygons(polygons)

root = Tk()
root.attributes('-zoomed', True)
#root.mainloop()