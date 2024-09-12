import node
import connection
import random

class Brain:
    def __init__(self, inputs, clone=False):
        self.connections = []
        self.nodes = []
        self.inputs = inputs
        self.network = []
        self.layers = 2

        if not clone:
            # Create input nodes
            for i in range(self.inputs):
                self.nodes.append(node.Node(i))
                self.nodes[i].layer = 0
            # Append bias node
            self.nodes.append(node.Node(self.inputs))
            self.nodes[-1].layer = 0
            # Append output node
            self.nodes.append(node.Node(self.inputs + 1))
            self.nodes[-1].layer = 1

            for i in range(len(self.nodes) - 1):
                self.connections.append(connection.Connection(self.nodes[i], 
                                                            self.nodes[-1], 
                                                            random.uniform(-1, 1)))
    
    def connect_nodes(self):
        for node in self.nodes:
            node.connections = [] 
        for connection in self.connections:
            connection.from_node.connections.append(connection)

    def generate_network(self):
        self.connect_nodes()
        self.network = []
        for i in range(self.layers):
            for node in self.nodes:
                if node.layer == i:
                    self.network.append(node)
    
    def feed_forward(self, vision):
        for i in range(self.inputs):
            self.nodes[i].output_value = vision[i]
        self.nodes[self.inputs].output_value = 1

        for node in self.network:
            node.activate()

        for node in self.nodes:
            node.input_value = 0
        
        return self.nodes[-1].output_value
    
    def clone(self):
        clone = Brain(self.inputs, True)
        for node in self.nodes:
            clone.nodes.append(node.clone())
        for connection in self.connections:
            clone.connections.append(connection.clone(
                clone.getNode(connection.from_node.id), 
                clone.getNode(connection.to_node.id)))
        clone.layers = self.layers
        clone.connect_nodes()
        return clone
    
    def getNode(self, id):
        for node in self.nodes:
            if node.id == id:
                return node
            
    def mutate(self):
        if random.uniform(0, 1) < 0.8:
            for connection in self.connections:
                connection.mutate_weight()