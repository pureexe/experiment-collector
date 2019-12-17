# simple example of experimentcollector

#Load ExperimentCollector
from experimentcollector import ExperimentCollector

# Create Collector by call the instructor
# You can pass a file name to use  database in file systeem
# Or leave it blank to use in meoroy database
# You also pass empty=True parameter to clear table if you want to restart experiment
# or empty=False to continue your work from last time
collector = ExperimentCollector('test.db',empty=True)

# our experiment will have 3 parameter to adjust 
collector.initial({
    'alpha':1,
    'beta':1,
    'gamma':1
})

# then you write how to compute the parameter
# since it's a function. you also can call other complex code
# or framework like tensorflow and store the result back
# here we will store value to 3 variables name a,b and c
collector.compute(lambda v: {
    'a': -v['alpha']-2*v['beta']-2*v['gamma']+6,
    'b': -v['alpha']-2*v['beta']+v['gamma'],
    'c': v['alpha']-3*v['gamma']/v['beta']
})

# You have to defined how vary the parameter
collector.step([1,3,4,8,10])

# add experiment info into database
collector.add(
    'alpha',
    'change alpha',
    'study to how alpha value affact the output a,b,c'
)
collector.add(
    'beta',
    'vary beta',
    'How beta variable change output a,b,c'
)
collector.add(
    'gamma',
    'gamma observe',
    'output a,b,c that create from difference gamma value',
)

# run an experiment
# output will store back into  database
# it's can take a long time to run if you called complex code
# such as tensorflow in compute function
collector.run()

# then plot the output to see the trend of parameter on each output
collector.plot()