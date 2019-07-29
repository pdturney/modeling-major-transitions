#
# Measure Similarities
#
# Peter Turney, July 4, 2019
#
# Calculate the average similarity between each elite
# seed and its most similar counterpart in the population.
#
# Although the pickles do not contain the whole population,
# they do contain the similarities between the elites and
# the whole population.
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
analysis_path = analysis_dir + "/measure-similarities-" + \
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
mfunc.show_message(g, analysis_handle, "\n\nSeed Similarities\n\n")
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
# The TSV (tab separated value) file has the format:
#
# <generation number> <tab> <seed density for A>
#                     <tab> <seed standard deviation for B>
#                     <tab> <seed standard deviation for C>
#                     ...
#
# -----------------------------------------------------------------
# For each generation, calculate the elite statistics.
# -----------------------------------------------------------------
#
for i in range(0, final_num + 1, step_size):
  # e.g.: i = 0, 1, 2, 3, ..., 75
  # fitness for Algorithm 1:
  total_fitness = 0
  total_sample_size = 0
  # for each run in generation i ...
  avg_similarities = []
  for run in range(num_runs):
    pickle_name = sorted_pickle_names[run] # log-2018-11-19-15h-40m-05s
    # read in X
    x_name = pickle_name + "-pickle-" + str(i) + ".bin"
    x_path = pickle_dir + x_name
    x_handle = open(x_path, "rb") # rb = read binary
    x_sample = pickle.load(x_handle)
    x_handle.close()
    # for each seed in X, find the maximum similarity to any
    # other seed in the population
    total_similarity = 0.0
    for seed in x_sample:
      sims = seed.similarities
      # set self-similarity to zero
      sims[seed.address] = 0.0
      # find maximum
      total_similarity = total_similarity + sims.max()
    # calculate the average
    avg_similarity = total_similarity / float(len(x_sample))
    # convert to formatted string and append to list
    avg_similarities.append("{:.4f}".format(avg_similarity)) 
  # write out the similarities
  tab = "\t"
  mfunc.show_message(g, analysis_handle, \
    str(i) + tab + tab.join(avg_similarities) + "\n")
#
# Final message.
#
mfunc.show_message(g, analysis_handle, "\nAnalysis complete.\n")
analysis_handle.close()
#
#