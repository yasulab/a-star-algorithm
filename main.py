#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import re
import Queue

agenda = Queue.PriorityQueue()
width = -1
height = -1
maze = []
start_loc = []
finish_loc = []
markmap = []
pathmap = []
X = 0
Y = 1
COST = 0
LOC = 1
DEBUG = False

def read_file(filename):
    input = open(filename, "r")
    return input.read()

def read_file_as_list(filename):
    input = open(filename, "r")
    return input.read().splitlines()

def save_file(file):
    fd = open("./output.txt", "w")
    fd.write(file)
    fd.close

def error(msg):
    print msg
    exit()

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
    while not agenda.empty():
        element = agenda.get()
        elements.append(element)
        print str(i) + ": " + str(element[LOC]) + " with " + str(element[COST]) + " cost."
        i += 1
    for elem in elements:
        agenda.put(elem)    
    
def zero_heuristic(location):
    return 0

def get_mark_from_markmap(loc):
    return markmap[loc[Y]][loc[X]]

def is_loc_marked(loc):
    return get_mark_from_markmap(loc)

def is_loc_wall(loc):
    if get_item_from_maze(loc) == '#':
        return True
    else:
        return False
    
def put_loc_into_agenda(cost, loc):
    mark(loc)
    agenda.put((cost, loc))
    print str(loc) + " is put into agenda with "+ str(cost) +" cost."
    
def put_around_locs_into_agenda(loc):
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
                cost = zero_heuristic(loc)
                put_loc_into_agenda(cost, loc)

def explore_maze():
    global markmap
    put_loc_into_agenda(0, start_loc)
    i = 0
    while not agenda.empty():
        raw_input("\n" + str(i)+" Turn: (Hit ENTER to explore next)")
        loc = agenda.get()[LOC]
        store_loc_on_pathmap(loc)
        print "exploring -> " + str(loc)
        if get_item_from_maze(loc) == '*':
            print "found the goal!\n"
            show_pathmap()
            return
        put_around_locs_into_agenda(loc)
        print_agenda()
        print_markmap()
        i += 1
        show_pathmap()
    print
    print "There is no way to reach the goal state."
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
        print lines

def store_loc_on_pathmap(loc):
    global pathmap
    #child = get_next_node(agenda)
    #path = (child, parent)
    pathmap.append(loc)

def show_pathmap():
    for i,loc in enumerate(pathmap):
        set_item_into_maze(loc, str(i))
    print_maze()
    for i,loc in enumerate(pathmap):
        set_item_into_maze(loc, '.')

    

if __name__ == "__main__":
    set_maze("./input.txt")
    print "Given:"
    print_maze()
    print "width="+str(width)+", height="+str(height)
    print "start: x=" + str(start_loc[0]) + ", y="+ str(start_loc[1])
    print "finish: x=" + str(finish_loc[0]) + ", y="+ str(finish_loc[1])
    set_markmap()
    explore_maze()
        
        

    

    