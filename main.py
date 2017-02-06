from neural_network.preprocessor import Preprocessor
from wikipedia_parser.wikipedia_parser import WikipediaParser
import numpy as np
import tensorflow as tf

'''
input > weight > hidden layer 1 (activation function)
> weights > hidden layer 2 (activation function)
> weights > output layer

compare output to intended output > cost function (cross entropy)
optimization function (optimizer) > minimize cost (AdamOptimizer, gradient descent, etc...)

backpropogation

feed forward + backpropogation = 1 epoch (one cycle of the network) 
'''

preprocessor = Preprocessor()
train_x,train_y,test_x,test_y = preprocessor.create_feature_sets_and_labels()

print(train_x)

batch_size = 100

n_nodes_hl1 = 500
n_nodes_hl2 = 500
n_nodes_hl3 = 500

n_classes = 5 # Example: [0,0,1,0,0] == 2

x = tf.placeholder('float', [None,len(train_x)])
y = tf.placeholder('float')

def neural_network_model(data):

	# (input_data * weights) + biases

	# biases make sure that inputs of zero still
	# produce a non-zero output

	hidden_layer_1 = {'weights':tf.Variable(tf.random_normal([len(train_x), n_nodes_hl1])),
					  'biases':tf.Variable(tf.random_normal([n_nodes_hl1]))}

	hidden_layer_2 = {'weights':tf.Variable(tf.random_normal([n_nodes_hl1, n_nodes_hl2])),
					  'biases':tf.Variable(tf.random_normal([n_nodes_hl2]))}

	hidden_layer_3 = {'weights':tf.Variable(tf.random_normal([n_nodes_hl2, n_nodes_hl3])),
					  'biases':tf.Variable(tf.random_normal([n_nodes_hl3]))}

	output_layer = {'weights':tf.Variable(tf.random_normal([n_nodes_hl3, n_classes])),
					'biases':tf.Variable(tf.random_normal([n_classes]))}

	# (input_data * weights) + biases

	layer_1 = tf.add(tf.matmul(data,hidden_layer_1['weights']),hidden_layer_1['biases'])
	layer_1 = tf.nn.relu(layer_1)

	layer_2 = tf.add(tf.matmul(layer_1,hidden_layer_2['weights']),hidden_layer_2['biases'])
	layer_2 = tf.nn.relu(layer_2)

	layer_3 = tf.add(tf.matmul(layer_2,hidden_layer_3['weights']),hidden_layer_3['biases'])
	layer_3 = tf.nn.relu(layer_3)

	output = tf.matmul(layer_3, output_layer['weights']) + output_layer['biases']

	return output

def train_neural_network(x):

	prediction = neural_network_model(x)

	print(prediction)
	print(y)
	return
	cost = tf.reduce_mean( tf.nn.softmax_cross_entropy_with_logits(prediction, y) )

	optimizer = tf.train.AdamOptimizer().minimize(cost)

	num_of_epochs = 15

	with tf.Session() as sess:
		sess.run(tf.global_variables_initializer())

		for epoch in range(num_of_epochs):
			epoch_loss = 0

			i = 0
			while  i < len(train_x):
				start = i
				end = i + batch_size

				batch_x = np.array(train_x[start:end])
				batch_y = np.array(train_x[start:end])

				_,c = sess.run([optimizer,cost], feed_dict={x:batch_x, y:batch_y})
				epoch_loss += c
				i += batch_size
			print('Epoch', epoch, 'completed out of', num_of_epochs, 'loss', epoch_loss)
		correct = tf.equal(tf.argmax(prediction,1), tf.argmax(y,1))
		accuracy = tf.reduce_mean(tf.cast(correct,'float'))

		print('Accuracy',accuracy.eval({x:test_x, y:test_y}))

train_neural_network(x)