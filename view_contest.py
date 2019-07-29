#
# View Contest
#
# Peter Turney, July 16, 2019
#
# Select two seeds from pickles and watch them battle.
#
import golly as g
import model_classes as mclass
import model_functions as mfunc
import model_parameters as mparam
import random as rand
import time
import pickle
import os
#
# Open a dialog window and ask the user to select two pickles.
#
g.note("View Contest\n\n" + \
  "You will be presented with two dialog menus:\n" + \
  "     (1) Select a file of pickled seeds.\n" + \
  "     (2) Select another file of pickled seeds.\n" + \
  "Two seeds, chosen randomly from each pickle, will then compete.")
#
path1 = g.opendialog("Select the first pickled seed file (*.bin)", \
  "(*.bin)|*.bin", g.getdir("app"))
path2 = g.opendialog("Select the second pickled seed file (*.bin)", \
  "(*.bin)|*.bin", g.getdir("app"))
#
# Some info to display to the user, in the header of the main window.
#
[head1, tail1] = os.path.split(path1)
[head2, tail2] = os.path.split(path2)
#
g.show("Red: " + path1 + "    Blue: " + path2)
#
# Load pickles and select the first seed from each pickle.
# The seeds are in order of decreasing fitness.
#
handle1 = open(path1, "rb") # rb = read binary
pickle1 = pickle.load(handle1)
handle1.close()
seed1 = rand.choice(pickle1) # random seed from pickle1
#
handle2 = open(path2, "rb") # rb = read binary
pickle2 = pickle.load(handle2)
handle2.close()
seed2 = rand.choice(pickle2) # random seed from pickle2
#
# Let the seeds play the Immigration Game.
#
width_factor = mparam.width_factor
height_factor = mparam.height_factor
time_factor = mparam.time_factor
#
# At the bottom of this loop, the user will be prompted to quit 
# the loop, if desired.
#
while True: 
  # random rotation of seeds
  s1 = seed1.random_rotate()
  s2 = seed2.random_rotate()
  # switch red to blue in the second seed
  s2.red2blue()
  # set up Golly
  [g_width, g_height, g_time] = mfunc.dimensions(s1, s2, \
      width_factor, height_factor, time_factor)
  g.setalgo("QuickLife") # use the QuickLife algorithm
  g.new("Immigration") # initialize cells to state 0
  g.setrule("Immigration:T" + str(g_width) + "," + str(g_height)) # make a toroid
  [g_xmin, g_xmax, g_ymin, g_ymax] = mfunc.get_minmax(g) # find range of coordinates
  s1.insert(g, g_xmin, -1, g_ymin, g_ymax) # insert the first seed into Golly
  s2.insert(g, +1, g_xmax, g_ymin, g_ymax) # insert the second seed into Golly
  g.setmag(mfunc.set_mag(g)) # set magnification
  g.setcolors([0,255,255,255]) # set state 0 (the background) to white
  #
  g.update() # show the intial state
  #
  g.note("These are the intial seeds.\n" + \
    "Red is on the left and blue is on the right.\n" + \
    "The file names are in the header of the main window.\n" + \
    "Drag this note to a new location if it is blocking your view.\n\n" + \
    "Red seed directory:  " + head1 + "\n" + \
    "Red seed file:  " + tail1 + "\n" + \
    "Red seed size:  {} x {}\n".format(seed1.xspan, seed1.yspan) + \
    "Red seed density:  {:.4f} ({} ones)\n\n".format(seed1.density(), \
      seed1.count_ones()) + \
    "Blue seed directory: " + head2 + "\n" + \
    "Blue seed file: " + tail2 + "\n" + \
    "Blue seed size: {} x {}\n".format(seed2.xspan, seed2.yspan) + \
    "Blue seed density: {:.4f} ({} ones)\n\n".format(seed2.density(), \
      seed2.count_ones()) + \
    "Select OK to begin the competition.\n")
  #
  while (int(g.getgen()) < g_time):
    g.run(1) # run for 1 step without displaying
    g.update() # now display
  #
  [count1, count2] = mfunc.count_pops(g) # see who won
  if (count1 > count2):
    result = "Red won! Red: {}. Blue: {}.\n\n".format(count1, count2)
  elif (count2 > count1):
    result = "Blue won! Red: {}. Blue: {}.\n\n".format(count1, count2)
  else:
    result = "Tie! Red: {}. Blue: {}.\n\n".format(count1, count2)
  #
  # Note that s2 is blue, which means it contains twos, not ones. 
  # Thus we use seed2, which is red, for density() and count_ones().
  #
  message = result + \
    "Red seed directory:  " + head1 + "\n" + \
    "Red seed file:  " + tail1 + "\n" + \
    "Red seed size:  {} x {}\n".format(seed1.xspan, seed1.yspan) + \
    "Red seed density:  {:.4f} ({} ones)\n\n".format(seed1.density(), \
      seed1.count_ones()) + \
    "Blue seed directory: " + head2 + "\n" + \
    "Blue seed file: " + tail2 + "\n" + \
    "Blue seed size: {} x {}\n".format(seed2.xspan, seed2.yspan) + \
    "Blue seed density: {:.4f} ({} ones)\n\n".format(seed2.density(), \
      seed2.count_ones()) + \
    "Select Cancel to end.\n" + \
    "Select OK to run again with new rotations and locations."
  #
  g.note(message) # here is where the user can quit
  #
#
#