# Horribly ugly test code to make DNA walks from basepair sequences
# (c) Patrick Thomas
# pst@coffeetocode.net

# Released under the WTFPL 
#(Though it would be nice to let me know if you use this anywhere interesting)

from matplotlib.figure import Figure                       
from matplotlib.axes import Axes                           
from matplotlib.lines import Line2D                        
from matplotlib.backends.backend_agg import FigureCanvasAgg

import dna_walk_utils as walk
import random


size_in_inches = [8, 8] #width, height
fig = Figure(figsize=size_in_inches)
ax = Axes(fig, [.1,.1,.8,.8])
fig.add_axes(ax)

bases = walk.TEST_SEQUENCES["Acinetobacter_calcoaceticus"]
bases2 = walk.TEST_SEQUENCES["A.israelii"]

for samplename in walk.TEST_SEQUENCES.keys():
    bases = walk.TEST_SEQUENCES[samplename]
    print "Walking", samplename
    clr = random.choice("bgrcmyk")
    def on_window(from_loc, to_loc):
        ax.add_line(Line2D([from_loc.x, to_loc.x],[from_loc.y, to_loc.y], color=clr))
    walk.do_line_walk(bases, 4, on_window, )

ax.relim()
ax.axis('tight')
ax.set_title('DNA Walk of "All Seqs.fasta"\n(16S Example Set)')

canvas = FigureCanvasAgg(fig)
canvas.print_figure("dna_walk.png")                 
 

