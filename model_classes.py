"""
Model Classes

Peter Turney, July 5, 2019
"""
import golly as g
import model_parameters as mparam
import random as rand
import numpy as np
import copy
"""
Make a class for seeds.
"""
#
# Note: Golly locates cells by x (horizontal) and y (vertical) coordinates,
# usually given in the format (x, y). On the other hand, we are storing
# these cells in matrices, where the coordinates are usually given in the
# format [row][column], where row is a vertical coordinate and column
# is a horizontal coordinate. Although it may be somewhat confusing, we
# use [x][y] for our matrices (x = row index, y = column index). That is:
#
#     self.xspan = self.cells.shape[0]
#     self.yspan = self.cells.shape[1]
#
class Seed:
  """
  A class for seeds.
  """
  #
  # __init__(self, xspan, yspan, pop_size) -- returns NULL
  #
  def __init__(self, xspan, yspan, pop_size):
    """
    Make an empty seed (all zeros).
    """
    # width of seed on the x-axis
    self.xspan = xspan 
    # height of seed on the y-axis
    self.yspan = yspan 
    # initial seed of zeros, to be modified later
    self.cells = np.zeros((xspan, yspan), dtype=np.int) 
    # initial history of zeros
    self.history = np.zeros(pop_size, dtype=np.float) 
    # initial similarities of zeros
    self.similarities = np.zeros(pop_size, dtype=np.float) 
    # position of seed in the population array, to be modified later
    self.address = 0 
  #
  # randomize(self, seed_density) -- returns NULL
  #
  def randomize(self, seed_density):
    """
    Randomly set some cells to state 1. It is assumed that the
    cells in the given seed are initially all in state 0. The
    result is a seed in which the fraction of cells in state 1
    is approximately equal to seed_density (with some random
    variation). Strictly speaking, seed_density is the
    expected value of the fraction of cells in state 1.
    """
    for x in range(self.xspan):
      for y in range(self.yspan):
        if (rand.random() <= seed_density):
          self.cells[x][y] = 1
  #
  # shuffle(self) -- returns a shuffled copy of the given seed
  #
  def shuffle(self):
    """
    Make a copy of the given seed and then shuffle the cells in 
    the seed. The new shuffled seed will have the same dimensions
    and the same density of 1s and 0s as the given seed, but the 
    locations of the 1s and 0s will be different. (There is a very 
    small probability that shuffling might not result in any change, 
    just as shuffling a deck of cards might not change the deck.)
    The density of shuffled_seed is exactly the same as the density
    of the given seed.
    """
    #
    shuffled_seed = copy.deepcopy(self)
    #
    # for each location [x0][y0], randomly choose another location
    # [x1][y1] and swap the values of the cells in the two locations.
    #
    for x0 in range(self.xspan):
      for y0 in range(self.yspan):
        x1 = rand.randrange(self.xspan)
        y1 = rand.randrange(self.yspan)
        temp = shuffled_seed.cells[x0][y0]
        shuffled_seed.cells[x0][y0] = shuffled_seed.cells[x1][y1]
        shuffled_seed.cells[x1][y1] = temp
    #
    return shuffled_seed
  #
  #
  # red2blue(self) -- returns NULL
  #
  def red2blue(self):
    """
    Switch cells from state 1 (red) to state 2 (blue).
    """
    for x in range(self.xspan):
      for y in range(self.yspan):
        if (self.cells[x][y] == 1):
          self.cells[x][y] = 2
  #
  # insert(self, g, g_xmin, g_xmax, g_ymin, g_ymax) -- returns NULL
  #
  def insert(self, g, g_xmin, g_xmax, g_ymin, g_ymax):
    """
    Write the seed into the Golly grid at a random location
    within the given bounds.
    g = the Golly universe
    s = a seed
    """
    step = 1
    g_xstart = rand.randrange(g_xmin, g_xmax - self.xspan, step)
    g_ystart = rand.randrange(g_ymin, g_ymax - self.yspan, step)
    for s_x in range(self.xspan):
      for s_y in range(self.yspan):
        g_x = g_xstart + s_x
        g_y = g_ystart + s_y
        s_state = self.cells[s_x][s_y]
        g.setcell(g_x, g_y, s_state)
  #
  # random_rotate(self) -- returns new_seed
  #
  def random_rotate(self):
    """
    Randomly rotate and flip the given seed and return a new seed.
    """
    rotation = rand.randrange(0, 4, 1) # 0, 1, 2, 3
    flip = rand.randrange(0, 2, 1) # 0, 1
    new_seed = copy.deepcopy(self)
    # rotate by 90 degrees * rotation (0, 90, 180 270)
    new_seed.cells = np.rot90(new_seed.cells, rotation) 
    if (flip == 1):
      # flip upside down
      new_seed.cells = np.flipud(new_seed.cells)
    new_seed.xspan = new_seed.cells.shape[0]
    new_seed.yspan = new_seed.cells.shape[1]
    return new_seed
  #
  # fitness(self) -- returns fitness
  #
  def fitness(self):
    """
    Calculate a seed's fitness from its history. 
    """
    history = self.history
    return sum(history) / len(history)
  #
  # mutate(self, prob_grow, prob_flip, prob_shrink, seed_density, mutation_rate) 
  # -- returns mutant
  #
  def mutate(self, prob_grow, prob_flip, prob_shrink, seed_density, mutation_rate):
    """
    Make a copy of self and return a mutated version of the copy.
    """
    #
    mutant = copy.deepcopy(self)
    #
    # prob_grow     = probability of invoking grow()
    # prob_flip     = probability of invoking flip_bits()
    # prob_shrink   = probability of invoking shrink()
    # seed_density  = target density of ones in an initial random seed
    # mutation_rate = probability of flipping an individual bit
    #
    assert prob_grow + prob_flip + prob_shrink == 1.0
    #
    uniform_random = rand.uniform(0, 1)
    #
    if (uniform_random < prob_grow):
      # this will be invoked with a probability of prob_grow
      mutant.grow(seed_density) 
    elif (uniform_random < (prob_grow + prob_flip)):
      # this will be invoked with a probability of prob_flip
      mutant.flip_bits(mutation_rate)
    else:
      # this will be invoked with a probability of prob_shrink
      mutant.shrink()
    # erase the parent's history from the child
    pop_size = len(self.history)
    mutant.history = np.zeros(pop_size, dtype=np.float)
    return mutant
  #
  # flip_bits(self, mutation_rate) -- returns NULL
  #
  def flip_bits(self, mutation_rate):
    """
    Mutate a seed by randomly flipping bits. Assumes the seed
    contains 0s and 1s.
    """
    num_mutations = 0
    for s_x in range(self.xspan):
      for s_y in range(self.yspan):
        if (rand.uniform(0, 1) < mutation_rate):
          # flip cell value: 0 becomes 1 and 1 becomes 0
          self.cells[s_x][s_y] = 1 - self.cells[s_x][s_y]
          # count the number of mutations so far
          num_mutations = num_mutations + 1
    # force a minimum of one mutation -- there is no value
    # in having duplicates in the population
    if (num_mutations == 0):
      s_x = rand.randrange(self.xspan)
      s_y = rand.randrange(self.yspan)
      self.cells[s_x][s_y] = 1 - self.cells[s_x][s_y]
  #
  # shrink(self) -- returns NULL
  #
  def shrink(self):
    """
    Randomly remove rows or columns from a seed.
    """
    # first we need to decide how to shrink
    choice = rand.choice([0, 1, 2, 3])
    # now do it
    if ((choice == 0) and (self.xspan > mparam.min_s_xspan)):
      # delete first row
      self.cells = np.delete(self.cells, (0), axis=0) 
    elif ((choice == 1) and (self.xspan > mparam.min_s_xspan)):
      # delete last row
      self.cells = np.delete(self.cells, (-1), axis=0) 
    elif ((choice == 2) and (self.yspan > mparam.min_s_yspan)):
      # delete first column
      self.cells = np.delete(self.cells, (0), axis=1) 
    elif ((choice == 3) and (self.yspan > mparam.min_s_yspan)):
      # delete last column
      self.cells = np.delete(self.cells, (-1), axis=1) 
    # now let's update xspan and yspan to the new size
    self.xspan = self.cells.shape[0]
    self.yspan = self.cells.shape[1]
    #
  #
  # grow(self, seed_density) -- returns NULL
  #
  def grow(self, seed_density):
    """
    Randomly add or remove rows or columns from a seed. Assumes 
    the seed contains 0s and 1s.
    """
    # - first we need to decide how to grow
    choice = rand.choice([0, 1, 2, 3])
    # - now do it
    if (choice == 0):
      # add a new row before the first row
      self.cells = np.vstack([np.zeros(self.yspan, dtype=np.int), self.cells])
      # initialize the new row with a density of approximately seed_density
      for s_y in range(self.yspan):
        if (rand.uniform(0, 1) < seed_density):
          self.cells[0][s_y] = 1
      #
    elif (choice == 1):
      # add a new row after the last row
      self.cells = np.vstack([self.cells, np.zeros(self.yspan, dtype=np.int)])
      # initialize the new row with a density of approximately seed_density
      for s_y in range(self.yspan):
        if (rand.uniform(0, 1) < seed_density):
          self.cells[-1][s_y] = 1
      #
    elif (choice == 2):
      # add a new column before the first column
      self.cells = np.hstack([np.zeros((self.xspan, 1), dtype=np.int), self.cells])
      # initialize the new column with a density of approximately seed_density
      for s_x in range(self.xspan):
        if (rand.uniform(0, 1) < seed_density):
          self.cells[s_x][0] = 1
      #
    elif (choice == 3):
      # add a new column after the last column
      self.cells = np.hstack([self.cells, np.zeros((self.xspan, 1), dtype=np.int)])
      # initialize the new column with a density of approximately seed_density
      for s_x in range(self.xspan):
        if (rand.uniform(0, 1) < seed_density):
          self.cells[s_x][-1] = 1
      #
    #
    # now let's update xspan and yspan to the new size
    self.xspan = self.cells.shape[0]
    self.yspan = self.cells.shape[1]
    #
  #
  # count_ones(self) -- returns number of ones in a seed
  #
  def count_ones(self):
    """
    Count the number of ones in a seed.
    """
    count = 0
    for x in range(self.xspan):
      for y in range(self.yspan):
        if (self.cells[x][y] == 1):
          count = count + 1
    return count
  #
  # density(self) -- returns density of ones in a seed
  #
  def density(self):
    """
    Calculate the density of ones in a seed.
    """
    return self.count_ones() / float(self.xspan * self.yspan)
  #
#
#
#