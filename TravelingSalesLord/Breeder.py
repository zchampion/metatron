"""
Programmer: Zachary Champion
Project:    Traveling Sales Lord
Project Description:

File:       Breeder.py
File Description:
            Breeder class - details how to breed, select parents, etc.
"""

from random import seed, choice, shuffle, randint

from ProgramMetatron.Minion import Minion


class Breeder:
    def __init__(self, gene_pool, population_size, tournament_size):
        # Breeder's policies
        self.next_avail_id = 1
        self.population_size = population_size
        self.tournament_size = tournament_size

        # Breeder's inventory
        self.gene_pool = gene_pool  # Names of the cities
        self.population = [self.spawn_route() for _ in range(self.population_size)]
        self.next_population = []

        # Breeder's records - overall
        self.best_route = None  # Best program so far
        self.elite_force = []  # Here is going to be the list of all the programs that run without errors.

    def assign_id(self):
        """
        Makes a string of an appropriate length of the minion id number.
        :return:
        """
        id_string = "{:0>8}".format(self.next_avail_id)
        self.next_avail_id += 1
        return id_string

    def spawn_route(self):
        new_minion = Minion(self.assign_id(), self.spawn_program())
        return new_minion

    def spawn_program(self):
        program = [line for line in self.gene_pool]
        shuffle(program)
        return program

    def breed(self, parents):
        """
        Breeds two parent programs together to get a single child.
        WISH LIST: Get two children and return the most fit child.
        :param parents: (tuple, contains 2 parents)
        :return: a single child minion object
        """
        seed()  # Seed the random functions anew every time.

        # Unpack the parents tuple.
        parent1, parent2 = parents

        gene_bgn = randint(1, min(len(parent1), len(parent2)) - 1)  # Generates a random index in the shorter of
        gene_end = randint(1, min(len(parent1), len(parent2)) - 1)  # parent1 or parent2.

        # I want the gene to be switched from parent1 to parent2 for now.
        # Later, it may just switch the genes between the two parents and return both as children.
        # Also, see function comment above for possible wish list feature.
        child_program = parent1.program[:gene_bgn] + parent2.program[gene_bgn:gene_end] + parent1.program[gene_end:]

        return Minion(self.assign_id(), child_program)

    @staticmethod
    def mutate(minion):
        """
        Mutates the minion (python code) by shuffling the minion's program.
        :param minion:
        :return:
        """
        shuffle(minion.program)

    def mating_ritual(self):
        """
        Uses tournament selection with a variable sized tournament to select breeding parent individuals.
        Returns the two most fit parents in the randomly selected arena to breed.
        :param population:
        :return: a tuple with 2 parents
        """
        # Choose random tournament participants up to the size of the tournament.
        arena = [choice(self.population) for _ in range(self.tournament_size)]

        # Look through the arena for the most and second most fit individuals.
        champion, runnerup = arena[0], arena[1]
        for gladiator in arena:
            if gladiator.fitness > runnerup.fitness:
                runnerup = gladiator

            elif gladiator.fitness > champion.fitness:
                runnerup = champion
                champion = gladiator

        return champion, runnerup