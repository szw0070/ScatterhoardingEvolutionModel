#!/usr/bin/env python3

''' Model Summary.

Population of 20 squirrels each go on 20 foraging bouts each day for 100 days.
Each squirrel has a chance of predation at the end of each foraging bout.
If a squirrel does not eat 1 food item by the end of the day, they starve and die.
Storable food is produced and added to the public food supply at the beginning of 
the first day (i.e. acorns falling to the ground). If a hoarder has stored food, 
the squirrel automatically eats that and is satiated before foraging. If the 
squirrel was not able to eat anything before foraging, they eat the first food 
they find through foraging. After eating one food item each day, all other foods 
found are stored, if the animal can store food. Each day, squirrels are all chosen 
to forage in a random order. When a squirrel forages, a detection probability is 
calculated and if a random number is less than that prob, the squirrel finds food 
to harvest. If detection prob < random number, the squirrel is marked as foraged 
and the next squirrel forages. If the squirrel detected food to harvest, it's 
either public food or food stored by other hoarders, based on amount of each 
available. If public food, squirrel eats or stores the food. If the squirrel 
detected stored food, they steal from another hoarder, depending on proportions 
of food stored by each other hoarder. After foraging is completed with eating 
or storing food, they may be eaten by a predator. At the end of each days 20 
foraging bouts, if the squirrel hasn't eaten any food, it starves and dies.

'''

#Load packages needed for code.
#
#    if 'import' doesn't work;
#    use: 'pip install #package#'

import copy #to copy dict under new name to act separately
import statistics #calculate mean for inheritance
import csv #exporting to csv
import gc #garbage collecting
import sys
import random #to generate random numbers
import decimal #to specify decimal places? (might not be needed if code is changed)
import math #exponents and natural logs
import numpy as np #math with lists; making arrays
# if numpy won't import; from command prompt, run: python3 -m pip install numpy


#prevents issues with the foraging function calling itself many, many times.
sys.setrecursionlimit(500000000) 


def reset(): #restarting entire simluation; first generation of first run only
    """
    Resets variables to initial values at the beginning of a run.
    
    Restarts the entire run of the model. 
    Only used before the first generation of the first run of the model
    
    """
    global season
    global state2
    global hoarder_id
    global hoarder_stored
    global hoarder_values
    global public_food_harv
    global foragers
    global forager_id
    global _id
    global phenotype
    global phenotype2
    global pred_risk
    global fixation
    global results
    global storage_effort
    season = {'Day' : 1, 'Bout' : 0, 'Generation':1, 'Run':1}
    state2 = (pop_size)*[0] # repeated pop_size times
    hoarder_id = [*range(0,pop_size)]
    hoarder_stored = (pop_size)*[0] #0 repeated pop_size times
    nonhoarder_num = pop_size - hoarders_num #storage effort is 0
    storage_effort_h = [1]*hoarders_num #repeats 1, for the number of hoarders
    storage_effort_nh = [0]*nonhoarder_num #repeats 0 for the number of nonhoarders
    storage_effort = []
    for i in storage_effort_h: #choose list to add to end of other list
        storage_effort.append(i) #add chosen list to end of this list
        #storage_effort is now list of hoarders
    for i in storage_effort_nh: #choose list to add to end of other list
        storage_effort.append(i) #add chosen list to end of this list
        #storage_effort is now entire list of hoarders and non hoarders
    pred_risk = pred_risk_pop + np.multiply(pred_risk_pop,storage_effort)
    hoarder_values = {'state':state2, 'id':hoarder_id, 'stored food':hoarder_stored, 
    'predation risk': pred_risk, 'storage effort':storage_effort} 
    public_food_harv = 0
    foragers = 0 #define global variable
    forager_id = -1
    _id = pop_size #for making list of survivors
    phenotype = [] #for calculating new phenotype       
    phenotype2 = [] #calculating new phenotype
    fixation = -1
    results = {'hoarder': 0, 'nonhoarder':0, 'dead':0}


def reset4(): #any first generation after first run
    """
    Resets variables to initial values for the first generation of
    any run after the first run.
    
    """
    global season
    global state2
    global hoarder_id
    global hoarder_stored
    global hoarder_values
    global public_food_harv
    global foragers
    global forager_id
    global _id
    global phenotype
    global phenotype2
    global pred_risk
    global public_food
    global public_food_tot
    global hoarders_num
    global fixation
    global results
    global storage_effort
    season['Day'] = 1
    season['Bout'] = 0
    season['Generation'] = 1
    state2 = (pop_size)*[0]
    hoarder_id = [*range(0,pop_size)]
    hoarder_stored = (pop_size)*[0]
    nonhoarder_num = pop_size - hoarders_num
    storage_effort_h = [1]*hoarders_num
    storage_effort_nh = [0]*nonhoarder_num
    storage_effort = []
    for i in storage_effort_h:
        storage_effort.append(i)
    for i in storage_effort_nh:
        storage_effort.append(i)
    pred_risk = pred_risk_pop + np.multiply(pred_risk_pop,storage_effort)
    hoarder_values = {'state':state2, 'id':hoarder_id, 'stored food':hoarder_stored, 
    'predation risk': pred_risk, 'storage effort':storage_effort} 
    public_food_harv = 0
    foragers = 0
    forager_id = -1
    _id = pop_size #for making list of survivors
    phenotype = [] #for calculating new phenotype       
    phenotype2 = [] #calculating new phenotype
    fixation = -1
    results = {'hoarder': 0, 'nonhoarder':0, 'dead':0}


### Define variables for starting the model

pop_size = 5 # number of animals in the population, always 20
days_tot = 5 # number of days in the season, always 100
runs_ = 5 #100 total for each combination of parameters

#Below variables are manipulated prior to running a specific variation of the model
pred_risk_pop = 0.0001 #population background risk, varies
SH_pilfer_ability = 1 #1 = hoarders can pilfer, 0 = hoarders cannot pilfer
hoarders_num = 1 #number of animals with storage effort of 1 (i.e., hoarders); 1, 10, or 19

#Below variables defined in function to run all code at end
days_perish = [] #days without starvation risk, defined in function to run all code
for_eff = [] #used to calculate detection probability, defined in function to run all code
mast_crop = [] #amount of storable food available starting the food day of the model

### Define starting values that are not manipulated manually
season = {'Day' : 1, 'Bout' : 0, 'Generation': 1, 'Run':1} #dictionary to keep track of time
public_food_harv = 0
foragers = 0
forager_id = -1
_id = pop_size
survivors = 0
fixation = -1 #-1 = not present, 0 = nonhoarding trait, 1 = hoarding trait
results = {'hoarder': 0, 'nonhoarder':0, 'dead':0}
detection_prob = 0
harv_foodtype = 0
public_total = -1
surv = 0
phenotype = []      
phenotype2 = []

#Creating list of different probabilities for storing vs. ignoring pilfered food.
nonhoarder_num = pop_size - hoarders_num #number of nonhoarders in the population

#Define number of animals with each type of storage effort
#Storage effort = 0 for nonhoarders and nonpilfering hoarders, 1 for pilfering hoarders
storage_effort_h = [1]*hoarders_num #repeats 1 for the number of hoarders
storage_effort_nh = [0]*nonhoarder_num #repeats 0 for the number of nonhoarders
storage_effort = [] #create empty list to add values to

for i in storage_effort_h: #choose list to add to end of other list
    storage_effort.append(i) #add chosen list to end of this list
#storage_effort is now a list of hoarders

for i in storage_effort_nh:
    storage_effort.append(i)
#storage_effort is now the full list of hoarders and non hoarders

# predation risk for each individual is a function of their storage effort
# hoarders = pred_risk_pop + pred_risk_pop; nonhoarders = pred_risk_pop
pred_risk = pred_risk_pop + np.multiply(pred_risk_pop,storage_effort) 

#hoarder_values is a dictionary used to reference values
#associated with specific animals, that consists of:
#state; 0 = satiated, -1 = hungry, 999/998 = dead
state2 = (pop_size)*[0]
#hoarder_id = individual id of each animal (hoarders and nonhoarders)
hoarder_id = list(range(0,pop_size))
#hoarder_stored = number of food items currently stored by each animal
hoarder_stored = (pop_size)*[0]

hoarder_values = {'state':state2, 'id':hoarder_id, 'stored food':hoarder_stored, 
    'predation risk': pred_risk, 'storage effort':storage_effort}


def choose_forager():
    ''' 
    This function chooses a new random foraging order for all animals.

    Run after each animal forages to see if all animals have foraged yet.
    If all animals have foraged, a new random order is created for all 
    animals in the population to forage. The next foraging bout begins.
    All animals are reset to not having foraged yet that bout. 
    
    Returns:
    foragers: dictionary with new randomly ordered list of all animals
    in the population and 0s for foraging status (indicating they have
    not foraged yet)
    '''
    global forager_id
    global foragers
    if forager_id == -1: #nobody has foraged, it's the start of a new bout
        rand_forage = random.sample(hoarder_id,pop_size) #create random list of foragers without replacement
        forage_status = [0]*pop_size #will indicate animal has not yet foraged this bout
        foragers = {'hoarder':rand_forage, 
        'foraged':forage_status} #dictionary for ease of calling variables      
        forager_id = 0 #start with first forager in order
        season['Bout'] += 1 # move to the next bout


def fun(hoarders_num, days_perish, mast_crop, for_eff):
    '''
    This function allows animals to forage.

    Determines if animals have foraged yet and passes them to the next appropriate
    function to determine if they are hungry, detect food, or to finish the generation
    at the end of a season. Moves to the next day after all individuals
    have foraged during a day. This function calls on itself many times in order
    to cycle through 100 days of 20 foraging bouts per 20 individuals.
    
    Attributes:
    hoarders_num ############################ DON'T THINK THIS IS NEEDED ANYMORE
    days_perish: number of days at the beginning of each season when perishable food is available
    mast_crop: total number of storable food items available at the beginning of each season
    for_eff: foraging efficiency of all individuals in the population
    ''' 
    global forager_id
    global foragers
    global season 
    choose_forager()
    if forager_id < pop_size: #if the forager is in the population 
        if hoarder_values['state'][foragers['hoarder'][forager_id]] < 1: #if state of forager identified by forager_id is alive
            if foragers['foraged'][forager_id] == 0: #and if they HAVEN'T foraged yet
                foragers['foraged'][forager_id] += 1 #then define them as foraged,
                if season['Bout'] == 1: #if it's the first bout of the day
                    state() #determine state based on perishable and stored food
                detect() #and let them continue foraging
            elif foragers['foraged'][forager_id] == 1: #or if they HAVE already foraged
                forager_id = forager_id + 1 #set forager to next hoarder in the order
                fun(hoarders_num, days_perish, mast_crop, for_eff)
        elif hoarder_values['state'][foragers['hoarder'][forager_id]] > 1: #or if they are dead
            forager_id = forager_id + 1 #set forager to next animal in the order
            fun(hoarders_num, days_perish, mast_crop, for_eff)
    #End of the day or bout:
    elif forager_id == pop_size: #if the forager is not in the population (all have foraged that bout)
        if season['Bout'] == 20: #and it's the last bout of the day
            if season['Day'] == days_tot: #and it's the last day of the season
                next_gen() #find survivors, check for fixation, check runs
            elif season['Day'] < days_tot: 
                season['Day'] += 1
                season['Bout'] = 0
                forage_status = [0]*pop_size 
                foragers['foraged'] = forage_status #reset all foragers to not foraged yet
                forager_id = -1 #reset to to able to choose new order
                fun(hoarders_num, days_perish, mast_crop, for_eff)
        elif season['Bout'] < 20: #but if it's not the last bout of the day
            forage_status = [0]*pop_size
            foragers['foraged'] = forage_status #reset all foragers to not foraged yet
            forager_id = -1 #reset to be able to choose new order            
            fun(hoarders_num, days_perish, mast_crop, for_eff)


def state(): #define forager's state based on available food
    ''' 
    Defines state of each individual as satiated, hungry, or dead.
    
    Other functions can define state as 998 for starvation mortality 
    and 999 for predation mortality. If the animal is alive, this 
    function checks for available food and determines if they are 
    satiated or hungry. If there is perishable food available, 
    the animal will be satiated (state = 0). If there is no perishable food, 
    but the animal has stored food available, the animal will be 
    satiated (state = 0). If neither food type is available, the 
    animal will be defined as hungry (state  = -1).
    '''
    global forager_id
    global hoarder_values
    #if perishable food or stored food is available to eat,
    if season['Day'] <= days_perish or hoarder_values['stored food'][foragers['hoarder'][forager_id]] > 0: 
    #if the forager is alive,
        if hoarder_values['state'][foragers['hoarder'][forager_id]] < 995: 
    #forager is satiated
            hoarder_values['state'][foragers['hoarder'][forager_id]] = 0 
    #if no perishable food and no stored food is avilable to eat
    elif season['Day'] > days_perish and hoarder_values['stored food'][foragers['hoarder'][forager_id]] == 0:
    #if the forager is alive,
        if hoarder_values['state'][foragers['hoarder'][forager_id]] < 995: 
    #forager is hungry
            hoarder_values['state'][foragers['hoarder'][forager_id]] = -1 


def detect():
    ''' 
    Determines amount of food available and calculates detection probability.
    
    This function calculates how much food (both stored and not yet stored) is available
    to harvest and then calculates the detection probability using the animal's foraging effiency 
    and the total number of available food items. When calculating available food, items 
    stored by the current forager are not included in the total value. If there is available
    food, the detection probability is calculated and the harvest_event function is 
    called for the animal to continue foraging. If there is no food available, the predation
    function is called to determine mortality due to starvation or predation.
    '''
    global forager_id
    global detection_prob
    global mast_crop
    global food_avail
    global public_food
    global other_SH
    total_stored = sum(hoarder_values['stored food']) #find total number of seeds stored by all animals
    other_SH = total_stored - hoarder_values['stored food'][foragers['hoarder'][forager_id]] #find food hoarded by others animals
    public_food = mast_crop - public_food_harv # total mast not yet eaten or stored
    food_avail = public_food + other_SH #total storable food items available to locate or pilfer
    if food_avail == 0:  #if there IS NOT food left to harvest or pilfer
        predation()
    elif food_avail > 0: #if there IS storable food left to harvest or pilfer
        #detection_prob = 1 - ((1 - pub_for_eff)**(public_food))*((1 - pilf_for_eff)**(other_SH))
        # ^^^ different probabilities of finding public food vs scatterhoarded food
        detection_prob = 1 - (1 - for_eff)**food_avail #probability of finding a particular food item
        # ^^^ all food is equally as easy to find (public and hoarded)
        harvest_event()
    

def harvest_event(): #determine if detected food is harvested
    ''' 
    This function determines if food is detected and then calls either
    the harvest_item function to continue foraging, or the predation
    function to end the foraging bout and determine mortality.

    '''
    harv_rand = random.random() #generates 0.#### number between 0 and 1
    if detection_prob > harv_rand: #item IS harvested
        harvest_item() #determine what type of food is harvested
    else: #item is NOT harvested
        #foraging bout is over for this individual; need to check for predator motality
        predation()


def harvest_item(): #determine which item is harvested
    ''' 
    This function determines if unstored food (e.g., public food) is harvested 
    or stored food is pilfered.
    
    '''
    global public_food_harv
    global forager_id
    global harv_foodtype
    global public_total
    total_stored = sum(hoarder_values['stored food']) #find total stored seeds
    other_SH = total_stored - hoarder_values['stored food'][foragers['hoarder'][forager_id]] #find food hoarded by others
    public_total = mast_crop - public_food_harv #total public food currently available
    if other_SH > 0: #if any seeds are stored 
        other_SH_prop = other_SH / (other_SH + public_total)
        public_prop = public_total / (other_SH + public_total)
        food_prop = [public_prop, other_SH_prop]
        food_types = [0,1] # 0 = public; 1 = hoarded
        #choose food type to harvest based on proportions of public and hoarded
        harv_foodtype = random.choices(food_types, weights=food_prop,k=1)
    elif other_SH == 0: #if there are no seeds stored
        harv_foodtype = [0] #public food is automatically harvested
    food_fate()
    

def food_fate():
    '''
    This function determines if harvested food is eaten, stored, or ignored.
    
    If the animal is hungry, they always eat the food item and become satiated for the day.
    If already satiated, a hoarder can store public food, while a nonhoarders will always ignore it.
    If stored food is pilfered, actions depend on whether the animal can pilfer food or not.
    Those that can pilfer can either eat or store pilfered food. Those that cannot pilfer will ignore
    pilfered food.

    '''
    global public_food_harv
    global harv_foodtype
    global public_total
    global mast_crop #total amount of storable food available at beginning of season
    if harv_foodtype == [0]: #if harvested food is public
        public_total = mast_crop - public_food_harv #public food currently available
        if public_total > 0: #if there is public food available
            if hoarder_values['state'][foragers['hoarder'][forager_id]] == -1: #if forager is hungry
                public_food_harv = public_food_harv + 1 
                hoarder_values['state'][foragers['hoarder'][forager_id]] = 0 #forager is satiated
            elif hoarder_values['state'][foragers['hoarder'][forager_id]] == 0: #if forager is satiated
                if hoarder_values['storage effort'][foragers['hoarder'][forager_id]] == 1: #if animal can store food
                    hoarder_values['stored food'][foragers['hoarder'][forager_id]] += 1 #food item is stored
                    public_food_harv = public_food_harv + 1    
                elif hoarder_values['storage effort'][foragers['hoarder'][forager_id]] == 0: #if animal CANNOT store food
                    pass #seed is ignored
        else:
            pass #there is no public food available
    if harv_foodtype == [1]: #if harvested food is stored
        #copy hoarder values dictionary to new variable to manipulate
        hoarders = copy.deepcopy({'id':hoarder_values['id'],'stored food': hoarder_values['stored food']})
        del hoarders['id'][foragers['hoarder'][forager_id]] #remove current forager id from dictionary
        del hoarders['stored food'][foragers['hoarder'][forager_id]] #remove current forager's stored items from dictionary
        pilf = random.choices(hoarders['id'], weights=hoarders['stored food'],k=1) #select from other hoarders weighted by seeds stored
        pilf1 = pilf[0] #pull hoarder value from list
        if hoarder_values['storage effort'][foragers['hoarder'][forager_id]] == 0 or (hoarder_values['storage effort'][foragers['hoarder'][forager_id]] == 1 and SH_pilfer_ability == 1): 
        # ^ if forager is a cheater or pilfering hoarder
        # they eat pilfered food if they are hungry
            if hoarder_values['state'][foragers['hoarder'][forager_id]] == -1: #if forager is hungry
                hoarder_values['stored food'][pilf1] -= 1 #take 1 food item from hoarder's food supply for pilferage
                hoarder_values['state'][foragers['hoarder'][forager_id]] = 0 #forager is satiated
        # they recache pilfered food if they are satiated
            elif hoarder_values['state'][foragers['hoarder'][forager_id]] == 0: #if forager is satiated
                if hoarder_values['storage effort'][foragers['hoarder'][forager_id]] == 1: #if animal can store food
                    hoarder_values['stored food'][pilf1] -= 1 #take 1 food item from owners's food supply for pilferage
                    hoarder_values['stored food'][foragers['hoarder'][forager_id]] += 1 #food item is stored by pilfering forager       
                elif hoarder_values['storage effort'][foragers['hoarder'][forager_id]] == 0: #if animal CANNOT store food
                    pass #seed is ignored, nothing happens
        elif hoarder_values['storage effort'][foragers['hoarder'][forager_id]] == 1 and SH_pilfer_ability == 0: #if forager is a hoarder and NOT able to pilfer
            pass #do nothing, forager cannot pilfer
    predation()


def predation():
    '''
    This function determines mortality due to starvation or predation.
    
    Animals face the risk of predation each foraging bout. If they die,
    their state is set to 999. At the end of each day, animals are checked
    for starvation. If they had not eaten a food item that day, they
    starve and their state is set to 998.

    Commented out blocks of code can be used to record survival data.
    '''
    global forager_id
    global hoarders_num
    global days_perish
    global mast_crop
    global for_eff
    global public_total
    global hoarder_values
    global foragers
    if season['Bout'] == 20: # if its the last bout of the day
    # on the last bout of the day, any starving animals will die after their attempt to forage
        if hoarder_values['state'][foragers['hoarder'][forager_id]] == -1: #and if forager is starving on the last bout of the day
            hoarder_values['state'][foragers['hoarder'][forager_id]] = 998 #forager dies from starvation
            #   input_variable = [season['Run'], # run number
            #   [foragers['hoarder'][forager_id]], #hoarder id
            #   hoarder_values['storage effort'][foragers['hoarder'][forager_id]], #hoarder or nonhoarder
            #   season['Day'], hoarder_values['state'][foragers['hoarder'][forager_id]], #day of event, event type
            #   1, 0, 1, #censor_starve, censor_pred, censor_dead
            #   hoarders_num, pred_risk_pop, detection_prob, food_avail, for_eff, 
            #   days_perish, mast_crop, SH_pilfer_ability]
            #   print(input_variable) #mort data for those that starve
        elif -1 < hoarder_values['state'][foragers['hoarder'][forager_id]] < 995: # if the forager is alive
            pred_rand = random.random() #generate random number between 0 and 1
            if pred_rand < hoarder_values['predation risk'][foragers['hoarder'][forager_id]]: #if random number is less than forager's predation risk
                hoarder_values['state'][foragers['hoarder'][forager_id]] = 999 #forager is now dead from predation
             #   input_variable2 = [season['Run'], # run number
             #   [foragers['hoarder'][forager_id]], #hoarder id
             #   hoarder_values['storage effort'][foragers['hoarder'][forager_id]], #hoarder or nonhoarder
             #   season['Day'], hoarder_values['state'][foragers['hoarder'][forager_id]], #day of event, event type
             #   0, 1, 1, #censor_starve, censor_pred, censor_dead
             #   hoarders_num, pred_risk_pop, detection_prob, food_avail, for_eff, 
             #   days_perish, mast_crop, SH_pilfer_ability]
             #   print(input_variable2) #mort data for those that are eaten by predators
    else: #if it is not the last bout of the day
        if hoarder_values['state'][foragers['hoarder'][forager_id]] < 995: # if the forager is alive (starving doesn't matter)
            pred_rand = random.random() #generate random number between 0 and 1
            if pred_rand < hoarder_values['predation risk'][foragers['hoarder'][forager_id]]: #if random number is less than forager's predation risk
                hoarder_values['state'][foragers['hoarder'][forager_id]] = 999 #forager is now dead from predation
            #    input_variable3 = [season['Run'], # run number
            #    [foragers['hoarder'][forager_id]], #hoarder id
            #    hoarder_values['storage effort'][foragers['hoarder'][forager_id]], #hoarder or nonhoarder
            #    season['Day'], hoarder_values['state'][foragers['hoarder'][forager_id]], #day of event, event type
            #    0, 1, 1, hoarders_num, pred_risk_pop, detection_prob, food_avail, for_eff, #censor_starve, censor_pred, censor_dead
            #    days_perish, mast_crop, SH_pilfer_ability]
            #    print(input_variable3) #mort data for those that are eaten
        else: # random number is larger; they survive the predator attack
            pass
           # if season['Day'] == days_tot: #if its the last day of the season
           #     ## write to Mortality data file for animals still alive at the end of the season
           #     input_variable4 = [season['Run'], # run number
           #     [foragers['hoarder'][forager_id]], #hoarder id
           #     hoarder_values['storage effort'][foragers['hoarder'][forager_id]], #hoarder or nonhoarder
           #     season['Day'], hoarder_values['state'][foragers['hoarder'][forager_id]], #day of event, event type
           #     0, 0, 0, #censor_starve, censor_pred, censor_dead
           #     hoarders_num, pred_risk_pop, detection_prob, food_avail, for_eff, 
           #     days_perish, mast_crop, SH_pilfer_ability]
           #     print(input_variable4) #animals that survive the last day of the season
           # else: #it's not the last day of the season
           #     pass #forager escapes predation and survives to the next bout
    forager_id = forager_id +1 ###### added 3-26-23, move to the next forager
    fun(hoarders_num, days_perish, mast_crop, for_eff) #restart foraging function


# end the model if an entire generation dies
def checkIfDuplicates_1(): #check for duplicates
    '''
    This funciton checks all animals at the end of a season to
    see if all animals died.
    
    Returns:
    surv: variable is set to -1 if population went extinct or 0 if there were survivors.
    '''
    global surv
    if set(hoarder_values['state']) == {999,998} or set(hoarder_values['state']) == {999} or set(hoarder_values['state']) == {998}: #if the entire population died
        surv = -1
    else:
        surv = 0 #there are survivors


def checkIfDuplicates_trait():
    '''
    This function checks to see if either nonhoarding or hoarding had fixated at the end of the season.
    
    Returns:
    fixation: -1 (no fixation), 0 = nonhoarding, 1 = hoarding
    '''
    global fixation
    if set(survivors['storage effort']) == {0}: #if the entire population are nonhoarders
        fixation = 0 #nonhoarding trait has evolved
    elif set(survivors['storage effort']) == {1}:
        fixation = 1 #hoarding trait has evolved

    
def next_gen():
    '''
    This function creates a list of survivors from the season that just ended.
    
    If there are no survivors, this population is recorded as extinct and either the
    model ends or moves to the next run. If there are survivors, a list is created
    of the surviors and if they were hoarders or nonhoarders. The offspring 
    function is then called to create a new generation and continue the run
    with a new season. If the previous population fixated with either
    hoarding or nonhoarding behavior, that is recorded and the model run is ended.
    '''
    global hoarder_values
    global _id
    global survivors
    global surv
    global fixation
    global results
    global hoarders_num
    global days_perish
    global mast_crop
    global for_eff
    global runs_
    checkIfDuplicates_1() #check to see if everyone is dead
    if surv == -1: #no survivors from previous generation
        results['dead'] += 1
        if season['Run'] == runs_: #end model at end of last run
            write()
        elif season['Run'] != runs_:
            reset3() #check runs and continue if needed
    elif surv == 0: #there are some survivors
        if _id == pop_size: #start of function
            survivors = copy.deepcopy(hoarder_values) #copy population survival data
            _id = _id - 1 #if some survived, move to first forager
            next_gen()
        elif _id > -1 and _id < pop_size: #0 is included as an id; if forager is in the population
            if survivors['state'][_id] > 997: #if forager is dead
                del survivors['id'][_id]
                del survivors['stored food'][_id]
                _id = _id -1 # move to next animal
                next_gen()
            elif survivors['state'][_id] < 998: #if forager is alive
                _id = _id -1 #move to next forager in list
                next_gen()   
        elif _id == -1: #if all survivors have been checked for death
            checkIfDuplicates_trait() #check to see if one trait died out
            if fixation == -1: 
                offspring() #determine phenotypes of offspring
                reset2() #add a generation, reset other values
                fun(hoarders_num, days_perish, mast_crop, for_eff) #start a new foraging season
            if fixation > -1: #if a trait HAS fixated
                if fixation == 1: #hoarding fixated
                    results['hoarder'] += 1
                elif fixation == 0: #nonhoarding fixated
                    results['nonhoarder'] += 1
                if season['Run'] == runs_: #end model at end of last run
                    write()
                elif season['Run'] != runs_:
                    reset3() #check runs, stop model if needed; continues foraging if needed


def offspring():
    '''
    Reproduction by suvivors of a season to create a new generation of foragers.
    
    A new population of animals is created by randomly choosing parents from
    the list of survivors. Each offspring's hoarding phenotype is determined 
    by the phenotype of a single parent. e.g., If the parent is a hoarder, 
    the offspring is a hoarder.
    
    '''
    global phenotype 
    global phenotype2
    global survivors
    if len(phenotype2) < pop_size: #if all animals have not yet been checked
        parents = random.choices(survivors['id'],k=1) #choose 1 parent, NOT WEIGHTED
        young = survivors['storage effort'][parents[0]] #offspring has same storage effort as parent
        phenotype2.append(young) #add offspring to new generation
        phenotype2 = phenotype2
        offspring() #repeat until entire new population is created
    elif len(phenotype2) == pop_size: #if new population is correct size
        phenotype = copy.deepcopy(phenotype2)


def reset2(): #all generations after the first, within a run
    ''' 
    Reset variables to initial values after the first generation,
    but within a run.
    '''
    global season
    global state2
    global hoarder_id
    global hoarder_stored
    global hoarder_values
    global public_food_harv
    global foragers
    global forager_id
    global phenotype
    global phenotype2
    global _id
    global fixation
    season['Day'] = 1
    season['Bout'] = 0    
    season['Generation'] += 1
    state2 = (pop_size)*[0]
    hoarder_id = [*range(0,pop_size)]
    hoarder_stored = (pop_size)*[0]
    pheno = copy.deepcopy(phenotype)
    pred_risk = pred_risk_pop + np.multiply(pred_risk_pop,pheno)
    pred_risk = pred_risk.tolist()
    pred_risk = pred_risk
    hoarder_values = {'state':state2, 'id':hoarder_id, 'stored food':hoarder_stored, 
    'predation risk': pred_risk, 'storage effort':pheno} 
    public_food_harv = 0
    foragers = 0 
    forager_id = -1
    _id = pop_size
    phenotype = []       
    phenotype2 = []
    fixation = -1


def write():
    ''' 
    This function checks to see if the appropriate number of runs have been completed
    for this combination of parameters within the model.
    
    Each time this function is called, data is exported to a cvs file.

    '''
    input_variable = [season['Run'],season['Generation'], results['hoarder'], results['nonhoarder'],
        results['dead'],hoarders_num, pred_risk_pop, for_eff,
        days_perish, mast_crop, SH_pilfer_ability]
    with open('Evolution_model1.csv', 'a', newline = '') as csvfile:
        my_writer = csv.writer(csvfile, delimiter = ',')
        my_writer.writerow(input_variable)
    gc.collect() #garbage collecting- might free up some memory?
    if season['Run'] == runs_:
        reset() #reset back to first generation of first run
        season['Run'] = 1
    else:
        pass


def reset3(): #after end of each run
    ''' 
    This function moves the model to the next run.
    
    '''
    global season
    global surv
    global hoarders_num
    global days_perish
    global mast_crop
    global for_eff
    surv = 5
    write()
    season['Run'] += 1 #directly add a run to the season dict
    reset4() #reset values back to first generation
    fun(hoarders_num, days_perish, mast_crop, for_eff) #start foraging and running the season


def run_fun():
    ''' Run the simulation. '''
    global days_perish
    global mast_crop
    global for_eff
    for days_perish in [0]: #always 0, in the current version of the model
        for mast_crop in [1000,1600,2000,2200]:
            for for_eff in [0.0005,0.001,0.0025,0.005,0.0075,0.01]:
                fun(hoarders_num, days_perish, mast_crop, for_eff)

# Run the model!
run_fun()