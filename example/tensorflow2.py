# here is example to use Experiment Collector with tensorflow 2.0

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

collector.compute(compute)

# define parameter a and b to use in the computation graph
collector.initial({
    'a':1,
    'b':3
})

# add new experiment that increase a by 1 for 10 times
collector.step(range(1,11))
collector.add(
    'a',
    'tensorflow computation graph',
)

# run experiment 
# tensorflow's computation graph will called by this step
collector.run()

# plot the result
collector.plot()