# Horribly ugly test code to make DNA walks from basepair sequences
# (c) Patrick Thomas
# pst@coffeetocode.net

# Released under the WTFPL 
#(Though it would be nice to let me know if you use this anywhere interesting)


lines = open("All seqs.fasta").readlines()

#name:bases
TEST_SEQUENCES = {}

name = None
bases = ""
for line in lines:
    if line.startswith(">"):
        if name: #store the previous one before we start the new one
            TEST_SEQUENCES[name] = bases
            bases = ""
        name = line.strip(">").strip()
    elif not line.isspace() and len(line) != 0:
        bases += line.strip().upper().replace("N", "").replace(" ", "").replace("R", "").replace("Y", "").replace("K", "").replace("S", "")

if name: #store the final one
    TEST_SEQUENCES[name] = bases


TEST_BASES_1 = TEST_SEQUENCES["Acinetobacter_calcoaceticus"]
TEST_BASES_2 = TEST_SEQUENCES["A.israelii"]


class Location:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def __str__(self):
        return str((self.x, self.y))


def left(loc):
    loc.x -= 1

def right(loc):
    loc.x += 1

def up(loc):
    loc.y += 1

def down(loc):
    loc.y -= 1

base_direction_mapping = {"G" : left, "T" : up, "A" : down, "C" : right}

def do_walk(bases, window, on_window):
    x_min, x_max, y_min, y_max = 0, 0, 0, 0
    for index, base in enumerate(bases):
        direction = base_direction_mapping[base]
        for i in range(5):
            direction(loc)
            print loc, direction.__name__
            x_max = max(x_max, loc.x)
            x_min = min(x_min, loc.x)
            y_max = max(y_max, loc.y)
            y_min = min(y_min, loc.y)
            #grid[loc.x, loc.y] = 10
            if not (index % window):
                img.putpixel((loc.x, loc.y), (0, 0, 255))    

def do_line_walk(bases, window, on_window, on_base=None):
    x_min, x_max, y_min, y_max = 0, 0, 0, 0
    real_loc = Location(0.0, 0.0)
    window_loc = Location(0.0, 0.0)
    
    for index, base in enumerate(bases):
        direction = base_direction_mapping[base]
        direction(real_loc)
        if on_base:
            on_base(real_loc, direction.__name__)
        x_max = max(x_max, real_loc.x)
        x_min = min(x_min, real_loc.x)
        y_max = max(y_max, real_loc.y)
        y_min = min(y_min, real_loc.y)
        if not (index % window):
            on_window(window_loc, real_loc)
            window_loc = real_loc
            real_loc = Location(real_loc.x, real_loc.y)

    return (x_min, x_max, y_min, y_max)