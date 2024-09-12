import operator
import random

class Species:
    def __init__(self, player):
        self.players = [player]
        self.average_fitness = 0
        self.threshold = 1.2
        self.benchmark_fitness = player.fitness
        self.benchmark_brain = player.brain.clone()
        self.champion = player.clone()
        self.staleness = 0

    def similarity(self, brain):
        similarity = self.weight_difference(self.benchmark_brain, brain)
        return self.threshold > similarity
    
    @staticmethod
    def weight_difference(brain1, brain2):
        total = 0
        for i in range(len(brain1.connections)):
            total += abs(brain1.connections[i].weight - brain2.connections[i].weight)
        return total
    
    def add_to_species(self, player):
        self.players.append(player)

    def sort_players_by_fitness(self):
        self.players.sort(key = operator.attrgetter("fitness"), reverse=True)
        if self.players[0].fitness > self.benchmark_fitness:
            self.benchmark_fitness = self.players[0].fitness
            self.champion = self.players[0].clone()
            self.staleness = 0
        else:
            self.staleness += 1

    def calculate_average_fitness(self):
        total = 0
        for player in self.players:
            total += player.fitness
        if len(self.players) > 0:
            self.average_fitness = int(total / len(self.players))

    def offspring(self):
        child = self.players[random.randint(1, len(self.players)) - 1].clone()
        child.brain.mutate()
        return child