from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot
from matplotlib.colors import LightSource
import numpy

def prepare_STL():
    figure = pyplot.figure()
    axes = figure.add_subplot(projection='3d')

    # Load the STL files and add the vectors to the plot
    your_mesh = mesh.Mesh.from_file('Output\output.stl') # todo: load and update actual STL file
    axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))
    polymesh = mplot3d.art3d.Poly3DCollection(your_mesh.vectors)

    # Auto scale to the mesh size
    scale = your_mesh.points.flatten()
    axes.auto_scale_xyz(scale,scale,scale)

    ls = LightSource(azdeg=225, altdeg=45)
    # Darkest shadowed surface, in rgba
    dk = numpy.array([0.2, 0.0, 0.0, 1])
    # Brightest lit surface, in rgba
    lt = numpy.array([0.7, 0.7, 1.0, 1])
    # Interpolate between the two, based on face normal
    shade = lambda s: (lt-dk) * s + dk

    # Set face colors 
    sns = ls.shade_normals(your_mesh.get_unit_normals(), fraction=1.0)
    rgba = numpy.array([shade(s) for s in sns])
    polymesh.set_facecolor(rgba)

    axes.add_collection3d(polymesh)

    return figure

def draw_STL(canvas, fig):
    if canvas.children:
        for child in canvas.winfo_children():
            child.destroy()
    figure_canvas_agg = FigureCanvasTkAgg(fig, master=canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='right', fill='both', expand=1)