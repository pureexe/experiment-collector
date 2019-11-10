# Experiment Collector
[![Build Status](https://travis-ci.org/pureexe/experiment-collector.svg?branch=master)](https://travis-ci.org/pureexe/experiment-collector)

Experiment Collector is part of IST-699 Databae System. This is python library that use to store experiment result into `sqlite` then plot the result into scatter chart with trend line for analyze the trend of parameter.

## Getting started
Let's create simple experiment that try to find the trend of parameter **c** when  `c=a*b` and we varie **a** for 10 times by increase 0.25 each step.
```python
from ExperimentCollector import ExperimentCollector
collector = ExperimentCollector()
collector.add('test c=a*b',{'a':2,'b':1},'b',step=10,step_function = lambda i,c: i + 0.25 * c,compute_function = lambda v:{'c': v['a'] * v['b']})
collector.run()
collector.plot()
```

Here is a result 

![Result](https://i.imgur.com/F9Epjq0.png)

## Useful Example

We provide some example that show you how to use Experiment Collector in the [example.py](https://github.com/pureexe/experiment-collector/blob/master/example.py) and also provide an example to use with [Tensorflow](https://tensorflow.org) the popular deep learning framework in the [example_tensorflow.py](https://github.com/pureexe/experiment-collector/blob/master/example_tensorflow.py)

## Usage
### import 
Before you use Experiment Collector you need to import it by
```python
from the.location.of.ExperimentCollector.py import ExperimentCollector
```

### construct
create you collector to store experiment result
```python
collector = ExperimentCollector(database = 'test.db',empty = False)
```
- **database** is a path of database file. you can store it in other directory or store into RAM by using **:memory:**
- **empty** if true the collector will clear any previous result. useful if you have to restart your experimnent frequently

### add
add new experiment into the collector
```python
id = collector.add(name, parameter, variable, description = '',step = 10,
            step_function = lambda initial, current_step: initial+current_step,
            compute_function = lambda inputs: {}
            )
```
- **name** name of the experiment
- **parameter** parameter of the experiement must be define in dict format. for example, `{'a':0,'b':1}` which is parameter **a** has initial value 0 and parameter **b** has initial parameter 1 
- **variable** name of parameter which will varie in this experiement for example 'a'
- **step** number of iteration on this experiment
- **step_function** by default we increase **variable** by 1 in each iteration. but sometime you might want to decrease or increase with exponential growth so you can the function that define the way to change the variable
- **compute_function** defined how each parameter inteact and how many output we get.
- **id** This function is return the id of experiment that store in database. it will be useful if you have manipulate the database by your self though `collector.cursor()`

### empty
abandon all previous experiment
```python
collector.empty()
```

### cursor
get cursor of sqlite database to manipulate directly. if thus library don't provide enough method for you
```python
c = collector.cursor()
```
### commit
do commit of sqlite database. useful if you do insert though the cursor
```python
c = collector.commit()
```

## License
[![MIT License](https://img.shields.io/github/license/pureexe/experiment-collector)](https://github.com/pureexe/experiment-collector/blob/master/LICENSE)

## Contacts
feel free to contact [@pureexe](https://github.com/pureexe) or open an issue for any questions or suggestions.
