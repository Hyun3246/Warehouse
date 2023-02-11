import tensorflow as tf

print('Define constant tensors')
a = tf.constant(2)
print('a = %i'%a)
b = tf.constant(3)
print('b = %i'%b)

print("Running operations, without tf.Session")
c = a + b
print('a + b = %i'%c)
d = a * b
print('a * b = %i'%d)

d = tf.matmul(a, b)
print('a * b = %s'%d)