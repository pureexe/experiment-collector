#Load ExperimentCollector
from ExperimentCollector import ExperimentCollector

# Create Collector by call the instructor
# You can pass a file name to use  database in file systeem
# Or leave it blank to use in meoroy database
collector = ExperimentCollector('test.db')

# our experiment will have 3 parameter to adjust 
parameter = {
    'alpha':1,
    'beta':1,
    'gamma':1
} 

# then you write how to compute the parameter
# since it's a function. you also can call other complex code
# or framework like tensorflow and store the result back
# here we will store value to 3 variables name a,b and c
compute = lambda v: {
    'a': -v['alpha']-2*v['beta']-2*v['gamma']+6,
    'b': -v['alpha']-2*v['beta']+v['gamma'],
    'c': v['alpha']-3*v['gamma']/v['beta']
}

# You have to defined how varie the parameter
step = lambda i,s: i+0.25*s

# add experiment info into database
collector.add(
    'change alpha',
    parameter,
    'alpha',
    'study to how alpha value affact the output a,b,c',
    compute_function=compute,
    step_function=step
)
collector.add(
    'varie beta',
    parameter,
    'beta',
    'How beta variable change output a,b,c',
    compute_function=compute,
    step_function = step
)
collector.add(
    'gamma observe',
    parameter,
    'gamma',
    'output a,b,c that create from difference gamma value',
    compute_function=compute,
    step_function = step
)

# run an experiment
# output will store back into  database
# it's can take a long time to run if you called complex code
# such as tensorflow in compute function
collector.run()

# then plot the output to see the trend of parameter on each output
collector.plot()