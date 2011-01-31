#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import re
import Queue

agenda = Queue.PriorityQueue()
width = -1
height = -1
maze = []

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
    lines = read_file(filename).splitlines()
    for i,line in enumerate(lines):
        line = line.rstrip(" ")
        if i == 0:
            chars = line.split(" ")
            if len(chars) != 2:
                print "First line of input should be 2 numbers separated by space."
                exit()
            width = int(chars[0])
            height = int(chars[1])
            print "width: " + str(width)
            print "height: " + str(height)
            continue

        """ Ignore texts after the maze """
        if i > height:
            continue

        if len(line) != width:
            print "The following line is not equal to the given width."
            print line
            exit()
        tmpList = []
        
        for char in line:
            tmpList.append(char)
        maze.append(tmpList)

def print_maze(maze):
    print "width="+str(width)+", height="+str(height)
    print "GIVEN MAZE:"
    for m in maze:
        for char in m:
            print char,
        print

def agenda_test():
    agenda.put((2, "second"))
    agenda.put((1, "first"))
    agenda.put((3, "third"))
    while not agenda.empty():
        print agenda.get(),

def exlore_maze():
    return
if __name__ == "__main__":
    set_maze("./input.txt")
    print_maze(maze)
    agenda_test()
    
        
        

    

    
