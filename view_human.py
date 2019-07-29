#
# View Human
#
# Peter Turney, July 16, 2019
#
# Select one human-designed seed and one machine-evolved seed
# and watch them battle.
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
# Open a dialog window and ask the user to select two seeds.
#
g.note("View Contest\n\n" + \
  "You will be presented with two dialog menus:\n" + \
  "     (1) Select a file with one human-designed pattern.\n" + \
  "     (2) Select a file of pickled seeds (the fittest seed will be used).\n" + \
  "The two seeds will then compete.")
#
path1 = g.opendialog("Select a human-designed Life pattern file (*.rle)", \
  "(*.rle)|*.rle", g.getdir("app"))
path2 = g.opendialog("Select a machine-evolved Life seed file (*.bin)", \
  "(*.bin)|*.bin", g.getdir("app"))
#
# Some info to display to the user, in the header of the main window.
#
[head1, tail1] = os.path.split(path1)
[head2, tail2] = os.path.split(path2)
#
g.show("Red: " + path1 + "    Blue: " + path2)
#
# Load the human-designed Life pattern file.
#
seed1 = mfunc.load_designed_seed(g, path1)
#
# Load machine-evolved Life seeds in the pickle.
# The seeds are in order of decreasing fitness.
# Select the first seed from the pickle.
# 
handle = open(path2, "rb") # rb = read binary
pickle = pickle.load(handle)
handle.close()
seed2 = pickle[0]
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