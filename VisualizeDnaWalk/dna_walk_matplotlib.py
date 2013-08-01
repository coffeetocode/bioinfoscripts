import numpy as np 
import matplotlib.pyplot as plt

nrows, ncols = 700, 700
window = 10

#start with a black grid
grid = np.zeros((nrows, ncols), dtype=np.int)

fasta_seq = r""">Acinetobacter_calcoaceticus
CTCAGATTGAACGCTGGCGGCAGGCTTAACACATGCAAGTCGAGCGGAGTGATGGTGCTTGCACTATCAC
TTAGCGGCGGACGGGTGAGTAATGCTTAGGAATCTGCCTATTAGTGGGGGACAACATTTCGAAAGGAATG
CTAATACCGCATACGTCCTACGGGAGAAAGCAGGGGATCTTCGGACCTTGCGCTAATAGATGAGCCTAAG
TCGGATTAGCTAGTTGGTGGGGTAAAGGCCTACCAAGGCGACGATCTGTAGCGGGTCTGAGAGGATGATC
CGCCACACTGGGACTGAGACACGGCCCAGACTCCTACGGGAGGCAGCAGTGGGGAATATTGGACAATGGG
CGCAAGCCTGATCCAGCCATGCCGCGTGTGTGAAGAAGGCCTTATGGTTGTAAAGCACTTTAAGCGAGGA
GGAGGCTACTGAAGTTAATACCTTCAGATAGTGGACGTTACTCGCAGAATAAGCACCGGCTAACTCTGTG
CCAGCAGCCGCGGTAATACAGAGGGTGCAAGCGTTAATCGGATTTACTGGGCGTAAAGCGCGCGTAGGCG
GCTAATTAAGTCAAATGTGAAATCCCCGAGCTTAACTTGGGAATTGCATTCGATACTGGTTAGCTAGAGT
GTGGGAGAGGATGGTAGAATTCCAGGTGTAGCGGTGAAATGCGTAGAGATCTGGAGGAATACCGATGGCG
AAGGCAGCCATCTGGCCTAACACTGACGCTGAGGTGCGAAAGCATGGGGAGCAAACAGGATTAGATACCC
TGGTAGTCCATGCCGTAAACGATGTCTACTAGCCGTTGGGGCCTTTGAGGCTTTAGTGGCGCAGCTAACG
CGATAAGTAGACCGCCTGGGGAGTACGGTCGCAAGACTAAAACTCAAATGAATTGACGGGGGCCCGCACA
AGCGGTGGAGCATGTGGTTTAATTCGATGCAACGCGAAGAACCTTACCTGGCCTTGACATAGTAAGAACT
TTCCAGAGATGGATTGGTGCCTTCGGGAACTTACATACAGGTGCTGCATGGCTGTCGTCAGCTCGTGTCG
TGAGATGTTGGGTTAAGTCCCGCAACGAGCGCAACCCTTTTCCTTATTTGCCAGCGAGTAATGTCGGGAA
CTTTAAGGATACTGCCAGTGACAAACTGGAGGAAGGCGGGGACGACGTCAAGTCATCATGGCCCTTACGG
CCAGGGCTACACACGTGCTACAATGGTCGGTACAAAGGGTTGCTACCTAGCGATAGGATGCTAATCTCAA
AAAGCCGATCGTAGTCCGGATTGGAGTCTGCAACTCGACTCCATGAAGTCGGAATCGCTAGTAATCGCGG
ATCAGAATGCCGCGGTGAATACGTTCCCGGGCCTTGTACACACCGCCCGTCACACCATGGGAGTTTGTTG
CACCAGAAGTAGGTAGTCTAACCGCAAGGAGGACGCTTACCACGGTGTGGCCGATGACTGGGGTGAAGTC
GTAACAAGGTAGCCGTAGGGGAACCTGCGGCTGGATCACCT
"""

bases = "".join(fasta_seq.split()[1:])

class Location:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def __str__(self):
        return str((self.x, self.y))

loc = Location(0, 0)

def left(loc):
    loc.x -= 1

def right(loc):
    loc.x += 1

def up(loc):
    loc.y += 1

def down(loc):
    loc.y -= 1

base_direction_mapping = {"G" : left, "T" : up, "A" : down, "C" : right}


x_min, x_max, y_min, y_max = 0, 0, 0, 0
for index, base in enumerate(bases):
    direction = base_direction_mapping[base]
    direction(loc)
    print loc, direction.__name__
    x_max = max(x_max, loc.x)
    x_min = min(x_min, loc.x)
    y_max = max(y_max, loc.y)
    y_min = min(y_min, loc.y)
    if not (index % window):
        grid[loc.x, loc.y] = 10

#    for i in range(5):
#        direction(loc)
#        print loc, direction.__name__
#        x_max = max(x_max, loc.x)
#        x_min = min(x_min, loc.x)
#        y_max = max(y_max, loc.y)
#        y_min = min(y_min, loc.y)
#        grid[loc.x, loc.y] = 10
    


    
#print """
#   %3d
#%3d   %3d
#   %3d
#""" % (y_max, x_min, x_max, y_min)




# And now we plot it:
plt.imshow(grid, interpolation='none', 
        extent=(x_min, x_max, y_max, y_min))

plt.show()



quit()


"""
#From matplotlib docs: http://matplotlib.sourceforge.net/examples/pylab_examples/colorbar_tick_labelling_demo.html

import matplotlib.pyplot as plt
import numpy as np

from numpy.random import randn

# Make plot with vertical (default) colorbar
fig = plt.figure()
ax = fig.add_subplot(111)

data = np.clip(randn(250, 250), -1, 1)

cax = ax.imshow(data, interpolation='nearest')
ax.set_title('Gaussian noise with vertical colorbar')
plt.show()

"""


"""
#From stackoverflow question: http://stackoverflow.com/questions/6318170/large-matplotlib-pixel-figure-best-approach

import numpy as np
import matplotlib.pyplot as plt

nrows, ncols = 1000, 1000
z = 500 * np.random.random(nrows * ncols).reshape((nrows, ncols))

plt.imshow(z, interpolation='nearest')
plt.colorbar()
plt.show()
"""



"""
#From same question:
import numpy as np 
import matplotlib.pyplot as plt

# Generate some data
nrows, ncols = 1000, 1000
xmin, xmax = -32.4, 42.0
ymin, ymax = 78.9, 101.3

dx = (xmax - xmin) / (ncols - 1)
dy = (ymax - ymin) / (ncols - 1)

x = np.linspace(xmin, xmax, ncols)
y = np.linspace(ymin, ymax, nrows)
x, y = np.meshgrid(x, y)

z = np.hypot(x - x.mean(), y - y.mean())
x, y, z = [item.flatten() for item in (x,y,z)]

# Scramble the order of the points so that we can't just simply reshape z
indicies = np.arange(x.size)
np.random.shuffle(indicies)
x, y, z = [item[indicies] for item in (x, y, z)]

# Up until now we've just been generating data...
# Now, x, y, and z probably represent something like you have.

# We need to make a regular grid out of our shuffled x, y, z indicies.
# To do this, we have to know the cellsize (dx & dy) that the grid is on and
# the number of rows and columns in the grid. 

# First we convert our x and y positions to indicies...
idx = np.round((x - x.min()) / dx).astype(np.int)
idy = np.round((y - y.min()) / dy).astype(np.int)

# Then we make an empty 2D grid...
grid = np.zeros((nrows, ncols), dtype=np.float)

# Then we fill the grid with our values:
grid[idy, idx] = z

# And now we plot it:
plt.imshow(grid, interpolation='nearest', 
        extent=(x.min(), x.max(), y.max(), y.min()))
plt.colorbar()
plt.show()
"""