"""
George.py implements a genetic algorithm aimed to reproduce text
The name stems from the infinite monkey theorem where a monkey hitting keys at random will type any given text
such as the complete works of Shakespeare
The Evolution() class takes in the target string as an argument and initializes a random population
evolution.evolution_rounds generates rounds of evolution
This can be continued in as many rounds as desired
If the target is acquired, evolution will stop.
"""
import numpy as np
from tqdm import tqdm

def generate_random_dna(N, target):
    """
    Function to randomly generate DNA elements
    DNA elements will be randomly generated from the ASCII characters that are present in the target string

    :param N: number of DNA elements to generate
    :type N: int
    :param target: target string to match
    :type target: str
    :return: DNA string randomly generated
    :rtype: str
    """
    dna_elements = []
    for i in range(0, len(target)):
        # ord takes the ASCII number of each character in the target string
        elem = ord(target[i])
        dna_elements.append(elem)
    # randomly generated ASCII characters
    dna_nums = list(np.random.choice(dna_elements, N))
    dna = ""
    for elem in dna_nums:
        # chr converts the ASCII character back into a str
        dna = dna + chr(int(elem))
    return dna


class Evolution(object):
    """
    Class for Evoloving a population to reach the target string

    Attributes:
        target  target string you wish to evolve to
        populationsize  size of population of each generation, default is 100
        population      population of each generation, will change with evolution
        fitness         fitness scores of the population
        mating_pool     mating pool to generate new members of population
        generation      number to represent the generation you are on
        target_acquired boolean field, if true then the target was required
        max_fitness     current maximum fitness score of population
        target_population   the member of the population that is equal to the target string once evolution is completed
        closest_target  the current member of hte population that is closest to the target
    """
    def __init__(self, target, populationsize=100):
        """

        :param target: target string
        :type target: str
        :param populationsize: size of initial population and subsequent new generations population, default is 100
        :type populationsize: int
        """
        self.target = target
        self.populationsize = populationsize
        self.population = []
        self.fitness = []
        self.mating_pool = []
        self.generation = 1
        self.target_acquired = False
        self.max_fitness = None
        self.target_population = None
        self.closest_target = None
        # initialize population
        self.generate_initial_population()
        # initialize fitness scores
        self.generate_fitness()
        # initialize matingpool
        self.create_mating_pool()
        # check initial progress
        self.check_progress()

    def generate_initial_population(self):
        """
        Function to generate a population sized denoted as size
        population is of N generated random DNA elements
        N is the length of the target
        """
        self.population = []
        N = len(self.target)
        for x in range(0, self.populationsize):
            dna = generate_random_dna(N, self.target)
            self.population.append(dna)

    def generate_fitness(self):
        """
        Function to generate the fitness score of each population member
        fitness score is determined by the number of correctly placed characters in the string
        """
        self.fitness = []
        for member in self.population:
            score = 0
            for i in range(0, len(self.target)):
                if member[i] == self.target[i]:
                    score = score + 1
            self.fitness.append(score / len(self.target))

    def create_mating_pool(self):
        """
        Function to generate the mating pool
        the matingpool will be generated from members of the population
        a member will be added to the matingpool as determined by their fitness score %
        for example: if a member has .5 fitness score, it will be added 50 times to the mating pool
        """
        self.mating_pool = []
        for i, member in enumerate(self.population):
            score = self.fitness[i]
            n = int(np.rint(score * 100))
            for j in range(0, n):
                self.mating_pool.append(member)

    def reproduction(self):
        """
            Function to pick two parents from the mating pool and combine them for the new generation
            2 parents are picked randomly
            The two parents will make 2 babies.
            The first will be the "best" parts from parentA and the rest from parentB
            the second will be the "best" parts from parentB and the rest from parentA
            """

        self.population = []
        for x in range(0, int(self.populationsize/2)):
            parentA = np.random.choice(self.mating_pool)
            other_parents = [member for member in self.mating_pool if member != parentA]
            parentB = np.random.choice(other_parents)
            babyA = ""
            babyB = ""
            for i in range(0, len(self.target)):
                if parentA[i] == self.target[i]:
                    babyA = babyA + parentA[i]
                else:
                    babyA = babyA + parentB[i]
                if parentB[i] == self.target[i]:
                    babyB = babyB + parentB[i]
                else:
                    babyB = babyB + parentA[i]
            self.population.append(babyA)
            self.population.append(babyB)

    def mutation(self, mutation_rate=0.01):
        """
        Function to mutate childs DNA
        This will allow more diversity in the new generation
        mutation rate is set at 0.01, but can be changed when calling evolution.evolution_rounds
        if mutating then the dna character will be randomly exchanged for one that is within the ASCII codes of the
        target str

        :param mutation_rate: rate to mutate
        :type mutation_rate: float
        """
        new_population = []
        for member in self.population:
            dna_out = ""
            for i in range(0, len(member)):
                mutation = np.random.choice(['mutate', 'no_mutate'], p=[mutation_rate, 1 - mutation_rate])
                if mutation == 'mutate':
                    dna_out = dna_out + generate_random_dna(1, self.target)
                else:
                    dna_out = dna_out + member[i]
            new_population.append(dna_out)
        self.population = new_population

    def check_progress(self):
        """
        Function to check progress of evolution
        can check max_fitness to check the highest fitness score
        closet_target will be the member of the population that has the highest score

        """
        self.max_fitness = max(self.fitness)
        index = self.fitness.index(self.max_fitness)
        self.closest_target = self.population[index]
        if self.max_fitness == 1.0:
            self.target_acquired = True
            self.target_population = self.closest_target

    def new_generation(self, mutation_rate=0.01):
        """
        Function to create a new generation

        """
        self.reproduction()
        self.mutation(mutation_rate)
        self.generate_fitness()
        self.check_progress()
        self.create_mating_pool()
        self.generation = self.generation + 1


    def evolution_rounds(self, rounds, mutation_rate=0.01):
        """
        Function to generate rounds of evolution
        main driver of the genetic algorithm class
        evolution_rounds will stop when the target is acquired

        :param rounds: rounds of evolution
        :type rounds: int
        :param mutation_rate: rate for mutation
        :type mutation_rate: float

        """
        pbar = tqdm(total=rounds, desc="Generations")
        for i in range(0, rounds):
            self.new_generation(mutation_rate)
            pbar.update(1)
            if self.target_acquired:
                pbar.close()
                print("Target Acquired: ", self.target_population)
                print("Generation acquired:", self.generation)
                break
        pbar.close()
        if not self.target_acquired:
            print("Need more evolution rounds!")
            print("Closest to target: ", self.closest_target)
            print("Max Population Fitness: {:.2%}".format(self.max_fitness))
            print("Generation: ", self.generation)






