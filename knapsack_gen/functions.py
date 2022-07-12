#!/bin/python3
import random
def init_pop(pop_size, knap_size):
	pop_array = []
	for i in range(pop_size):
		lis1 = []
		for j in range(knap_size):
			lis1.append(random.randint(0, 1))
		pop_array.append(lis1)
	return pop_array

def fitness_function(knapsack, chromosome, capacity):
	profit = 0
	volume = 0
	for i in range(len(chromosome)):
		xi = chromosome[i]
		pi = knapsack[i][0]
		vi = knapsack[i][1]
		profit += xi * pi
		volume += xi * vi
	while volume > capacity:
		chromo_size = len(chromosome)
		location = random.randint(0, chromo_size - 1)
		while chromosome[location] != 1:
			location = random.randint(0, chromo_size - 1)
		chromosome[location] = 0
		profit -= knapsack[location][0]
		volume -= knapsack[location][1]
	return profit, volume

def mutate(chromosome, mutation_rate):
	for i in range(len(chromosome)):
		chance = random.random()
		if chance <= mutation_rate:
			chromosome[i] ^= 1

def crossover(chromosome1, chromosome2, crossover_rate, mutation_rate):
	if len(chromosome1) != len(chromosome2):
		print("Crossover Error: chromosomes must of same size")
		return
	cross_point = random.randint(0, len(chromosome1))
	offspring1 = []
	offspring2 = []
	for i in range(0, len(chromosome1)):
		offspring1.append(chromosome1[i])
		offspring2.append(chromosome2[i])
	chance = random.random()
	if chance <= crossover_rate: 
		for j in range(cross_point + 1, len(chromosome1)):
			offspring1[j] = chromosome2[j]
			offspring2[j] = chromosome1[j]
	mutate(offspring1, mutation_rate)
	mutate(offspring2, mutation_rate)
	chromosome1 = offspring1
	chromosome2 = offspring2

def pop_fitness(knapsack, pop_array, capacity):
	chr_fitness = []
	chr_volume = []
	for i in range(len(pop_array)):
		chromosome = pop_array[i]
		profit, volume = fitness_function(knapsack, chromosome, capacity)
		chr_fitness.append([profit, i])
		chr_volume.append([volume, i])
	return chr_fitness, chr_volume

def roulette_select(pop_array, chr_fitness):
	fitness_sum = 0
	for fitness in chr_fitness:
		fitness_sum += fitness[0]
	stopping_sum = random.randint(0, fitness_sum)
	acc_sum = 0
	stopping_point = 0
	for i in range(len(chr_fitness)):
		acc_sum += chr_fitness[i][0]
		stopping_point = i
		if acc_sum >= stopping_sum:
			break
	return pop_array[stopping_point]
				
def group_select(pop_array, chr_fitness):
	copy_chr_fitness = []
	for elem in chr_fitness:
		copy_chr_fitness = elem
	copy_chr_fitness.sort()
	size = len(copy_chr_fitness)
	ind1 = 0
	ind2 = size//4
	ind3 = 2 * ind2
	ind4 = 3 * ind2
	ind5 = size - 1
	selected_range = []
	chance = random.randint(1, 100)
	if chance <= 50:
		selected_range = [ind1, ind2]
	elif chance > 50 and chance <= 80:
		selected_range = [ind2, ind3]
	elif chance > 80 and chance <= 95:
		selected_range = [ind3, ind4]
	else:
		selected_range = [ind4, ind5]
	selected = random.randint(selected_range[0], selected_range[1])
	return pop_array[selected]
	
def get_ratio(chr_fitness):
	frequencies = {}
	for i in chr_fitness:
		if i[0] not in frequencies:
			frequencies[i[0]] = 1
		else:
			frequencies[i[0]] += 1
	total = 0
	maximum = -1
	for key in frequencies.keys():
		total += frequencies[key]
		maximum = max(frequencies[key], maximum)
	return maximum / total

def terminate(ratio, generations, termination_ratio, max_generations):
	if ratio >= termination_ratio or generations >= max_generations:
		return True
	else:
		return False
