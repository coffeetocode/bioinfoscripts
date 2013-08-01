from matplotlib.figure import Figure                       
from matplotlib.axes import Axes                           
from matplotlib.lines import Line2D                        
from matplotlib.backends.backend_agg import FigureCanvasAgg

fig = Figure(figsize=[4,4])                                
ax = Axes(fig, [.1,.1,.8,.8])                              
fig.add_axes(ax)                                           
l = Line2D([0,1],[0,1])                                    
ax.add_line(Line2D([0,.5],[0,.7]))

canvas = FigureCanvasAgg(fig)                              
canvas.print_figure("line_ex.png")                         
 