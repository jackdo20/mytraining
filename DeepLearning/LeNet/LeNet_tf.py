import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

#MNIST data 
mnist = input_data.read_data_sets("../../MNIST", one_hot = True)

#input data(28X28,grey)
x = tf.placeholder("float", [None,784])
y_= tf.placeholder("float",[None,10])

x_reshape = tf.reshape(x,[-1,28,28,1])
w1 = tf.Variable(tf.random_normal([5,5,1,6],stddev=0.1)) #28
#b1 = tf.Variable(tf.random_normal([6]))
b1 = tf.constant(0.1,shape=[6])
con1 = tf.nn.conv2d(x_reshape,w1,strides=[1,1,1,1],padding="SAME") # tf.nn.avg_pool, tf.nn.sigmoid
#lay1_out = tf.nn.relu(con1+b1)
lay1_out = tf.nn.relu(con1+b1)
#mpool1 = tf.nn.max_pool(con1,ksize = [1,2,2,1],strides=[1,2,2,1],padding="VALID")
mpool1 = tf.nn.max_pool(lay1_out,ksize = [1,2,2,1],strides=[1,2,2,1],padding="SAME")

#2nd Conv
w2=tf.Variable(tf.random_normal([5,5,6,16],stddev=0.1)) #14
#b2 = tf.Variable(tf.random_normal([16]))
b2 = tf.constant(0.1,shape = [16])
con2 = tf.nn.conv2d(mpool1,w2,strides=[1,1,1,1],padding="SAME")
#lay2_out = tf.nn.relu(con2 + b2)
lay2_out = tf.nn.relu(con2 + b2)
mpool2 = tf.nn.max_pool(lay2_out,ksize=[1,2,2,1],strides=[1,2,2,1],padding="SAME")
##print(mpool2)


#3rd Conv
w3 = tf.Variable(tf.random_normal([5,5,16,120],stddev=0.1)) #7
#b3 = tf.Variable(tf.random_normal([120]))
b3 = tf.constant(0.1,shape = [120])
con3 = tf.nn.conv2d(mpool2,w3,strides=[1,1,1,1],padding="SAME")
lay3_out = tf.nn.relu(con3 + b3)
mpool3 = tf.nn.max_pool(lay3_out,ksize=[1,2,2,1],strides=[1,2,2,1],padding="SAME")


#full connect1
w_fc1 = tf.Variable(tf.random_normal([4*4*120, 1024],stddev=0.1))
#b_fc1 = tf.Variable(tf.random_normal([1024]))
b_fc1 = tf.constant(0.1,shape = [1024])

mpool3_flat = tf.reshape(mpool3,[-1,4*4*120])
#fc1_out = tf.nn.relu(tf.matmul(mpool2_flat, w_fc1)+b_fc1)
fc1_out = tf.nn.relu(tf.matmul(mpool3_flat, w_fc1)+b_fc1)

#full connect 2
w_fc2 = tf.Variable(tf.random_normal([1024,10],stddev=0.1))
#b_fc2 = tf.Variable(tf.random_normal([10]))
b_fc2 = tf.constant(0.1,shape = [10])
#drop_out
keep_prob = tf.placeholder("float")
fc1_out_drop = tf.nn.dropout(fc1_out,keep_prob)

#y = tf.nn.softmax(tf.matmul(fc1_out,w_fc2) + b_fc2)
y = tf.nn.softmax(tf.matmul(fc1_out_drop,w_fc2) + b_fc2)

#test
cross_entropy = -tf.reduce_sum(y_* tf.log(y))
step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(y,1),tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction,"float"))
sess = tf.Session()
sess.run(tf.initialize_all_variables())
for i in range(20000):
    batch = mnist.train.next_batch(100)
    if i%1000 == 0:
        train_accuracy = sess.run(accuracy,feed_dict={x:batch[0],y_:batch[1],keep_prob:1.0})
        print "Steo %d, accuracy is: %g " %(i,train_accuracy)
    sess.run(step, feed_dict={x:batch[0],y_:batch[1],keep_prob: 0.5})

print "Total Accuracy: %g" %sess.run(accuracy,feed_dict={x:mnist.test.images, y_:mnist.test.labels,keep_prob: 1.0})
sess.close()
