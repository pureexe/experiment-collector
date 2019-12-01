# This is test file that define for pytest
from experimentcollector import ExperimentCollector
import sqlite3
import os

def test_general(tmp_path):
    # prepare test
    collector = ExperimentCollector(str(tmp_path / 'test_general.db'),True)
    # define essential parameter
    collector.initial({
        'alpha':1,
        'beta':1,
        'gamma':1
    })
    collector.compute(lambda v: {
        'a': -v['alpha']-2*v['beta']-2*v['gamma']+6,
        'b': -v['alpha']-2*v['beta']+v['gamma'],
        'c': v['alpha']-3*v['gamma']/v['beta']
    })
    collector.step(lambda i,s: i+0.25*s,10)
    # add a single experiment
    collector.add(
        'alpha',
        'change alpha',
        'study to how alpha value affact the output a,b,c'
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
    assert exps[0]['exp_id'] == 1
    assert exps[0]['exp_name'] == 'change alpha'
    assert exps[0]['exp_description'] == 'study to how alpha value affact the output a,b,c'
    assert exps[0]['var_name'] == 'alpha'
    # test if fact table work correctly
    c.execute('SELECT * FROM fact')
    facts = c.fetchall()
    assert len(facts) == 40
    conn.close()