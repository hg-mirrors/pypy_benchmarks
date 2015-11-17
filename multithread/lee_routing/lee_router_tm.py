#!/usr/bin/python

#
# BSD License
#
# Copyright (c) 2007, The University of Manchester (UK)
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#     - Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     - Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#     - Neither the name of the University of Manchester nor the names
#       of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written
#       permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Simple Lee's Routing Algorithm
# Author: IW
# Translated from Java to Python by Remi Meier


import time
import sys, math
import threading

try:
    from pypystm import atomic, hint_commit_soon
except ImportError:
    print "NOT RUNNING STM"
    atomic = threading.RLock()
    hint_commit_soon = lambda : 0

try:
    from pypystm import STMQueue, STMEmpty
except ImportError:
    from Queue import Queue as STMQueue, Empty as STMEmpty


DEBUG = True

CYAN = "#00FFFF"
MAGENTA = "#FF00FF"
YELLOW = "#FFFF00"
GREEN = "#00FF00"
RED = "#FF0000"
BLUE = "#0000FF"

GRID_SIZE = 600
EMPTY = 0
TEMP_EMPTY = 10000
OCC = 5120
VIA = 6000
BVIA = 6001
TRACK = 8192
MAX_WEIGHT = 1

# used as loop indices to look at neighbouring cells
NEIGHBOUR_OFFS = ((0,1), (1,0), (0,-1), (-1,0))

class Grid(object):

    def __init__(self, width, height, depth):
        self.width = width
        self.height = height
        self.depth = depth
        # self._data = [[[0 for _ in range(depth)]
        #              for _ in range(height)]
        #              for _ in range(width)]
        self._data = None
        self.reset(EMPTY)

    def _idx(self, x, y, z):
        return (x * self.height + y) * self.depth + z

    def __getitem__(self, args):
        #x, y, z = args
        #return self._data[x][y][z]
        return self._data[self._idx(*args)]

    def __setitem__(self, args, value):
        self._data[self._idx(*args)] = value
        # x, y, z = args
        # self._data[x][y][z] = value

    def reset(self, val):
        self._data = [val] * (self.width * self.height * self.depth)
        # for col in self._data:
        #     for r in range(len(col)):
        #         col[r] = [val] * self.depth

    def occupy(self, lo_x, lo_y, up_x, up_y):
        for x in range(lo_x, up_x + 1):
            for y in range(lo_y, up_y + 1):
                for c in range(self.depth):
                    self[x, y, c] = OCC
                # depth = self._data[x][y]
                # for c in range(len(depth)):
                #     depth[c] = OCC


    def add_weights(self):
        for i in range(MAX_WEIGHT):
            # this loop iteratively propagates weights
            # if for MAX_WEIGHT > 1...
            for z in range(self.depth):
                for x in range(1, self.width - 1):
                    for y in range(1, self.height - 1):
                        val = self[x, y, z]
                        if val == OCC:
                            # for OCC fields, we set EMPTY neighbours to
                            # MAX_WEIGHT
                            for dx, dy in NEIGHBOUR_OFFS:
                                if self[x + dx, y + dy, z] == EMPTY:
                                    self[x + dx, y + dy, z] = MAX_WEIGHT
                        elif val != EMPTY:
                            # for MAX_WEIGHT fields, set EMPTY neighbours to
                            # "our value - 1" --> 0 = EMPTY if MAX_WEIGHT is 1
                            for dx, dy in NEIGHBOUR_OFFS:
                                if self[x + dx, y + dy, z] == EMPTY:
                                    self[x + dx, y + dy, z] = val - 1





class WorkItem:
    def __init__(self, x1=0, y1=0, x2=0, y2=0, n=0):
        self.x1, self.y1, self.x2, self.y2, self.n = (
            x1, y1, x2, y2, n)

    def __cmp__(self, o):
        selfLen = ((self.x2 - self.x1) * (self.x2 - self.x1)
                   + (self.y2 - self.y1) * (self.y2 - self.y1))
        otherLen = ((o.x2 - o.x1) * (o.x2 - o.x1)
                    + (o.y2 - o.y1) * (o.y2 - o.y1))
        return cmp(selfLen, otherLen)


class WorkQueue:
    def __init__(self, items):
        self._stmQ = STMQueue()
        for i in (items):
            self._stmQ.put(i)

    def dequeue(self):
        return self._stmQ.get(0)



class LeeThread(threading.Thread):

    def __init__(self, lr):
        super(LeeThread, self).__init__()
        self.lr = lr
        self.wq = None
        self.tempgrid = Grid(GRID_SIZE, GRID_SIZE, 2)

    def run(self):
        while True:
            self.wq = self.lr.get_next_track()
            if self.wq is None:
                print "finished"
                return
            #
            #self.tempgrid = Grid(GRID_SIZE, GRID_SIZE, 2)
            self.lr.lay_next_track(self.wq, self.tempgrid)



class LeeRouter(object):

    def __init__(self, file):
        self.grid = Grid(GRID_SIZE, GRID_SIZE, 2)
        self._work = []
        self.net_no = 0
        self._parse_data_file(file)
        self.grid.add_weights()
        self._compatibility_sort(self._work)
        self.workQ = WorkQueue(self._work)
        #
        self.grid_lock = atomic#threading.Lock()
        self.view = Viewer()

    def _parse_data_file(self, file_name):
        with open(file_name, 'r') as file:
            for line in file:
                line = line.strip()
                line = line.split()
                c, params = line[0], map(int, line[1:])
                if c == 'E':
                    break # end of file
                elif c == 'C':
                    # chip bounding box
                    x0, y0, x1, y1 = params
                    self.grid.occupy(x0, y0, x1, y1)
                elif c == 'P':
                    # pad
                    x0, y0 = params
                    self.grid.occupy(x0, y0, x0, y0)
                elif c == 'J':
                    # join connection pts
                    x0, y0, x1, y1 = params
                    self.net_no += 1
                    # do what happens in Java (insert instead of append):
                    self._work.insert(0,WorkItem(x0, y0, x1, y1, self.net_no))

    @staticmethod
    def _compatibility_sort(work):
        def _pass():
            done = True
            ent = -1
            a = ent + 1
            while a + 1 < len(work):
                b = a + 1
                if work[a] > work[b]:
                    # swap a, b
                    work[a], work[b] = work[b], work[a]
                    a, b = b, a
                    assert ent == b - 1

                    done = False
                ent = a
                a = b
                b = b + 1
            return done
        #
        while not _pass():
            pass
        #print "|".join(map(lambda x:str((x.x1 - x.x2)**2+(x.y1-x.y2)**2), work[:20]))

    # @staticmethod
    # def _compatibility_sort(work):
    #     # just here for result-compatibility with Java code
    #     for passnum in range(len(work) - 1, 0, -1):
    #         for i in range(passnum):
    #             if work[i] > work[i+1]:
    #                 work[i], work[i+1] = work[i+1], work[i]
    #     #print "|".join(map(lambda x:str((x.x1 - x.x2)**2+(x.y1-x.y2)**2), work))

    def get_next_track(self):
        try:
            return self.workQ.dequeue()
        except STMEmpty:
            return None

    def lay_next_track(self, wq, tempgrid):
        # start transaction
        with self.grid_lock:
            done = self._connect(wq.x1, wq.y1, wq.x2, wq.y2,
                                wq.n, tempgrid, self.grid)
        return done # end transaction

    def create_thread(self):
        return LeeThread(self)

    @staticmethod
    def _expand_from_to(x, y, x_goal, y_goal, num,
                        tempgrid, grid):
        # this method should use Lee's expansion algorithm from
	# coordinate (x,y) to (x_goal, y_goal) for the num iterations
	# it should return true if the goal is found and false if it is not
	# reached within the number of iterations allowed.
        #
        # g[x_goal][y_goal][0] = EMPTY; // set goal as empty
	# g[x_goal][y_goal][1] = EMPTY; // set goal as empty
        front = []
        tmp_front = []
        tempgrid[x, y, 0] = 1
        tempgrid[x, y, 1] = 1
        #
        front.append((x, y, 0, 0)) # (x y z dw)
        front.append((x, y, 1, 0)) # we can start from either side
        #
        reached0, reached1 = False, False
        while front:
            while front:
                fx, fy, fz, fdw = front.pop(0)
                #
                if fdw > 0:
                    tmp_front.append((fx, fy, fz, fdw - 1))
                else:
                    for dx, dy in NEIGHBOUR_OFFS:
                        fdx, fdy = fx + dx, fy + dy

                        weight = grid[fdx, fdy, fz] + 1
                        prev_val = tempgrid[fdx, fdy, fz]
                        reached = (fdx == x_goal) and (fdy == y_goal)
                        if reached or (
                                prev_val > tempgrid[fx, fy, fz] + weight and weight < OCC):
                            # check that a point is actually within the bounds of grid array:
                            if 0 < fdx < GRID_SIZE - 1 and 0 < fdy < GRID_SIZE - 1:
                                tempgrid[fdx, fdy, fz] = tempgrid[fx, fy, fz] + weight
                                if not reached:
                                    tmp_front.append((fdx, fdy, fz, 0))
                    #
                    not_fz = 1 - fz
                    weight = grid[fx, fy, not_fz] + 1
                    if tempgrid[fx, fy, not_fz] > tempgrid[fx, fy, fz] and weight < OCC:
                        tempgrid[fx, fy, not_fz] = tempgrid[fx, fy, fz]
                        tmp_front.append((fx, fy, not_fz, 0))
                    #
                    # must check if found goal, if so, return True
                    reached0 = tempgrid[x_goal, y_goal, 0] != TEMP_EMPTY
                    reached1 = tempgrid[x_goal, y_goal, 1] != TEMP_EMPTY
                    if reached0 and reached1: # both
                        return True # (x_goal, y_goal) can be found in time
            #
            front, tmp_front = tmp_front, front
        return False

    @staticmethod
    def _path_from_other_side(tempgrid, x, y, z):
        zo = 1 - z # other side
        sqval = tempgrid[x, y, zo]
        if sqval in (VIA, BVIA):
            return False
        #
        if tempgrid[x, y, zo] <= tempgrid[x, y, z]:
            return (tempgrid[x-1, y, zo] < sqval or tempgrid[x+1, y, zo] < sqval
                    or tempgrid[x, y-1, zo] < sqval or tempgrid[x, y+1, zo] < sqval)
        return False

    @staticmethod
    def _tlength(x1, y1, x2, y2):
        sq = (x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1)
	return int(math.sqrt(float(sq)))

    def _backtrack_from(self, x_goal, y_goal, x_start, y_start,
                      track_no, tempgrid, grid):
        # this method should backtrack from the goal position (x_goal, y_goal)
	# back to the starting position (x_start, y_start) filling in the
	# grid array g with the specified track number track_no ( + TRACK).
	# ***
	# CurrentPos = Goal
	# Loop
	# Find dir to start back from current position
	# Loop
	# Keep going in current dir and Fill in track (update currentPos)
	# Until box number increases in this current dir
	# Until back at starting point
	# ***
        distsofar = 0
        if abs(x_goal - x_start) > abs(y_goal - y_start):
            z_goal = 0
        else:
            z_goal = 1
        #
        if tempgrid[x_goal, y_goal, z_goal] == TEMP_EMPTY:
            z_goal = 1 - z_goal
        #
        # arrays used for looking NSEW:
        DX = (( -1, 1, 0, 0 ),
              ( 0, 0, -1, 1 ))
        DY = (( 0, 0, -1, 1 ),
              ( -1, 1, 0, 0 ))
        #
        temp_y, temp_x, temp_z = y_goal, x_goal, z_goal
        while (temp_x != x_start) or (temp_y != y_start): # PDL: until back
            # at starting point
            advanced = False
            min_dir = 0
            min_square = 100000
            for d in range(4): # PDL: find dir to start back from
                # current position
                temp_dx, temp_dy = temp_x + DX[temp_z][d], temp_y + DY[temp_z][d]
                if (tempgrid[temp_dx, temp_dy, temp_z] < tempgrid[temp_x, temp_y, temp_z]
                    and tempgrid[temp_dx, temp_dy, temp_z] != TEMP_EMPTY):
                    if tempgrid[temp_dx, temp_dy, temp_z] < min_square:
                        min_square = tempgrid[temp_dx, temp_dy, temp_z]
                        min_dir = d
                        advanced = True
            if advanced:
                distsofar += 1
            #
            if (self._path_from_other_side(tempgrid, temp_x, temp_y, temp_z)
                # not preferred dir for this layer
                and ((min_dir > 1 and distsofar > 15
                      and self._tlength(temp_x, temp_y, x_start, y_start) > 15)
                     or (not advanced and
                         grid[temp_x, temp_y, temp_z] not in (VIA, BVIA)
                     ))):
                t_z = 1 - temp_z
                viat = VIA if advanced else BVIA # BVIA is nowhere else to go
                # mark via
                tempgrid[temp_x, temp_y, temp_z] = viat
                grid[temp_x, temp_y, temp_z] = viat
                # go to the other side:
                temp_z = t_z
                tempgrid[temp_x, temp_y, temp_z] = viat
                grid[temp_x, temp_y, temp_z] = viat
                distsofar = 0
            else:
                if grid[temp_x, temp_y, temp_z] < OCC:
		    # PDL: fill in track unless connection point
		    grid[temp_x, temp_y, temp_z] = TRACK
                # PDL: updating current position
                temp_x = temp_x + DX[temp_z][min_dir];
		temp_y = temp_y + DY[temp_z][min_dir];

    def _connect(self, xs, ys, xg, yg, net_no, tempgrid, grid):
        # calls expand_from and backtrack_from to create connection
	# This is the only real change needed to make the program
	# transactional.
	# Instead of using the grid 'in place' to do the expansion, we take a
	# copy but the backtrack writes to the original grid.
	# This is not a correctness issue. The transactions would still
	# complete eventually without it.
	# However the expansion writes are only temporary and do not logically
	# conflict.
	# There is a question as to whether a copy is really necessary as a
	# transaction will anyway create
	# its own copy. if we were then to distinguish between writes not to be
	# committed (expansion) and
	# those to be committed (backtrack), we would not need an explicit
	# copy.
	# Taking the copy is not really a computational(time) overhead because
	# it avoids the grid 'reset' phase
	# needed if we do the expansion in place.
        tempgrid.reset(TEMP_EMPTY)
        # call the expansion method to return found/not found boolean
        found = self._expand_from_to(xs, ys, xg, yg, GRID_SIZE * 5, tempgrid, grid)
        if found:
            self._backtrack_from(xg, yg, xs, ys, net_no, tempgrid, grid)
        return found

    def disp_grid(self, z):
        laycol = (MAGENTA, GREEN)[z]
        for y in reversed(range(GRID_SIZE)): #WTF
            for x in range(GRID_SIZE):
                gg = self.grid[x, y, z]
                if gg == OCC:
                    self.view.point(x, y, CYAN)
                elif gg == VIA:
                    self.view.point(x, y, YELLOW)
                elif gg == BVIA:
                    self.view.point(x, y, RED)
                elif gg == TRACK:
                    self.view.point(x, y, laycol)



def main(args):
    if len(args) != 2:
        print "Params: [numthreads] [input-file]"
        sys.exit(-1)
    #
    num_threads = int(args[0])
    filename = args[1]
    lr = LeeRouter(filename)
    #
    # setup the benchmark
    start_time = 0
    current_time = 0
    #
    thread = [lr.create_thread() for _ in range(num_threads)]
    start_time = time.time()
    for t in thread:
        t.start()
    current_time = time.time()
    for t in thread:
        t.join()
    #
    elapsed_time = current_time - start_time
    print "Numthreads:", num_threads
    print "ElapsedTime:", elapsed_time, "s"
    report(start_time)
    if DEBUG:
        lr.disp_grid(0)
        lr.disp_grid(1)
        lr.view.show()



def report(start_time):
    stop_time = time.time()
    elapsed = stop_time - start_time
    print "Elapsed time:", elapsed, "s"
    print "-------------------------"



class Viewer(object):
    def __init__(self):
        self.points = []

    def point(self, x, y, col):
        self.points.append((x, y, col))

    def show(self, width=GRID_SIZE, height=GRID_SIZE):
        import Tkinter
        master = Tkinter.Tk()
        c = Tkinter.Canvas(master, width=width, height=height,
                           background="black")
        c.pack()
        img = Tkinter.PhotoImage(width=width, height=height)
        c.create_image((width/2, height/2), image=img,
                       state="normal")
        # draw
        for (x, y, col) in self.points:
            img.put(col, (x, y))
            #c.create_oval(x-1, y-1, x+1, y+1, fill=col, width=0)
        Tkinter.mainloop()



if __name__ == '__main__':
    main(sys.argv[1:])