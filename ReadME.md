# Model Purpose
The purpose of this model is to explore the interactions and effects of predation risk, foraging efficiency, food availability, and reciprocal pilferage on the evolution of scatterhoarding behavior. We designed our model as a modified version of the model presented by Vander Wall and Jenkins (2003). Scatterhoarding habits in this model were modeled after the behaviors of eastern gray squirrels (_Sciurus carolinensis_) based on previous studies and personal experience with prior research on the species. This model was coded using Python 3.11.0.

## Model Summary
### The population: hoarders vs. nonhoarders
A population of 20 squirrels (a mix of hoarders and nonhoarders) each have up to 20 foraging bouts each day for 100 days (i.e., 1 season). Hoarding individuals will either eat their own stored food, if available, or eat the first food item they find then continue to forage and store subsequent food items found. Nonhoarding individuals will eat the first food item they find they will not have any more foraging bouts until the next day. Nonhoarders can always steal hoarded food from hoarders, however, hoarders may not always be capable of stealing hoarded food from other hoarders (depending on user-defined model parameters).

### Foraging for food
Storable food is added to the public food supply at the beginning of the first day of each season (i.e., acorns falling to the ground). Each day, surviving individuals forage in a different random order each foraging bout. During each foraging bout, a detection probability is calculated to determine if the squirrel finds food to harvest. If the squirrel detects food to harvest, the food item is defined as either public storable food or food already stored by other hoarders, based on proportions of each type available. If public food is detected, squirrel eats or stores the food (based on satiation and hoarding ability). If the squirrel detected stored food, they steal from another hoarder, depending on proportions of food stored by each other hoarder.

### Mortality risk
After the individual's foraging bout is completed by eating or storing food, the individual faces predation risk. Additionally, if a squirrel does not eat 1 food item by the end of the day, they starve and die.

### The next generation
At the end of 100 day season, individuals of the next generation completely show the hoarding or nonhoarding trait of one randomly selected survivor. Survivors are chosen to create individuals of the new generations until the population is full (i.e., 20 individuals in the new generation). Each generation of the population is completely new, survivors from the previous generation do not remain in the population. The population cycles through seasons and generations until either hoarding or nonhoarding fixates (i.e., the other trait dies out) or the population goes extinct.

## Manipulatable variables for each population
These variables can either be found under the first two function in a section called "Define variables for starting the model", or within the last function of the model.

### Defining the population
These variables are used to define the inherent characteristics of the population represented within the model.
* Number of individuals in the population: any continuous number
* Number of hoarders: continuous number of hoarders; rest of population will be defined as nonhoarders
* Reciprocal pilferage: Hoarders either can or cannot steal (i.e., reciprocally pilfer) hoarded food from other hoarders. Nonhoarders can always pilfer.
* Foraging efficiency: number 0 - 1, used to define how easy food it to find based on how much food is available

### Defining the environment
These variables are used to define the environmental variables of the model.
* Mast crop: The total number of storable food available at the beginning of the season (found in the last function of the model code)
* Predation risk: The probability of predation mortality each individual faces after foraging

### Defining the model
These variables are used to define how long each season is and how many times the initial parameters for the population will be run to fixation or extinction.
* Total days in season: any continuous number
* Runs: continuous number of times model is run with same population conditions
*** Runs where many individuals survive each generation take a lot of time and memory. More runs will add more time and more memory.

## How to run the model
The function used to define mast crop, foraging efficiency and run the model is the very last function: run_fun(). 
* change the numbers in brackets as needed for:
	* mast_crop (storable food available at beginning)
	* pub_for_eff (foraging efficiency)
You can add multiple numbers separated by commas (,) to have model run through all combinations of all variables.
* <b>Run the model using the code "run_fun()". The model can also be running by defining the population variables as desired and then using Python to run the script.</b>


## End of a run of the model
At either trait fixation or extinction of the popoulation, the model outputs a csv. file with the following characteristics of the population:
* Run number
* Generations until end of run
* Hoarder trait fixated in population (1 = yes, 0 = no)
* Nonhoarder trait fixated in population (1 = yes, 0 = no)
* Population went extinct (1 = yes, 0 = no)
* Number of hoarders in beginning population
* Predation risk
* Foraging efficiency
* Number of storable food items available at beginning of model
* Ability of hoarders to pilfer (1 = yes, 0 = no)

## Contact Information:
This model was created by Sarah Ramirez and Todd Steury. For questions, comments, or permission to use the model, please email: sramirez26@wisc.edu.
