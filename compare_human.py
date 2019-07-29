#
# Compare Human
#
# Peter Turney, July 23, 2019
#
# Compare human-designed seeds with evolved seeds.
#
import golly as g
import model_classes as mclass
import model_functions as mfunc
import model_parameters as mparam
import numpy as np
import pickle
import os
import sys
import glob
#
# version number
#
version = "layer4XL_breeders"
#
# the path for Golly
#
app_dir = g.getdir("app")
#
# the path for human-designed Game of Life patterns
#
######pattern_dir = app_dir + os.path.join("Patterns", "Life")
pattern_dir = app_dir + os.path.join("Patterns", "Life", "Breeders")
#
# the path for evolved seeds
#
######evolved_dir = app_dir + os.path.join("Modeling Major Transitions",
######  "Section 4.1", "Layer 4", "pickles")
evolved_dir = app_dir + os.path.join("Experiments", "exper186",
  "pickles100")
#
# the path for the analysis report file
#
text_path = app_dir + os.path.join("Experiments", "exper188",
  "compare_human_" + version + ".txt")
#
# the path for the spreadsheet file (tsv - tab separated values)
#
spreadsheet_path = app_dir + os.path.join("Experiments", "exper188",
  "compare_human_" + version + ".tsv")
#
# the maximum allowed area for a designed seed
#
max_area = 50000
#
# overriding the value given to num_trials in model_parameters
#
num_trials = 20
#
# a pattern for matching the last generation of pickles
#
last_generation = "*-pickle-100.bin"
#
# some parameters for the Immigration Game
#
width_factor = mparam.width_factor
height_factor = mparam.height_factor
time_factor = mparam.time_factor
#
# open files for recording results
#
# - use "0" for unbuffered file output, so we can see the results
#   immediately
#
text_file = open(text_path, "w", 0)
spreadsheet_file = open(spreadsheet_path, "w", 0)
#
# write out some parameter settings for the record
#
text_file.write("\n\nDesigned Seeds versus Evolved Seeds\n\n" + \
  "width_factor = " + str(width_factor) + "\n" + \
  "height_factor = " + str(height_factor) + "\n" + \
  "time_factor = " + str(time_factor) + "\n" + \
  "num_trials = " + str(num_trials) + "\n" + \
  "last_generation = " + last_generation + "\n" + \
  "max_area = " + str(max_area) + "\n\n")
#
# read in the evolved seeds
#
# - for each experiment run in the directory, extract the fittest seed
#   from the last generation of the run
#
text_file.write(evolved_dir + "\n\n") # for record keeping
evolved_file_list = glob.glob(os.path.join(evolved_dir, last_generation))
evolved_seeds = []
total_area = 0
total_density = 0
#
for evolved_file in evolved_file_list:
  pickle_handle = open(evolved_file, "rb") # rb = read binary
  elite_sample = pickle.load(pickle_handle)
  pickle_handle.close()
  fittest_seed = elite_sample[0] # first element is fittest seed
  evolved_seeds.append(fittest_seed)
  # for record keeping
  xspan = fittest_seed.xspan
  yspan = fittest_seed.yspan
  area = xspan * yspan
  density = fittest_seed.density()
  text_file.write(os.path.basename(evolved_file) + \
    " -- x = " + str(xspan) + ", y = " + str(yspan) + \
    ", area = " + str(area) + ", density = " + \
    str(density) + "\n")
  total_area = total_area + area
  total_density = total_density + density
#
num_evolved_seeds = len(evolved_seeds)
avg_area = total_area / num_evolved_seeds
avg_density = total_density / num_evolved_seeds
text_file.write("\naverage area = " + str(avg_area) + "\n")
text_file.write("average density = " + str(avg_density) + "\n\n")
#
# traverse the directory tree for pattern_dir and look for suitable 
# pattern files
#
for dir_name, subdir_list, file_list in os.walk(pattern_dir):
  for file_name in file_list:
    pattern_file = os.path.join(dir_name, file_name)
    # verify that we can handle this pattern: 0 = bad, 1 = good
    if (mfunc.validate_designed_seed(g, pattern_file, max_area) == 1):
      # write the path for this pattern to the text file
      text_file.write(pattern_file + "\n\n")
      # read the pattern into a seed
      designed_seed = mfunc.load_designed_seed(g, pattern_file)
      # write the x span and y span of the designed seed pattern
      designed_seed_area = designed_seed.xspan * designed_seed.yspan
      designed_seed_density = designed_seed.density()
      text_file.write("designed seed size: x = " + \
        str(designed_seed.xspan) + ", y = " + \
        str(designed_seed.yspan) + ", area = " + \
        str(designed_seed_area) + ", density = " + \
        str(designed_seed_density) + "\n")
      # compete the designed seed against the evolved seeds
      total_designed_score = 0.0
      total_evolved_score = 0.0
      for evolved_seed in evolved_seeds:
        [designed_score, evolved_score] = mfunc.score_pair(g, \
          designed_seed, evolved_seed, width_factor, height_factor, \
          time_factor, num_trials)
        total_designed_score = total_designed_score + designed_score
        total_evolved_score = total_evolved_score + evolved_score
      # write out the score for the analysis report file
      avg_designed_score = total_designed_score / num_evolved_seeds
      avg_evolved_score = total_evolved_score / num_evolved_seeds
      text_file.write("score designed = " + str(avg_designed_score) + \
        "\nscore evolved = " + str(avg_evolved_score) + "\n\n")
      #
      # write out the score for the spreadsheet file
      #
      # - from the path "...\Patterns\Life\Bounded-Grids\agar-p3.rle",
      #   we want to extract both the file name "agar-p3.rle" and 
      #   the category "Bounded-Grids"
      # - "agar-p3.rle" is given by file_name
      # - "Bounded-Grids" is the last subdirectory in the path dir_name
      #
      category = os.path.basename(os.path.normpath(dir_name))
      spreadsheet_file.write(category + "\t" + file_name + "\t" + \
        str(designed_seed.xspan) + "\t" + str(designed_seed.yspan) + \
        "\t" + str(designed_seed_area) + "\t" + \
        str(designed_seed_density) + "\t" + \
        str(avg_designed_score) + "\t" + str(avg_evolved_score) + "\n")
#
# close the files for recording results
#
text_file.close()
spreadsheet_file.close()
#
#