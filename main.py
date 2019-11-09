from ExperimentCollector import ExperimentCollector

collector = ExperimentCollector('test.db')

parameter = {'alpha':1,'beta':1,'gamma':1} 
compute = lambda v: {
    'a': -v['alpha']-2*v['beta']-2*v['gamma']+6,
    'b': -v['alpha']-2*v['beta']+v['gamma'],
    'c': v['alpha']-3*v['gamma']/v['beta']
}
step = lambda i,s: i+0.25*s

collector.add('change alpha',parameter,'alpha','study to how alpha value affact the output a,b,c',compute_function=compute,step_function = step)
collector.add('varie beta',parameter,'beta','How beta variable change output a,b,c',compute_function=compute,step_function = step)
collector.add('gamma observe',parameter,'gamma','output a,b,c that create from difference gamma value',compute_function=compute,step_function = step)

collector.run()
collector.plot()