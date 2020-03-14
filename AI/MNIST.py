import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
from tensorflow.examples.tutorials.mnist import input_data
tf.reset_default_graph()
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True, validation_size=50000)
print("Training dataset :", len(mnist.train.labels),
      "\nTesting dataset :", len(mnist.test.labels),
      "\nValidation dataset :", len(mnist.validation.labels))

#Xavier initialization
def init(n_inputs, n_outputs, uniform=True):
    if uniform:
        init_range = tf.sqrt(6.0 / (n_inputs + n_outputs))
        return tf.random_uniform_initializer(-init_range, init_range)
    else:
        stddev = tf.sqrt(3.0 / (n_inputs + n_outputs))
        return tf.truncated_normal_initializer(stddev=stddev)

n_input = 784
n_hidden1 = 1024
n_hidden2 = 512
n_output = 10
learning_rate = 0.001
batch_size = 100
training_epochs = 60

X = tf.placeholder(tf.float32, [None, n_input])
Y = tf.placeholder(tf.float32, [None, n_output])


W1 = tf.get_variable("W1", shape=[n_input, n_hidden1], initializer=init(n_input, n_hidden1))
W2 = tf.get_variable("W2", shape=[n_hidden1, n_hidden2], initializer=init(n_hidden1, n_hidden2))
W3 = tf.get_variable("W3", shape=[n_hidden2, n_hidden2], initializer=init(n_hidden2, n_hidden2))
W4 = tf.get_variable("W4", shape=[n_hidden2, n_hidden2], initializer=init(n_hidden2, n_hidden2))
W5 = tf.get_variable("W5", shape=[n_hidden2,  n_output], initializer=init(n_hidden2,  n_output))

B1 = tf.Variable(tf.zeros([n_hidden1]))       
B2 = tf.Variable(tf.zeros([n_hidden2]))
B3 = tf.Variable(tf.zeros([n_hidden2]))
B4 = tf.Variable(tf.zeros([n_hidden2]))
B5 = tf.Variable(tf.zeros([n_output]))

# ReLU
L1 = tf.nn.relu(tf.add(tf.matmul(X, W1), B1))
L2 = tf.nn.relu(tf.add(tf.matmul(L1, W2), B2)) 
L3 = tf.nn.relu(tf.add(tf.matmul(L2, W3), B3)) 
L4 = tf.nn.relu(tf.add(tf.matmul(L3, W4), B4)) 
hypothesis = tf.add(tf.matmul(L4, W5), B5)

# softmax & Adam Optimizer
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=hypothesis, labels=Y)) 
optimizer = tf.train.AdamOptimizer(learning_rate).minimize(cost)

init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

def lr_schedule(epoch):
    lr = 0.001
    if epoch > 30:
        lr = 0.0005
    if epoch > 45:
        lr = 0.0003
    return lr

with tf.Session() as sess:
    sess.run(init)
    for epoch in range(training_epochs):
        learning_rate = lr_schedule(epoch)
        avg_cost = 0.
        total_batch = int(mnist.train.num_examples/batch_size)
        for i in range(total_batch):
            batch_xs, batch_ys = mnist.train.next_batch(batch_size)
            _, c = sess.run([optimizer, cost], feed_dict={X: batch_xs, Y: batch_ys})
            avg_cost += c / total_batch
        if (epoch+1) % 5 == 0:
            print("Epoch:", '%02d' % (epoch+1), "cost=", "{:.8f}".format(avg_cost))
    correct_prediction = tf.equal(tf.argmax(hypothesis, 1), tf.argmax(Y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    print('Accuracy:', sess.run(accuracy, feed_dict={X: mnist.test.images, Y: mnist.test.labels}))
