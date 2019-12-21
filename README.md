# Experiment Collector
[![Build Status](https://travis-ci.org/pureexe/experiment-collector.svg?branch=master)](https://travis-ci.org/pureexe/experiment-collector)

Experiment Collector is part of IST-699 Database  System. This is python library that use to store experiment result into [SQLite](https://docs.python.org/3/library/sqlite3.html) then plot the result into scatter chart with trend line for analyse the trend of parameter.

**features**
- support multiple input parameter
- support multiple output parameter
- easy integrate with other computation framework like [NumPy](https://numpy.org/) or [Tensorflow](https://tensorflow.org), we also provide example for use with Tensorflow

**limitation**
- Experiment Collector only support floating point as input parameter and experiment result. we don't support input and output in other data type like string,image or tensor because we can't plot trend line from that data type

## Getting started
### Let's do experiment!

Let's create simple experiment that try to find the trend of parameter **c** when `c=a*b` and we varie **a** for 10 times by increase 0.25 each step.

```python
from experimentcollector import ExperimentCollector

collector =  ExperimentCollector()
collector.initial({'a':2,'b':1})
collector.compute(lambda v:{'c': v['a'] * v['b']}))
collector.step(lambda i,c: i + 0.25 * c, 10)
collector.add('b','test c=a*b')
collector.run()
collector.plot()
```

Here is a result

![Result](https://i.imgur.com/F9Epjq0.png)

### Prerequisite
You need to reach this requirement to run example code

-  **Python 3.x**

-  **numpy, matplotlib** - those require to plot trend line

- (optional) **tensorflow >= 2.0** - use to run example_tensorflow.py, no need if you don't want to use with tensorflow

  

You can install those require package (except [Tensorflow](https://tensorflow.org)! it's only use to run [example_tensorflow.py](https://github.com/pureexe/experiment-collector/blob/master/example/tensorflow2.py)) by run

```bash
pip install -r requirements.txt
```

### Installation

You can install this module using pip by following this command.

```bash
git clone https://github.com/pureexe/experiment-collector.git
pip install .
```

After installed, you can use it from anywhere in your computer by `from experimentcollector import ExperimentCollector`

## Useful Example

We provide some example that show you how to use Experiment Collector in the [example.py](https://github.com/pureexe/experiment-collector/blob/master/example/simple.py) and also provide an example to use with [Tensorflow](https://tensorflow.org) the popular deep learning framework in the [example_tensorflow.py](https://github.com/pureexe/experiment-collector/blob/master/example/tensorflow.py)

## Usage
### import
Before you use Experiment Collector you need to import it by
```python
from experimentcollector import ExperimentCollector
```

### construct
create you collector to store experiment result
```python

collector =  ExperimentCollector(database  =  'test.db',empty  =  False)

```

-  **database** is a path of database file. you can store it in other directory or store into RAM by using **:memory:**

-  **empty** if true the collector will clear any previous result. useful if you have to restart your experimnent frequently

  

### add
add new experiment into the collector
```python
id  = collector.add(variable, name=None, description=None):
```
-  **variable** name of parameter which will vary in this experiement for example 'a'

-  **name** name of the experiment

-  **id** This function is return the id of experiment that store in database. it will be useful if you have manipulate the database by your self though `collector.cursor()`

### step
define how we increase parameter 
```python
collector.step(step_function,iteration  =  10)
```
-  **step_function**  sometime you might want to decrease or increase with exponential growth so you can the function that define the way to change the variable, you also can press list to be step function like  `[1,3,5,7]` 
- **iteration** number of times to repeat **step_function** However, If **iteration** is list or generator instead of callable function,  **iteration** will be ignore
### initial
```python
collector.initial(intial_values)
```
-  **intial_values** dictionary of intial value like `{a:1,b:2}`
### compute
defined how each value that we define in intial interact is other
```python
collector.compute(compute_function)
```
-  **compute_function** defined how each parameter inteact and how many output we get.

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