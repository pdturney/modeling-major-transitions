#
# Compare Generations
#
# Peter Turney, July 4, 2019
#
# Compare seeds across different generations. Each seed in a
# given run is compared with the seeds in the final generation
# of the same run.
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
# -----------------------------
# Get some input from the user.
# -----------------------------
#
[pickle_dir, analysis_dir, sorted_pickle_names, \
  smallest_pickle_size] = mfunc.choose_pickles(g)
#
# -----------------------------------------------------------------
# Initialize some variables and print them to the output.
# -----------------------------------------------------------------
#
# pickles
#
num_runs = len(sorted_pickle_names)
final_num = smallest_pickle_size
step_size = 1
#
# stats analysis file
#
basename = os.path.basename(os.path.normpath(analysis_dir))
analysis_path = analysis_dir + "/compare-generations-" + \
  basename + ".tsv"
analysis_handle = open(analysis_path, "w", 0) 
#
# parameters from model_parameters.py
#
width_factor = mparam.width_factor
height_factor = mparam.height_factor
time_factor = mparam.time_factor
num_trials = mparam.num_trials
#
mfunc.show_message(g, analysis_handle, "\n\nCompare Generations\n\n")
#
for i in range(num_runs):
  message = sorted_pickle_names[i] + "\n"
  mfunc.show_message(g, analysis_handle, message)
#
mfunc.show_message(g, analysis_handle, "\n")
#
mfunc.show_message(g, analysis_handle, "\nwidth_factor = " + \
  str(width_factor) + "\n")
mfunc.show_message(g, analysis_handle, "height_factor = " + \
  str(height_factor) + "\n")
mfunc.show_message(g, analysis_handle, "time_factor = " + \
  str(time_factor) + "\n")
mfunc.show_message(g, analysis_handle, "num_trials = " + \
  str(num_trials) + "\n\n")
mfunc.show_message(g, analysis_handle, "path = " + \
  str(pickle_dir) + "\n\n")
#
mfunc.show_message(g, analysis_handle, \
  "Note that the numbers will change slightly each time this \n" + \
  "runs.\n\n")
#
# The TSV (tab separated value) file has the format:
#
# <generation number> <tab> <average fitness of given generation vs 
#                            average fitness of final generation>
#
# -----------------------------------------------------------------
# For each generation, compare the given generation to the final
# generation.
# -----------------------------------------------------------------
#
pop_size = mparam.pop_size
elite_size = mparam.elite_size
#
# fetch the final generation pickles
#
z_pickles = []
for run in range(num_runs):
  pickle_name = sorted_pickle_names[run] # log-2018-11-19-15h-40m-05s
  # read in Z
  z_name = pickle_name + "-pickle-" + str(final_num) + ".bin"
  z_path = pickle_dir + z_name
  z_handle = open(z_path, "rb") # rb = read binary
  z_sample = pickle.load(z_handle)
  z_handle.close()
  z_pickles.append(z_sample)
#
# compare each generation to the final generation
#
for i in range(0, final_num + 1, step_size):
  # for each run in generation i ...
  avg_fitnesses = []
  for run in range(num_runs):
    pickle_name = sorted_pickle_names[run] # log-2018-11-19-15h-40m-05s
    # read in X
    x_name = pickle_name + "-pickle-" + str(i) + ".bin"
    x_path = pickle_dir + x_name
    x_handle = open(x_path, "rb") # rb = read binary
    x_sample = pickle.load(x_handle)
    x_handle.close()
    # get Z
    z_sample = z_pickles[run]
    # compare X with Z
    total_fitness = 0.0
    total_sample_size = 0
    for sx in x_sample:
      for sz in z_sample:
        [scorex, scorez] = mfunc.score_pair(g, sx, sz, \
          width_factor, height_factor, time_factor, num_trials)
        total_fitness = total_fitness + scorex
        total_sample_size = total_sample_size + 1
    # calculate average fitness for the run
    avg_fitness = total_fitness / total_sample_size
    # convert to formatted string
    avg_fitnesses.append("{:.4f}".format(avg_fitness)) 
  # write out the fitness
  tab = "\t"
  mfunc.show_message(g, analysis_handle, \
    str(i) + tab + tab.join(avg_fitnesses) + "\n")
#
# Final message.
#
mfunc.show_message(g, analysis_handle, "\nAnalysis complete.\n")
analysis_handle.close()
#
#