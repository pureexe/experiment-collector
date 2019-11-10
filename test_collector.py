# This is test file that define for pytest
from ExperimentCollector import ExperimentCollector
import sqlite3
import os

def test_01(tmp_path):
    # prepare test
    collector = ExperimentCollector(str(tmp_path / 'test_01.db'),True)
    # define essential parameter
    parameter = {'alpha':1,'beta':1,'gamma':1} 
    compute = lambda v: {
        'a': -v['alpha']-2*v['beta']-2*v['gamma']+6,
        'b': -v['alpha']-2*v['beta']+v['gamma'],
        'c': v['alpha']-3*v['gamma']/v['beta']
    }
    step = lambda i,s: i+0.25*s
    # add a single experiment
    collector.add(
        'change alpha',
        parameter,
        'alpha',
        'study to how alpha value affact the output a,b,c',
        compute_function=compute,
        step_function=step
    )
    # run experiment
    collector.run()
    # save plot
    collector.plot(image_path=tmp_path / 'plot_out.png')
    del collector
    # run test
    # test if db exist
    assert os.path.isfile(str(tmp_path / 'test_01.db')) 
    # test if plot exist
    assert os.path.isfile(str(tmp_path / 'plot_out.png'))     
    # connect to db
    conn = sqlite3.connect(str(tmp_path / 'test_01.db'))
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    # test if experiment table work correctly
    c.execute('SELECT * FROM experiment')
    exps = c.fetchall()
    assert len(exps) == 1
    assert exps[0]['id'] == 1
    assert exps[0]['name'] == 'change alpha'
    assert exps[0]['description'] == 'study to how alpha value affact the output a,b,c'
    assert exps[0]['variable'] == 'alpha'
    assert exps[0]['step'] == 10
    # test if parameter table work correctly
    c.execute('SELECT * FROM parameter ORDER BY name')
    parameters = c.fetchall()
    assert len(parameters) == 3
    names = ['alpha','beta','gamma']
    for i in range(3):
        assert parameters[i]['experiment'] == 1
        assert parameters[i]['value'] == 1
        assert parameters[i]['name'] == names[i]
    # test if fact table work correctly
    c.execute('SELECT * FROM fact')
    facts = c.fetchall()
    assert len(facts) == 40
    c.close()
