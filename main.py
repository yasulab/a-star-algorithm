#!/usr/bin/env python
# -*- coding:utf-8 -*-

from optparse import OptionParser
import math
import Queue

agenda = Queue.PriorityQueue()
width = -1
height = -1
maze = []
start_loc = []
finish_loc = []
markmap = []
exploremap = []
pathmap = {}
X = 0
Y = 1
COST = 0
LOC = 1
DEBUG = False
heuristic_type = ""

def read_file(filename):
    input = open(filename, "r")
    return input.read()

def save_file(file):
    fd = open("./output.txt", "w")
    fd.write(file)
    fd.close

def set_maze(filename):
    global width, height, start_loc, finish_loc
    lines = read_file(filename).splitlines()
    # tmpMaze = []
    for i,line in enumerate(lines):
        line = line.rstrip(" ")
        if i == 0:
            chars = line.split(" ")
            if len(chars) != 2:
                print "First line of input should be 2 numbers separated by space."
                exit()
            width = int(chars[0])
            height = int(chars[1])
            continue

        """ Ignore texts after inputting maze. """
        if i > height:
            continue

        if len(line) != width:
            print "The following line is not equal to the given width."
            print line
            exit()
            
        tmpList = []        
        for j,char in enumerate(line):
            tmpList.append(char)
            if char == 'o':
                start_loc = (j, (i-1))
            elif char == '*':
                finish_loc = (j, (i-1))
        maze.append(tmpList)

        """
    for y, lines in enumerate(tmpMaze):
        tmpLine = []
        for x,char in enumerate(lines):
            print "[x="+str(x)+", y="+str(y)+"]"
            tmpLine.append(tmpMaze[y][x])
        maze.append(tmpLine)
        """              
def get_item_from_maze(loc):
    return maze[loc[Y]][loc[X]]

def set_item_into_maze(loc, item):
    maze[loc[Y]][loc[X]] = item
    
def print_maze():
    for m in maze:
        for char in m:
            if len(char) == 1:
                print " "+char,
            else:
                print char,
        print

def test_pq():
    pq = Queue.PriorityQueue()
    pq.put((0, (2,4)))
    pq.put((0, (1,2)))
    pq.put((0, (3,6)))
    while not pq.empty():
        print pq.get(),
    print

def print_agenda():
    elements = []
    i = 0
    if VFLAG:
        print "\tPriority Queue:"
    while not agenda.empty():
        element = agenda.get()
        elements.append(element)
        if VFLAG:
            print '\t\t' + str(i) + ": " + str(element[LOC]) + " with " + str(element[COST]) + " cost."
        i += 1
    for elem in elements:
        agenda.put(elem)    
    
def zero_heuristic(loc):
    return 0

def manhattan_heuristic(loc):
    x1 = abs(start_loc[X] - loc[X])
    y1 = abs(start_loc[Y] - loc[Y])
    s = x1 + y1
    x2 = abs(finish_loc[X] - loc[X])
    y2 = abs(finish_loc[Y] - loc[Y])
    f = x2 + y2
    return s+f

def euclidean_heuristic(loc):
    x1 = abs(start_loc[X] - loc[X])
    y1 = abs(start_loc[Y] - loc[Y])
    s = math.sqrt((x1**2 + y1**2))
    x2 = abs(finish_loc[X] - loc[X])
    y2 = abs(finish_loc[Y] - loc[Y])
    f = math.sqrt((x2**2 + y2**2))
    return s+f

def get_mark_from_markmap(loc):
    return markmap[loc[Y]][loc[X]]

def is_loc_marked(loc):
    return get_mark_from_markmap(loc)

def is_loc_wall(loc):
    if get_item_from_maze(loc) == '#':
        return True
    else:
        return False
    
def put_child_into_agenda(cost, loc):
    mark(loc)
    agenda.put((cost, loc))
    if VFLAG:
        print '\t' + str(loc) + " is put into agenda." # with "+ str(cost) +" cost."

def calc_heuristic(loc):
    if heuristic_type == "zero":
        return zero_heuristic(loc)
    elif heuristic_type == "manhattan":
        return manhattan_heuristic(loc)
    elif heuristic_type == "euclidean":
        return euclidean_heuristic(loc)
    else:
        print "Error: unknown heuristic type is found: " + heuristic_type
        exit()
        
def get_children(loc):
    children = []
    new_locs = []
    new_locs.append((loc[X], loc[Y]-1))
    new_locs.append((loc[X]-1, loc[Y]))
    new_locs.append((loc[X]+1, loc[Y]))
    new_locs.append((loc[X], loc[Y]+1))
    for loc in new_locs:
        if 0 <= loc[X] and loc[X] < width:
            if 0 <= loc[Y] and loc[Y] < height:
                if is_loc_marked(loc): continue
                if is_loc_wall(loc): continue
                children.append(loc)
    return children

def explore_maze():
    global markmap
    put_child_into_agenda(0, start_loc)
    i = 0
    while not agenda.empty():
        raw_input("\n" + str(i)+" Turn: (Hit ENTER to explore next)")
        loc = agenda.get()[LOC]
        if VFLAG:
            print "\texploring -> " + str(loc)
        children = get_children(loc)
        store_node_link_on_pathmap(children, loc)
        if get_item_from_maze(loc) == '*':
            print "Found the goal!\n"
            show_exploremap()
            return
        
        for child in children:            
            cost = calc_heuristic(child)
            put_child_into_agenda(cost, child)
            
        print_agenda()
        #print_markmap()
        i += 1
        show_exploremap()
    print
    print "There is no path exists."
    exit()

def mark(loc):
    global markmap
    markmap[loc[Y]][loc[X]] = True
        
def set_markmap():
    for y in range(height):
        tmpList = []
        for x in range(width):
            tmpList.append(False)
        markmap.append(tmpList)
        #print tmpList

def print_markmap():
    for lines in markmap:
        for bln in lines:
            if bln == True:
                print " M",
            else:
                print " .",
        print
    print

def store_node_link_on_pathmap(children, parent):
    global exploremap
    exploremap.append(parent)
    global pathmap
    for child in children:
        pathmap[child] = parent
        #print "node link: " + str(child)+"->"+str(pathmap[child])

def show_exploremap():
    for i,loc in enumerate(exploremap):
        set_item_into_maze(loc, str(i))
    print_maze()
    for i,loc in enumerate(exploremap):
        set_item_into_maze(loc, '.')

def is_adjacent_start(loc):
    x = abs(start_loc[X] - loc[X])
    y = abs(start_loc[Y] - loc[Y])
    if x+y == 1:
        True
    else:
        False
    
def print_shortest_path():
    set_item_into_maze(finish_loc, '*')
    child = pathmap[finish_loc]
    while not child == start_loc:
        set_item_into_maze(child, 'x')
        #print "node link: " + str(child)+"->"+str(pathmap[child])
        child = pathmap[child]
    set_item_into_maze(start_loc, 'o')
    print_maze()    

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option(
        "-f", "--file", 
        type="string",
        default="mazes/sample",
        help="choose a formatted text file for creating a maze. This program uses 'mazes/sample' by default."
        )
    parser.add_option(
        "-H",
        type="choice",
        choices=["zero", "manhattan", "euclidean"],
        dest="heuristic_type",
        default="zero",
        metavar="HEURISTIC_FUNC",
        help="choose a heuristic function for A* algorithm from 'zero', 'manhattan', 'euclidean'. This program uses 'zero' by default."
        )
    parser.add_option(
        "-v", "--verbose",
        action="store_true",
        default=False,
        help="display information verbosely."
        )
    (options, args) = parser.parse_args() 
    heuristic_type = options.heuristic_type
    filename = options.file
    VFLAG = options.verbose
    
    set_maze(filename)
    print "Given maze:"
    print_maze()
    if VFLAG:
        print "width="+str(width)+", height="+str(height)
        print "start: x=" + str(start_loc[0]) + ", y="+ str(start_loc[1])
        print "finish: x=" + str(finish_loc[0]) + ", y="+ str(finish_loc[1])
    set_markmap()
    explore_maze()
    print
    print "SHOTEST PATH:"
    print_shortest_path()
    print
        
        

    

    
