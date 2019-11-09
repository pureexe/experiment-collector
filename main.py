from ExperimentCollector import ExperimentCollector

collector = ExperimentCollector('test.db')
def calculate(inputs):
    return {'b':inputs['a'] + 20}
collector.add('hello',{'a':0},'a',compute_function=calculate)
collector.run()
collector.plot()