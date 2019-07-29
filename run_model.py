#
# Run Model
#
# Peter Turney, July 5, 2019
#
# The evolutionary algorithm used here is based on Whitley's 
# GENITOR algorithm, with several extensions.
#
# Whitley, D., and Kauth, J. (1988). GENITOR: A different genetic 
# algorithm. Proceedings of the Rocky Mountain Conference on 
# Artificial Intelligence, Denver, CO. pp. 118-130.
# 
# Whitley, D. (1989). The GENITOR algorithm and selective pressure. 
# Proceedings of the Third International Conference on Genetic 
# Algorithms (ICGA-89), pp. 116-121. California: Morgan Kaufmann. 
#
import golly as g
import model_classes as mclass
import model_functions as mfunc
import model_parameters as mparam
import random as rand
import copy
import time
import pickle
#
# -----------------------------------------------------------------
# Make a file for logging the results. The filename is based on the
# date, so that log files can easily be ordered by date.
# -----------------------------------------------------------------
#
log_name = time.strftime("log-20%y-%m-%d-%Hh-%Mm-%Ss", \
  time.localtime())
log_path = mparam.log_directory + "/" + log_name + ".txt"
# use 0 so that log file writes immediately (no buffer), 
# in case of forced exit
log_handle = open(log_path, "w", 0) 
start_time = time.strftime("Start time: 20%y-%m-%d %Hh:%Mm:%Ss\n", \
  time.localtime())
mfunc.show_message(g, log_handle, start_time)
# show parameter settings
parameter_settings = mfunc.show_parameters()
mfunc.show_message(g, log_handle, "\nParameter Settings\n\n")
for setting in parameter_settings:
  mfunc.show_message(g, log_handle, setting + "\n")
mfunc.show_message(g, log_handle, "\n")
#
# -----------------------------------------------------------------
# Set the random number generator seed here. If random_seed is 
# negative, then Python will automatically set a random number 
# seed. Note that, if random_seed is negative, then the experiment 
# cannot be exactly repeated.
# -----------------------------------------------------------------
#
random_seed = mparam.random_seed
if (random_seed >= 0):
  rand.seed(random_seed)
#
# -----------------------------------------------------------------
# Build the initial population. Initialize the seeds randomly.
# -----------------------------------------------------------------
#
seed_density = mparam.seed_density # density of state 1 in seed
assert seed_density > 0.0
assert seed_density < 1.0
s_xspan = mparam.s_xspan # width of seed
s_yspan = mparam.s_yspan # height of seed
pop_size = mparam.pop_size # fixed population size
#
message = "Building initial population of size: " + str(pop_size) + "\n"
mfunc.show_message(g, log_handle, message)
#
pop = mfunc.initialize_population(pop_size, s_xspan, s_yspan, \
  seed_density)
#
# -----------------------------------------------------------------
# Make the seeds compete against each other, to build up a history
# of wins and losses for the initial population.
# -----------------------------------------------------------------
#
width_factor = mparam.width_factor
height_factor = mparam.height_factor
time_factor = mparam.time_factor
num_trials = mparam.num_trials
#
message = "Building a history for initial population.\n"
mfunc.show_message(g, log_handle, message)
#
# Every seed competes against every other seed (and itself)
for i in range(pop_size):
  # Since mfunc.update_history updates i's score for j and j's score for i,
  # we only need to calculate the lower triangle of the matrix of scores.
  for j in range(i + 1):
    mfunc.update_history(g, pop, i, j, width_factor, height_factor, \
      time_factor, num_trials)
    # While we're here, let's update the similarities.
    mfunc.update_similarity(pop, i, j)
#
# -----------------------------------------------------------------
# Log the average population fitness for the initial population.
# -----------------------------------------------------------------
#
avg_fit = mfunc.average_fitness(pop)
message = "Average fitness of the initial population: {:.3f}\n".format(avg_fit)
mfunc.show_message(g, log_handle, message)
#
# -----------------------------------------------------------------
# Run the system until run_length children have been born.
# -----------------------------------------------------------------
#
# Get some parameter values from model_parameters.py.
#
run_length = mparam.run_length
tournament_size = mparam.tournament_size
elite_size = mparam.elite_size
log_directory = mparam.log_directory
experiment_type_num = mparam.experiment_type_num
max_area_first = mparam.max_area_first
max_area_last = mparam.max_area_last
#
# We add 1 to run_length so that a run_length of, say, 1000, will
# yield a range of 0, 1, ..., 1000. Then, if pop_size is, say, 100,
# the final trip through the loop will have n = 1000 and
# pop_size = 100, so ((n % pop_size) == 0) will be true, and
# the final trip will be archived.
#
for n in range(run_length + 1): 
  #
  # If n (the number of children born so far) is an integer multiple
  # of pop_size (the population size), then store the top elite_size
  # seeds in the population, as a benchmark for measuring progress
  # in evolution.
  #
  if ((n % pop_size) == 0): # if n divides evenly by pop_size ...
    run_id_number = n / pop_size # ... an integer is expected here
    # Store the elite of the population for later analysis.
    mfunc.archive_elite(pop, elite_size, log_directory, \
      log_name, run_id_number)
    #
  #
  # Calculate max_seed_area. The maximum seed area increases linearly 
  # with each new child born. The motivation for this linear limit to 
  # the seed area is to prevent an explosive increase in seed area, 
  # which causes the simulation to run extremely slowly. This limit is 
  # due to a lack of patience on my part; it is not intended to model 
  # a natural phenomenon.
  #
  max_area_delta = max_area_last - max_area_first
  max_area_increment = max_area_delta * (n / float(run_length + 1))
  max_seed_area = max_area_first + max_area_increment
  #
  # Run a tournament to select a seed for reproduction. Four types
  # of reproduction are possible.
  #
  # Get a random sample of tournament_size from the population
  tournament_sample = mfunc.random_sample(pop, tournament_size)
  # Find the most fit member of the sample
  candidate_seed = mfunc.find_best_seed(tournament_sample)
  #
  # Find the address of the incumbent best seed in the population.
  #
  incumbent_seed = mfunc.find_best_seed(pop)
  #
  # Update the population according to the chosen type of reproduction;
  # that is, chosen according to experiment_type_num.
  #
  if (experiment_type_num == 1):
    # uniform asexual -- note: no need for max_seed_area here
    [pop, message] = mfunc.uniform_asexual(candidate_seed, \
      pop, n)
    mfunc.show_message(g, log_handle, message)
  elif (experiment_type_num == 2):
    # variable asexual
    [pop, message] = mfunc.variable_asexual(candidate_seed, \
      pop, n, max_seed_area)
    mfunc.show_message(g, log_handle, message)
  elif (experiment_type_num == 3):
    # sexual
    [pop, message] = mfunc.sexual(candidate_seed, pop, n, \
      max_seed_area)
    mfunc.show_message(g, log_handle, message)
  else:
    # symbiotic
    assert experiment_type_num == 4
    [pop, message] = mfunc.symbiotic(candidate_seed, pop, n, \
      max_seed_area)
    mfunc.show_message(g, log_handle, message)
  #
  # Compare the new best seed with the incumbent best seed.
  # Note that the fitness of the incumbent will have changed
  # now that the population has been updated.
  #
  incumbent_address = incumbent_seed.address
  incumbent_fitness = incumbent_seed.fitness()
  incumbent_area = incumbent_seed.xspan * incumbent_seed.yspan
  #
  winning_seed = mfunc.find_best_seed(pop)
  winning_address = winning_seed.address
  winning_fitness = winning_seed.fitness()
  winning_area = winning_seed.xspan * winning_seed.yspan
  #
  similarity = mfunc.similarity(incumbent_seed, winning_seed)
  address_change = (incumbent_address != winning_address)
  fitness_change = winning_fitness - incumbent_fitness
  area_change = winning_area - incumbent_area
  #
  message = "Incumbent vs Winner: " + \
    "  Similarity: {:.3f}".format(similarity) + \
    "  Address change: {:}".format(address_change) + \
    "  Fitness change: {:.3f}".format(fitness_change) + \
    "  Area change: {:.3f}\n".format(area_change)
  #
  mfunc.show_message(g, log_handle, message)
  #
#
# -----------------------------------------------------------------
# Close the log file.
# -----------------------------------------------------------------
#
avg_fit = mfunc.average_fitness(pop)
message = "Average fitness of the final population: {:.3f}\n".format(avg_fit)
mfunc.show_message(g, log_handle, message)
#
end_time = time.strftime("End time: 20%y-%m-%d %Hh:%Mm:%Ss\n", time.localtime())
mfunc.show_message(g, log_handle, end_time)
log_handle.close()
#
#