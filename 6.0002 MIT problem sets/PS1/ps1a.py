###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name: SK
# Collaborators: Nein
# Time: 3:00

from cgi import valid_boundary
from lib2to3.fixer_util import parenthesize

from ps1_partition import get_partitions
import time


# ================================
# Part A: Transporting Space Cows
# ================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    # Without the use of try-finally
    with open(filename, 'r') as cowFile:
        cowData = cowFile.read()
    cowFile.closed
    # Regardless of how data appears in notepad, there exists new line characters that are appropriately divided
    # Can also use str.split
    cows = str.splitlines(cowData, False)
    cowDict = {}
    # Loop through, split data and update dictionary above, Cast Second value of split to int
    for cowDetail in cows:
        splitCowDetail = str.split(cowDetail, ',')
        cowDict.update({splitCowDetail[0]: int(splitCowDetail[1])})
    return cowDict


def sortedCowsList(cows):
    """
    Sorts a dictionary of cows passed by user into list of tuples of cow and its weight
    Do not use dictionary composition because dictionaries cannot be sorted

    Parameters:
    cows - a dictionary of cows

    Returns:
    a list of tuples representing key and value
    """
    sortedCows = [(key, value)
                  for key, value in
                  sorted(cows.iteritems(),
                         key=lambda (k, v): (v, k), reverse=True)
                  ]
    return sortedCows

# Problem 2
def greedy_cow_transport(cows, limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    start = time.time()
    finalTransportList = []
    sortedCows = sortedCowsList(cows)

    while (len(sortedCows) != 0):
        remainingWeight = limit
        transportlist = []
        for cow in sortedCows:
            if cow[1] <= remainingWeight:
                remainingWeight -= cow[1]
                transportlist.append(cow)
        for cow in transportlist:
            sortedCows.remove(cow)

        finalTransportList.append([cow[0] for cow in transportlist])
    end = time.time()
    print("Greedy Algorithm time taken:", end - start)

    return finalTransportList

# Problem 3
def brute_force_cow_transport(cows, limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    start = time.time()
    cowsNames = cows.keys()
    sortedCows = sortedCowsList(cows)
    powerSet = get_partitions(cowsNames)
    smallest = limit ** limit
    smallestSets = []
    for partitions in powerSet:
        if len(partitions) <= smallest:
            exceedsWeight = False
            for permutation in partitions:
                weight = 0
                for cow in permutation:
                    weight += cows[cow]
                    if weight > limit:
                        exceedsWeight = True
                        break
                if exceedsWeight == True:
                    break
            if exceedsWeight == False:
                if len(partitions) == smallest:
                    smallestSets.append(partitions)
                else:
                    smallestSets = []
                    smallestSets.append(partitions)
                    smallest = len(partitions)
    end = time.time()
    print("Time taken for Brute Force: ", end - start)

    return smallestSets


# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    cowSet = load_cows('ps1_cow_data.txt')
    print greedy_cow_transport(cowSet)
    for sets in brute_force_cow_transport(cowSet):
        print sets
    return


compare_cow_transport_algorithms()
