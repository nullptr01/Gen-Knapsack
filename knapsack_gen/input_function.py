#!/bin/python3
def isint(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def get_knapsack(profit_filename, volume_filename, capacity_filename):
	profit_file = open(profit_filename, 'r')
	volume_file = open(volume_filename, 'r')
	capacity_file = open(capacity_filename, 'r')
	profits = [int(i) for i in (profit_file.read()).split()]
	volumes = [int(i) for i in (volume_file.read()).split()]
	capacities = [int(i) for i in (capacity_file.read()).split()]
	knap = []
	for i in range(len(profits)):
		knap.append([profits[i], volumes[i]])
	return knap, capacities
