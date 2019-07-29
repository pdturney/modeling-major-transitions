

Model-T -- Modeling Major Transitions in Evolution with the Game of Life
========================================================================

Peter Turney
July 8, 2019

Model-T is a tool for modeling the major transitions in evolution.
Model-T is implemented as a set of Python scripts that work with the Golly 
software for the Game of Life.

This document describes how to install and run Model-T in Windows 10.
With some changes, you should also be able to run Model-T in Linux
or Mac OS.


Background Reading
==================

The Major Transitions in Evolution:

- https://en.wikipedia.org/wiki/The_Major_Transitions_in_Evolution

Conditions for Major Transitions in Biological and Cultural Evolution:

- http://www.alife.org/workshops/oee3/papers/turney-oee3-final.pdf


Installing Model-T
==================

(1) Download and Install Golly

Golly is a C++ program for the simulation of cellular automata:

- https://en.wikipedia.org/wiki/Golly_(program)

I used the 64-bit version of Golly 3.2 for Windows 10 
(golly-3.2-win-64bit.zip):

- http://golly.sourceforge.net/
- https://sourceforge.net/projects/golly/files/golly/golly-3.2/
  
Golly is stored in a zip file. I created a directory called Golly64
and put the contents of the zip file in this directory:

- C:\Users\peter\Golly64


(2) Download and Install Python

Golly can be extended with scripts written in Python or Lua. Model-T is
a set of Python scripts that run with Golly.

I used Python 2.7 for Windows. Golly 3.2 is designed to work with Python 2.X
but not Python 3.X. Here is some information on using Python with Golly:

- http://golly.sourceforge.net/Help/python.html


(3) Download and Install Numpy and Statistics

Numpy provides Python numerical functions needed by Model-T. After Python
has been installed, Numpy can be installed in Windows 10 by opening a
command prompt and executing the following commands:

> cd \Python27\Scripts
> pip install numpy
> pip install statistics


(4) Download and Install Model-T

Create a subdirectory of your Golly directory and put the Model-T files
in this subdirectory. In my case, the Model-T files are in this
directory:

- C:\Users\peter\Golly64\Model-T

Golly needs to know where to find the rules for the Immigration game.
The rules are in the file Immigration.rule in the Model-T files.
Start Golly and navigate through the Golly menu system as follows:

- File > Preferences > Control > Your Rules ...

Click on "Your Rules ..." and enter the Model-T directory:

- C:\Users\peter\Golly64\Model-T


(5) Adjust Windows 10 Antimalware Service

Windows 10 Antimalware Service wastes a lot of CPU time checking Golly
for malware, whenever Golly is executing. To free up your CPU, tell the
Antimalware Service not to check Golly:

- open Windows Defender Security Center
- select Virus & threat protection
- select Virus & threat protection settings
- select Add or remove exclusions
- add the Golly process (Golly.exe)


(6) Adjust Windows 10 Update Policy

Windows 10 will periodically install updates and restart the computer
without asking for permission. This will terminate an ongoing simulation
prematurely. To prevent this, you need to use the Windows Group Policy
Editor, which is available in Windows 10 Pro, but not in Windows 10 Home.
If you have Windows 10 Home, it is worthwhile to upgrade to Windows 10 Pro.
Here is information about how to set the Windows Group Policy Editor
to prevent termination of a simulation run:

- https://docs.microsoft.com/en-us/windows/deployment/update/waas-restart

I set my group policy as follows:

- Local Computer Policy > Computer Configuration > Administrative Templates
  > Windows Components > Windows Update
- Configure Automatic Updates = Enabled = 2 = Notify before downloading
  and installing any updates
- No auto-restart with logged on users for scheduled automatic updates
  instalations = Enabled
  

Running Model-T
===============

(1) run_model.py -- run a simulation; evolve a population

The main routine for running Model-T is run_model.py. It uses the
supporting code in model_classes.py, model_functions.py, and
model_parameters.py. It also uses the rules for the Immigration
Game, in the file Immigration.rule.

To run Model-T, start Golly and then open the Model-T folder in the 
left panel of Golly. Click on run_model.py to start the simulation. 
You can control the behaviour of the simulation by editing the
numbers in the parameter file, model_parameters.py, before you
start Golly. 

When Golly is running, the Golly screen will show the final outcome of
each Immigration game that is played. The intermediate stages of the 
games are not displayed, in order to maximize the speed of the simulation. 
If you want a more detailed view of an individual game, use the
script view_contest.py. A typical simulation run takes about two to
six days for 100 generations, depending on the speed of the computer
and the settings of the parameters.

As run_model.py executes, it stores a log file with some statistics
from the run. It also stores samples (pickles) of individuals that 
evolve during the run. The directory where these files are stored, 
log_directory, is specified in model_parameters.py. You should
create a folder for storing the files and edit model_parameters.py
so that log_directory points to your desired folder.


(2) compare_generations.py -- compare populations across generations

As a simulation runs, Model-T stores samples of the population for each
generation. After the simulation ends, compare_generations.py can 
compare samples across different generations. Individuals in an
earlier generation will compete with individuals in a later generation
in repeated Immigration Games. In general, we expect that individuals
in the later generation will perform better than individuals in an
earlier generation.

To run compare_generations.py, start Golly and open the Model-T folder 
in the  left panel of Golly, then click on compare_generations.py.


(3) compare_random.py -- compare populations with random individuals

After a simulation ends, compare_random.py can compare samples from
a run by having them compete against randomly generated individuals.
For a given individual from a run, the competitor is an individual
with the same dimensions (the same number of rows and columns) and
the same density (the same ratio of 1s to 0s). The competitor is
generated by randomly shuffling the cells of the given individual 
from the simulation run. This ensures that the outcome of the
competition is based on the structure of the individual (the
pattern of the 0s and 1s) and not on the size or density of the
individual. 


(4) compare_types.py -- compare populations with different parameters

Two different simulation runs, based on different parameter settings,
can be compared with compare_types.py. Individuals in generation N of
one run are compared with individuals in generation N of another run.


(5) measure_areas.py -- calculate the average areas of individuals

After a simulation ends, measure_areas.py can examine samples to
calculate their areas (the number of rows times the number of columns).
In general, we expect the areas to grow over the generations.


(6) measure_densities.py -- calculate the average densities

After a simulation ends, measure_densities.py can examine samples to
calculate their densities (the number of 1s divided by the area).
We expect that a relatively narrow range of densities will be
preferred.


(7) measure_diversities.py -- calculate the standard deviation of fitness

After a simulation ends, measure_diversities.py can examine samples
to calculate the standard deviation of the fitness in the samples, which
gives an indication of how much diverity there is in the samples.


(8) view_contest.py -- see an Immigration Game played

After a simulation ends, view_contest.py allows the user to pick
samples and have individuals from the samples compete against
each other in an Immigration Game. This may provide some
insight into the nature of the game and the nature of the
indivuals that evolve in the simulation.

