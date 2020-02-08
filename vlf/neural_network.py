import math
import numpy as np
# Kindly stolen from https://towardsdatascience.com/lets-code-a-neural-network-in-plain-numpy-ae7e74410795

def sigmoid(Z):
    return 1/(1+np.exp(-Z))

def tanh(z):
    return (np.exp(z) - np.exp(-z)) / (np.exp(z) + np.exp(-z))

def create_layer(isize, osize):
        weights = np.random.randn(osize, isize)
        biases = np.random.randn(osize, 1)
        return (weights, biases)

def single_layer_forward_propagation(a_prev, w_curr, b_curr):
        #print("====")
        #print("A_PREV")
        #print(a_prev)
        #print("W_CURR")
        #print(w_curr)
        #print("B_CURR")
        #print(b_curr)
        #print("====")
        z_curr = np.dot(w_curr, a_prev) + b_curr
        #return sigmoid(z_curr)
        return tanh(z_curr)

def full_forward_propagation(inp, layers):
    a_curr = inp
    
    for layer in layers:
        a_prev = a_curr
        w_curr, b_curr = layer
        a_curr = single_layer_forward_propagation(a_prev, w_curr, b_curr)
    return a_curr

class FFNeuralNetwork():
    def __init__(self, input_size=4, output_size=2, hidden_layers=(3,)):
        temp_list = [input_size, *hidden_layers, output_size]
        self.i_s = input_size
        self.o_s = output_size
        self.layers = [create_layer(i, o) for i, o in zip(temp_list, temp_list[1:])]
        self.layers_scheme = [(i, o) for i, o in zip(temp_list, temp_list[1:])]

    def get_result(self, inp):
        i = np.array(inp).reshape((self.i_s, 1))
        result = full_forward_propagation(i, self.layers).reshape((self.o_s,))
        return result

    def get_flattened_array(self):
        mega_flat = np.array(None)
        first_generator = ((l[0].flatten(), l[1].flatten()) for l in self.layers)
        # Mind -> broken
        mega_generator = (item for sublist in first_generator for item in sublist)
        listo = list(mega_generator)
        result = np.concatenate(listo)
        return result

    def assemble_from_flattened(self, flattened):
        cur_array = flattened
        layers = []
        for sch in self.layers_scheme:
            weights, cur_array = np.split(cur_array, (sch[0]*sch[1],))
            biases, cur_array = np.split(cur_array, (sch[1],))
            layers.append((weights.reshape((sch[1], sch[0])), biases.reshape((sch[1]),1)))
        self.layers = layers


# TODO make it a test
"""
nn1 = FFNeuralNetwork()
nn2 = FFNeuralNetwork()

flat = nn1.get_flattened_array()
#nn2.assemble_from_flattened(flat)
print(nn1.layers)
print("====")
print(nn2.layers)
nn2.assemble_from_flattened(flat)
print("====")
print(nn2.layers)

for a, b in zip(nn1.layers, nn2.layers):
    print(a[0].all() == b[0].all())
    print(a[1].all() == b[1].all())
"""
