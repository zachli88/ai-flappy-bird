import config
import player
import math
import species
import operator

class Population:
    def __init__(self, size):
        self.players = []
        self.generation = 1
        self.species = []
        self.size = size
        for i in range(self.size):
            self.players.append(player.Player())

    def update_live_players(self):
        for player in self.players:
            if player.alive:
                player.look()
                player.think()
                player.draw(config.window)
                player.update(config.ground)

    def natural_selection(self):
        print("SPECIATE")
        self.speciate()

        print("CALCULATE FITNESS")
        self.calculate_fitness()

        print("REMOVE EXTINCT")
        self.remove_extinct()

        print("REMOVE_STALE")

        print("SORT BY FITNESS")
        self.sort_species_by_fitness()

        print("CHILDREN FOR NEXT GENERATION")
        self.next_gen()

    def speciate(self):
        for s in self.species:
            s.players = []

        for player in self.players:
            add_to_species = False
            for s in self.species:
                if s.similarity(player.brain):
                    s.add_to_species(player)
                    add_to_species = True
                    break
            if not add_to_species:
                self.species.append(species.Species(player))
    
    def calculate_fitness(self):
        for s in self.species:
            s.calculate_average_fitness()

    def remove_extinct(self):
        species_bin = []
        for species in self.species:
            if len(species.players) == 0:
                species_bin.append(species)
        for species in species_bin:
            self.species.remove(species)

    def remove_stale(self):
        player_bin = []
        species_bin = []
        for species in self.species:
            if species.staleness >= 8:
                if len(self.species) > len(species_bin) + 1:
                    species_bin.append(species)
                    for player in species.players:
                        player_bin.append(player)
                else:
                    species.staleness = 0
        for player in player_bin:
            self.players.remove(player)
        for species in species_bin:
            self.species.remove(species)
    
    def sort_species_by_fitness(self):
        for s in self.species:
            s.sort_players_by_fitness()
        
        self.species.sort(key = operator.attrgetter("benchmark_fitness"), reverse=True)

    def next_gen(self):
        children = []
        for s in self.species:
            children.append(s.champion.clone())
        children_per_species = math.floor((self.size - len(self.species) / len(self.species)))
        for s in self.species:
            for i in range(children_per_species):
                children.append(s.offspring())
    
        while len(children) < self.size:
            children.append(self.species[0].offspring())

        self.players = children

        self.generation += 1
            
    
    def extinct(self):
        for player in self.players:
            if player.alive:
                return False
        return True
