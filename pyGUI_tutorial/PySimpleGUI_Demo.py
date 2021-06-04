# Basic Structure from--
#     https://github.com/PySimpleGUI/PySimpleGUI/blob/master/PySimpleGUIWeb/Demo%20Programs/Web_Matplotlib_Browser.py

# For this demo, make sure you have all of the imports. They should all be in Anaconda, except PySimpleGUIWeb and remi
# Also make sure 747.jpeg and 777.jpeg are in the directory specified by dir (relaive path)

# Just execute 'python PySimpleGUI_Demo.py' in the command line to run

import PySimpleGUIWeb as sg
import remi

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasAgg
import matplotlib.figure
import io
import inspect

import time
import matplotlib.image as img
import os.path as osp


# Put any saved images here
dir= './'


# Functions used in main() ----

# Animated Plots:
def PlotRandomUniform(ax):
    ax.set_ylim([-0.1,1.1])
    ax.set_title('30 Random Uniformly Distributed Numbers')
    ax.scatter(np.arange(30), np.random.rand(30))
    ax.set_aspect(aspect=6.0)
    return

def PlotRandomNormal(ax):
    ax.scatter(np.arange(30), np.random.randn(30))
    ax.set_ylim([-4,4])
    ax.set_title('30 Random Normally Distributed Numbers')
    ax.set_aspect(aspect=3.0)
    return

def WavySine(ax):
    ar= np.arange(0,15,0.01)
    ax.plot(ar, np.sin(ar-time.time()))
    ax.set_aspect(aspect=3.0)
    ax.axis('off')
    return

# Displaying pre-saved images:
def b747(ax):
    if not osp.exists(dir + '747.jpeg'):
        print('Oops. There is no 747.jpeg image in the target directory. Failing...')
        return
    im= img.imread(dir + '747.jpeg', format='jpeg')
    ax.imshow(im)
    ax.axis('off')
    return

def b777(ax):
    if not osp.exists(dir + '777.jpeg'):
        print('Oops. There is no 777.jpeg image in the target directory. Failing...')
    im= img.imread(dir + '777.jpeg', format='jpeg')
    ax.imshow(im)
    ax.axis('off')
    return


# ---------------------------- Beginning of PySimpleGUI program ----------------------------

# ---------------------------- draw_figure (the helper function) ----------------------------
def draw_figure(func, element, fig, ax):
    """
    Draws the previously created "figure" in the supplied Image Element
    :param func: a function that returns a Matplotlib figure
    :param element: an Image Element
    :return: The figure canvas
    """
    # Using ax.clear() or plt.cla() is NECESSARY -- otherwise the memory goes bananas
    #plt.cla()            # erases previously drawn plots
    ax.clear()            # does the same thing as plt.cla()

    func(ax)
    canv = FigureCanvasAgg(fig)
    buf = io.BytesIO()
    canv.print_figure(buf, format='png')
    if buf is None:
        return None
    buf.seek(0)
    element.update(data=buf.read())
    return canv


# -------------------------------- GUI Starts Here -------------------------------#
def main():

    # Create a Figure and Axes at the beginning, and redraw it as necessary
    fig, ax= plt.subplots(figsize = (7,5))

    fig_dict = {'PlotRandomUniform': PlotRandomUniform, 'PlotRandomNormal': PlotRandomNormal, 
                'b747':b747, 'b777':b777, 'WavySine':WavySine}

    # define the layout -- very easy with PySimpleGUI because it's just a 2d array of blocks

    col_listbox = [[sg.Listbox(values=fig_dict.keys(), enable_events=True, size=(25, len(fig_dict.keys())), key='-LISTBOX-')],
                   [sg.Exit(size=(5, 2))]]

    layout = [[sg.Text('Matplotlib Plot Browser', font=('current 25'))],
              [sg.Text('Choose a plot from the list to see the plot and the source code used to make it.')],
              [sg.Column(col_listbox, element_justification='c'), sg.Image(key='-IMAGE-'),
               sg.Multiline(size=(40, 20), font='Courier 12', key='-MULTILINE-')], ]

    # create the window
    window = sg.Window('Embedding Matplotlib In PySimpleGUIWeb', layout)
    
    # Initial plot
    choice= 'b747'
    the_plotting_func = fig_dict[choice]  # get function to call from the dictionary
    window['-MULTILINE-'].Widget= remi.gui.TextInput() # prevent updating a NoneType
    window['-MULTILINE-'].update(inspect.getsource(the_plotting_func))

    while True:  # The event loop
        
        # the timeout enables image refreshing (i.g. live plotting)
        # It can be kind of slow though depending on what's being plotted
        event, values = window.read(timeout=1)
    
        if event in (sg.WIN_CLOSED, 'Exit'):  # if user closed window or clicked Exit button
            break

        # If no new button has been pressed:
        if event == '__TIMEOUT__' or values['-LISTBOX-'][0] == None:
            draw_figure(the_plotting_func, window['-IMAGE-'], fig, ax)
            continue

        # If a button has been pressed
        else:
            # If it's a new button
            if values['-LISTBOX-'][0] != choice:
                choice = values['-LISTBOX-'][0]  # get first listbox item chosen (returned as a list)
                the_plotting_func = fig_dict[choice]  # get function to call from the dictionary
                window['-MULTILINE-'].update(inspect.getsource(the_plotting_func))  # show source code to function in multiline

            draw_figure(the_plotting_func, window['-IMAGE-'], fig, ax)  # draw the figure

    window.close()


if __name__ == '__main__':
    main()
