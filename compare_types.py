#
# Compare Types
#
# Peter Turney, July 4, 2019
#
# Compare contrasting types, such as asexual reproduction
# versus sexual reproduction.
#
import golly as g
import model_classes as mclass
import model_functions as mfunc
import model_parameters as mparam
import numpy as np
import pickle
import os
import sys
#
# -----------------------------------------------------------------
# Open a dialog window and ask the user to select three folders.
# -----------------------------------------------------------------
#
g.note("Analyze Pickles\n\n" + \
       "You will be presented with three dialog menus:\n\n" + \
       "     (1) Select a FOLDER of pickled seeds of type 1.\n" + \
       "     (2) Select a FOLDER of pickled seeds of type 2.\n" + \
       "     (3) Select a FOLDER for storing the analysis results.\n\n" + \
       "The pickles will be analyzed and the results will be stored.\n")
#
pickle_dir1 = g.opendialog("Choose a folder of pickled seeds of type 1.", \
             "dir", g.getdir("app"))
pickle_dir2 = g.opendialog("Choose a folder of pickled seeds of type 2.", \
             "dir", g.getdir("app"))
analysis_dir = g.opendialog("Choose a folder for the analysis.", \
             "dir", g.getdir("app"))
#
g.note("Verify Selection\n\n" + \
       "The chosen folder of pickled seeds of type 1:\n\n" + \
       "   " + pickle_dir1 + "\n\n" + \
       "The chosen folder of pickled seeds of type 2:\n\n" + \
       "   " + pickle_dir2 + "\n\n" + \
       "The chosen folder for the analysis results:\n\n" + \
       "   " + analysis_dir + "\n\n" + \
       "Exit now if these folders are incorrect.")
#
# Make a list of the pickles in pickle_dir1.
#
pickle_list1 = []
for file in os.listdir(pickle_dir1):
  if file.endswith(".bin"):
    pickle_list1.append(file)
#
# Verify that there are some ".bin" files in the list.
#
if (len(pickle_list1) == 0):
  g.note("No pickles were found in the directory:\n\n" + \
         "   " + pickle_dir1 + "\n\n" + \
         "Exiting now.")
  sys.exit(0)
#
# Make a hash table that maps pickle names to the last
# generation number of the given group of pickles.
#
pickle_hash1 = mfunc.hash_pickles(pickle_list1)
smallest_pickle_size1 = min(pickle_hash1.values())
#
# Make a list of the pickles in pickle_dir2.
#
pickle_list2 = []
for file in os.listdir(pickle_dir2):
  if file.endswith(".bin"):
    pickle_list2.append(file)
#
# Verify that there are some ".bin" files in the list.
#
if (len(pickle_list2) == 0):
  g.note("No pickles were found in the directory:\n\n" + \
         "   " + pickle_dir2 + "\n\n" + \
         "Exiting now.")
  sys.exit(0)
#
# Make a hash table that maps pickle names to the last
# generation number of the given group of pickles.
#
pickle_hash2 = mfunc.hash_pickles(pickle_list2)
smallest_pickle_size2 = min(pickle_hash2.values())
#
# -----------------------------------------------------------------
# Initialize some variables and print them to the output.
# -----------------------------------------------------------------
#
# pickles for Algorithm 1
#
path1 = pickle_dir1
long_names1 = sorted(pickle_hash1.keys())
num_runs1 = len(long_names1)
#
# pickles for Algorithm 2
#
path2 = pickle_dir2
long_names2 = sorted(pickle_hash2.keys())
num_runs2 = len(long_names2)
#
# parameters shared by Algorithms 1 and 2
#
final_num = min(smallest_pickle_size1, smallest_pickle_size2)
step_size = 1
#
# analysis file
#
analysis_path = analysis_dir + "/compare-types.tsv"
analysis_handle = open(analysis_path, "w", 0) 
#
# parameters from model_parameters.py
#
width_factor = mparam.width_factor
height_factor = mparam.height_factor
time_factor = mparam.time_factor
num_trials = mparam.num_trials
#
mfunc.show_message(g, analysis_handle, \
  "\n\nCompare Types\n\n")
#
mfunc.show_message(g, analysis_handle, "path 1 = " + path1 + "\n\n")
for i in range(num_runs1):
  message = long_names1[i] + "\n"
  mfunc.show_message(g, analysis_handle, message)
mfunc.show_message(g, analysis_handle, "\n")
#
mfunc.show_message(g, analysis_handle, "path 2 = " + path2 + "\n\n")
for i in range(num_runs2):
  message = long_names2[i] + "\n"
  mfunc.show_message(g, analysis_handle, message)
mfunc.show_message(g, analysis_handle, "\n")
#
mfunc.show_message(g, analysis_handle, "width_factor = " + \
  str(width_factor) + "\n")
mfunc.show_message(g, analysis_handle, "height_factor = " + \
  str(height_factor) + "\n")
mfunc.show_message(g, analysis_handle, "time_factor = " + \
  str(time_factor) + "\n")
mfunc.show_message(g, analysis_handle, "num_trials = " + \
  str(num_trials) + "\n\n")
#
mfunc.show_message(g, analysis_handle, \
  "Note that the numbers will change slightly each time this \n" + \
  "runs. Although the seeds are constant, their locations and \n" + \
  "rotations vary.\n\n")
#
# The TSV (tab separated value) file has the format:
#
# <generation number> <tab> <average fitness of Algorithm 2 vs 1>
#
# If Algorithm 2 is more fit than Algorithm 1 for the given generation,
# then the average fitness will be greater than 0.5; otherwise it will
# be less than 0.5.
#
# -----------------------------------------------------------------
# For each generation, compare Algorithm 2 to Algorithm 1.
# -----------------------------------------------------------------
#
for i in range(0, final_num + 1, step_size):
  # e.g.: i = 0, 1, 2, 3, ..., 75
  # fitness for Algorithm 2:
  total_fitness = 0
  total_sample_size = 0
  # for each run of Algorithm 1 in generation i ...
  for run1 in range(num_runs1):
    # A0, B0, C0, D0
    long_name1 = long_names1[run1] # log-2018-11-19-15h-40m-05s
    # read in X1
    x1_long_name = long_name1 + "-pickle-" + str(i) + ".bin"
    x1_path = path1 + x1_long_name
    x1_handle = open(x1_path, "rb") # rb = read binary
    x1_sample = pickle.load(x1_handle)
    x1_handle.close()
    # for each run of Algorithm 2 in generation i ...
    for run2 in range(num_runs2):
      # A1, B1, C1, D1
      long_name2 = long_names2[run2] # log-2018-11-19-15h-40m-05s
      # read in X2
      x2_long_name = long_name2 + "-pickle-" + str(i) + ".bin"
      x2_path = path2 + x2_long_name
      x2_handle = open(x2_path, "rb") # rb = read binary
      x2_sample = pickle.load(x2_handle)
      x2_handle.close()
      # for each seed in x1_sample ...
      for s1 in x1_sample:
        # for each seed in x2_sample ...
        for s2 in x2_sample:
          [score1, score2] = mfunc.score_pair(g, s1, s2, \
            width_factor, height_factor, time_factor, num_trials)
          total_fitness = total_fitness + score2
          total_sample_size = total_sample_size + 1
  #
  average_fitness = total_fitness / total_sample_size
  #
  mfunc.show_message(g, analysis_handle, \
    str(i) + "\t" + str(average_fitness) + "\n")
#
# Final message.
#
mfunc.show_message(g, analysis_handle, "\nAnalysis complete.\n")
analysis_handle.close()
#
#