Model Summary

* Storable food added to the public food supply at the beginning of the first day (i.e., acorns falling to the ground). 
* A population of 20 squirrels (a mix of hoarders and nonhoarders) each have up to 20 foraging bouts each day for 100 days (i.e., 1 season).
* Hoarding individuals will either eat their own stored food, if available, or eat the first food item they find then continue to forage and store subsequent food items found.
* Nonhoarding individuals will eat the first food item they find they will not have any more foraging bouts until the next day.

* Each day, surviving squirrels are all chosen to forage in a random order. 
* When a squirrel forages, a detection probability is calculated and if a random number is less than that prob, the squirrel finds food to harvest. 
* If detection prob < random number, the squirrel is marked as foraged and the next squirrel forages. 
* If the squirrel detects food to harvest, it is defined as either public food or food stored by other hoarders, based on amount of each available. 
* If public food is detected, squirrel eats or stores the food (based on satiation and hoarding ability).
* If the squirrel detected stored food, they steal from another hoarder, depending on proportions of food stored by each other hoarder.
* After the individual's foraging bout is completed with eating ot storing food, the individual faces predation risk. 
* If a squirrel does not eat 1 food item by the end of the day, they starve and die.
* At the end of 100 days, surviving individuals are randomly chosen to create the next generation of 20 individuals.
* Individuals of the next generation completely show the hoarding or nonhoarding trait of one selected survivor.
* The population cycles through seasons and generations until either hoarding or nonhoarding fixates (i.e., the other trait dies out) or the population goes extinct.



Manipulatable variables for each population
UNDER "### Define variables for starting the model"
Defining the population
* Number of individuals in the population: any continuous number
* Number of hoarders: continuous number of hoarders; rest of population will be defined as nonhoarders
* Reciprocal pilferage: Hoarders either can or cannot steal (i.e., reciprocally pilfer) hoarded food from other hoarders. Nonhoarders can always pilfer.
* Foraging efficiency: number 0 - 1, used to define how easy food it to find based on how much food is available

Defining the environment
* Mast crop: The total number of storable food available at the beginning of the season
* Predation risk: The probability of predation mortality each individual faces after foraging

Defining the model
* total days in season: any continuous number
* Runs: continuous number of times model is run with same population conditions
*** runs where many individuals survive each generation take a lot of time and memory. More runs will add more time and more memory.

How to run the model
last function: run_fun
* change the numbers in brackets as needed for:
	*mast_crop (storable food available at beginning)
	*pub_for_eff (foraging efficiency)
* can add multiple numbers separated by commas (,) to have model run through all combinations of all variables.


End of a run of the model
* At either trait fixation or extinction of the popoulation, the model outputs a csv. file with the following characteristics of the population:
	*run number
	*generations until end of run
	*hoarder trait fixated in population (1 = yes, 0 = no)
	*nonhoarder trait fixated in population (1 = yes, 0 = no)
	*population went extinct (1 = yes, 0 = no)
	*number of hoarders in beginning population
	*predation risk
	*foraging efficiency
	*number of storable food items available at beginning of model
	*ability of hoarders to pilfer (1 = yes, 0 = no)