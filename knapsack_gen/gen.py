#!/bin/python3
from functions import *
from input_function import get_knapsack

MUTATION_RATE = 0.001
CROSSOVER_RATE = 0.85
MAX_GENERATIONS = 300
TERMINATION_RATIO = 0.9
POPULATION_RANGE = [100, 200, 250, 300, 400, 500, 750]


def solve(pop_size, knapsack, capacity, selection_function, termination_ratio, max_generations):
	pop_array = init_pop(pop_size, len(knapsack))
	chr_fitness, chr_volume = pop_fitness(knapsack, pop_array, capacity)
	generations = 0
	while terminate(get_ratio(chr_fitness), generations, termination_ratio, max_generations) == False: 
		chromosome1 = selection_function(pop_array, chr_fitness)
		chromosome2 = selection_function(pop_array, chr_fitness)
		crossover(chromosome1, chromosome2, CROSSOVER_RATE, MUTATION_RATE)
		generations += 1
		chr_fitness, chr_volume = pop_fitness(knapsack, pop_array, capacity)
	return pop_array, chr_fitness, chr_volume, generations
	 
def write_output(knapsack, capacity, selection_function, out_file):
	for pop_size in POPULATION_RANGE:
		pop_array, chr_fitness, chr_volume, generations = solve(pop_size, knapsack, capacity, selection_function, TERMINATION_RATIO, MAX_GENERATIONS)
		chr_fitness.sort()
		max_profit = chr_fitness[len(chr_fitness) - 1][0]
		max_chr = pop_array[chr_fitness[len(chr_fitness) - 1][1]]
		elems = []
		for i in range(len(max_chr)):
			if max_chr[i] == 1:
				elems.append(i + 1)
		out_file.write("Population: " + str(pop_size) + "  " + "Generations: " + str(generations) + "  "  + "Max Profit: " + str(max_profit) + "  " + "Items Chosen :" + str(elems) + "\n\n") 

def main():
	for i in range(3):
		output_filename = "output" + str(i + 1) + ".txt"
		out_file = open(output_filename, "w")
		profit_filename = "p0" + str(i + 1) + "_p.txt"
		volume_filename = "p0" + str(i + 1) + "_w.txt"
		capacity_filename = "p0" + str(i + 1) + "_c.txt"
		out_file.write("Problem-" + str(i + 1) + "\n")
		knapsack, capacities = get_knapsack(profit_filename, volume_filename, capacity_filename)
		out_file.write("Roulette Select, Capacity = "+ str(capacities[0]) + "\n\n")
		write_output(knapsack, capacities[0], roulette_select, out_file)
		out_file.write("Roulette Select, Capacity = "+ str(capacities[1]) + "\n\n")
		write_output(knapsack, capacities[1], roulette_select, out_file)
		out_file.write("Group Select, Capacity = "+ str(capacities[0]) + "\n\n")
		write_output(knapsack, capacities[0], group_select, out_file)
		out_file.write("Group Select, Capacity = "+ str(capacities[1]) + "\n\n")
		write_output(knapsack, capacities[1], group_select, out_file)
main()
