#
# Model Parmeters
#
# Peter Turney, July 5, 2019
#
# Set various parameters for running experiments
#
#
#
# Type of experiment:
#
# 1 = uniform asexual  = asexual with bit-flip mutation but no seed size change
# 2 = variable asexual = asexual with bit-flip mutation and seed size change
# 3 = sexual           = bit-flip mutation, seed size change, and crossover
# 4 = symbiotic        = mutation, size change, crossover, fission, and fusion
#
experiment_type_num = 3
#
if (experiment_type_num == 1):
  experiment_type_name = "uniform asexual"
elif (experiment_type_num == 2):
  experiment_type_name = "variable asexual"
elif (experiment_type_num == 3):
  experiment_type_name = "sexual"
else:
  assert experiment_type_num == 4
  experiment_type_name = "symbiotic"
#
# Set the random number generator seed here. If random_seed is negative,
# then Python will automatically set a random number seed. Note that, if
# random_seed is negative, then the experiment cannot be exactly repeated.
#
random_seed = 42
#
# Directory for log files. 
#
log_directory = "../Experiments/exper180/pickles"
#
# Fixed population size. Steady-state model for evolution. For every
# birth, there is one death.
#
pop_size = 200
#
# The number of trials for a given pair of seeds. Each pair of seeds
# competes several times, with different rotations and different
# locations in Golly space. The final result for the pair is the 
# average of the trials.
#
num_trials = 2
#
# run_length: the number of children born in one run. Each child that
# is born will replace an existing member of the population, so the
# size of the population is constant.
#
# num_generations: one generation is when pop_size children are born.
#
# We want run_length to be evenly divisible by pop_size, because we
# take samples of the population at the end of each generation.
#
num_generations = 100
#
run_length = num_generations * pop_size
#
# Minimum seed sizes.
#
min_s_xspan = 5
min_s_yspan = 5
#
# Initial seed sizes.
#
s_xspan = 5
s_yspan = 5
#
assert s_xspan >= min_s_xspan
assert s_yspan >= min_s_yspan
#
# Maximum seed area: The maximum seed area increases linearly with
# each new child born. Here we set the desired maximum seed area
# for the first child and the last child. The motivation for this
# linear limit to the seed area is to prevent an explosive increase
# in seed area, which causes the simulation to run extremely
# slowly. This limit is due to a lack of patience on my part; it
# is not intended to model a natural phenomenon.
#
max_area_first = 120
max_area_last = 170
#
# Probability of state 1 for random initialization of a new seed.
# For the initial random seeds, use a random density of 37.5%. See:
#
# http://www.njohnston.ca/2009/06/longest-lived-soup-density-in-conways-game-of-life/
# http://www.njohnston.ca/2009/07/the-maximal-lifespan-of-patterns-in-conways-game-of-life/
#
seed_density = 0.375
#
# Multiply the sizes of the seeds by this factor to get the size
# of the toroid. Thus the toroid expands as the seeds get larger.
# The width is greater than the height because the two seeds are
# positioned side-by-side horizontally.
#
width_factor = 6.0
height_factor = 3.0
#
# Multiply the sizes of the toroid by this factor to get the
# number of generations for a run. Thus the running time
# increases as the toroid expands.
#
time_factor = 6.0
#
# The size of the random sample for a tournament. The most fit
# member of the tournament sample will be allowed to reproduce.
#
tournament_size = 2
#
# Probability for mutation in uniform asexual experiments
# (type 1; see above).
#
mutation_rate = 0.01
#
# Probabilities for the three kinds of mutation in variable
# asexual experiments (type 2; see above).
#
# prob_grow     = probability of invoking grow()
# prob_flip     = probability of invoking flip_bits()
# prob_shrink   = probability of invoking shrink()
#
# Constraints:
#
# - all parameters must lie in the range from 0.0 to 1.0
# - the parameters must sum to 1.0
#
prob_grow     = 0.2
prob_flip     = 0.6
prob_shrink   = 0.2
#
assert prob_grow + prob_flip + prob_shrink == 1.0
#
# Elite size: size of the sample that will be used to evaluate
# whether the best seeds (the elite) are getting better.
#
elite_size = 50
#
# Two seeds are allowed to mate (that is, they are considered as
# member of the same species) when they are highly similar but
# not identical. The following parameters define the desired
# region of similarity for mating.
#
min_similarity = 0.80
max_similarity = 0.99
#
# For symbiosis, set the probabilities of fission and fusion.
# Because fusion can result in large seeds, which will slow down 
# the simulation, the probability of fusion should be relatively 
# low.
#
prob_fission = 0.01
prob_fusion = 0.005
#
assert prob_fission + prob_fusion <= 1.0
#