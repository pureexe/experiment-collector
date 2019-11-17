# This is test file that define for pytest
from ExperimentCollector import ExperimentCollector
import sqlite3
import os

def test_general(tmp_path):
    # prepare test
    collector = ExperimentCollector(str(tmp_path / 'test_general.db'),True)
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
    assert os.path.isfile(str(tmp_path / 'test_general.db')) 
    # test if plot exist
    assert os.path.isfile(str(tmp_path / 'plot_out.png'))     
    # connect to db
    conn = sqlite3.connect(str(tmp_path / 'test_general.db'))
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
    conn.close()

def test_crash_handle(tmp_path):
     # prepare test
    collector = ExperimentCollector(str(tmp_path / 'test_crash_handle.db'),True)
    # define essential parameter
    parameter = {'alpha':1,'beta':1,'gamma':1} 
    # make simple crash
    def compute(v):
        raise Exception('simeple crash')
    collector.add(
        'change alpha',
        parameter,
        'alpha',
        'study to how alpha value affact the output a,b,c',
        compute_function=compute,
    )
    # run experiment
    collector.run()
    del collector
     # test if db exist
    assert os.path.isfile(str(tmp_path / 'test_crash_handle.db')) 
    conn = sqlite3.connect(str(tmp_path / 'test_crash_handle.db'))
    c = conn.cursor()
    # test if crash table work correctly
    c.execute('SELECT * FROM crash')
    crashs = c.fetchall()
    assert len(crashs) == 10
    conn.close()

