import math
import numpy as np
np.random.seed(2020)
# Kindly stolen from https://towardsdatascience.com/lets-code-a-neural-network-in-plain-numpy-ae7e74410795

def sigmoid(Z):
    return 1/(1+np.exp(-Z))

def create_layer(isize, osize):
	weights = np.random.randn(osize, isize)*0.1
	biases = np.random.randn(osize, 1)*0.1
	return (weights, biases)

def single_layer_forward_propagation(a_prev, w_curr, b_curr):
	z_curr = np.dot(w_curr, a_prev) + b_curr
	return sigmoid(z_curr)

def full_forward_propagation(X, layers):
	#memory = {}
	A_curr = X
	
	for layer in layers:
		A_prev = A_curr
		
		W_curr, b_curr = layer
		A_curr = single_layer_forward_propagation(A_prev, W_curr, b_curr)
	return A_curr

class FFNeuralNetwork():
	def __init__(self, input_size=4, output_size=2, hidden_layers=(3,)):
		temp_list = [input_size, *hidden_layers, output_size]
		self.i_s = input_size
		self.o_s = output_size
		self.layers = [create_layer(i, o) for i, o in zip(temp_list, temp_list[1:])]

	def get_result(self, inp):
		i = np.array(inp).reshape((self.i_s, 1))
		result = full_forward_propagation(i, self.layers).reshape((self.o_s,))
		return result

nn = FFNeuralNetwork()
print(nn.get_result([1, 2, 3, 4]))
