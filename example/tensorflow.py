# here is example to use Experiment Collector with tensorflow 2.0

# import from above directory
import sys
sys.path.append("..")

# load tensorflow and Experimental Collector
import tensorflow as tf
from experimentcollector import ExperimentCollector

# create Collector object 
# database will be store into memory by default
collector = ExperimentCollector()

# define tensorflow's computation graph
# for example c = a^2 * b
@tf.function
def compute_graph(inputs):
    a = tf.constant(inputs['a'])
    b = tf.constant(inputs['b'])
    result = tf.multiply(a ** 2, b)
    return result

# create compute function that call the tensorflow's computation graph
# and convert it back to float to store in variable name c 
def compute(inputs):
    outputs = compute_graph(inputs).numpy()
    return {'c':float(outputs)}

# define parameter a and b to use in the computation graph
parameter = {
    'a':1,
    'b':3
} 

# add new experiment that increase a by 1 for 10 times
collector.add(
    'tensorflow computation graph',
    parameter,
    'a',
    compute_function=compute,
)

# run experiment 
# tensorflow's computation graph will called by this step
collector.run()

# plot the result
collector.plot()