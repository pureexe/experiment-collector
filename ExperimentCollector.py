import os,sqlite3,dill
import numpy as np 
import matplotlib.pyplot as plt

class ExperimentCollector(object):
    def __init__(self,database = ':memory:',empty = False):
        self.__database_path = database
        self.__connection = None
        if empty:
            self.drop()
        self.create()

    def empty(self):
        """ clear the old experiment """
        self.drop()
        self.create()
    
    def drop(self):
        """ remove table in database """
        c = self.cursor()
        for table in ['experiment','parameter','fact']:
            c.execute("drop table if exists {}".format(table))
        self.commit()

    def create(self):
        """ create table in database """
        c = self.cursor()
        c.execute(
            """
            create table if not exists experiment(
                id integer primary key autoincrement,
                name text,
                description text,
                variable text,
                step integer,
                step_function  blob,
                compute_function blob
            )             
            """
        )
        c.execute(
            """
            create table if not exists parameter(
                experiment integer,
                name text,
                value real
                
            )
            """
        )
        c.execute(
            """
            create table if not exists fact(
                experiment integer,
                step integer,
                variable text,
                value real
            )
            """
        )
        self.commit()


    def connect(self):
        """ connect database """
        self.__connection = sqlite3.connect(self.__database_path)
        self.__connection.row_factory = sqlite3.Row 

    def disconnect(self):
        """ disconnect database """
        self.__connection.close()   
        self.__connection = None
    def commit(self):
        """ commit database after write to update value """
        self.__connection.commit()
    def cursor(self):
        """ get cursor of database to read/write it """
        if self.__connection is None:
            self.connect()
        return self.__connection.cursor()

    def add(self, name, parameter,variable, description = '',step = 10,
            step_function = lambda initial,current_step: initial+current_step,
            compute_function = lambda inputs: {}
        ):
        """ add new experiment """
        c = self.cursor()
        sql_experiment_insert = '''
            INSERT INTO experiment(
                name, description, variable, step,
                step_function, compute_function
            ) VALUES (
                ?,?,?,?,?,?
            )
        '''
        values = (
            name,
            description,
            variable,
            step,
            dill.dumps(step_function),
            dill.dumps(compute_function)
        )
        c.execute(sql_experiment_insert,values)
        self.commit()
        experiment_id = c.lastrowid
        parameter_records = [(experiment_id,k,v) for k,v in parameter.items()]
        sql_parameter_insert = '''
            INSERT INTO parameter(experiment,name,value) 
            VALUES (?,?,?)
        '''
        c.executemany(sql_parameter_insert,parameter_records)
        self.commit()
        return experiment_id
    
    def run(self):
        """ run the experiment """
        c = self.cursor()
        c.execute('SELECT * FROM experiment')
        experiments_rows = c.fetchall()
        for experiment in experiments_rows:
            compute_function = dill.loads(experiment['compute_function'])
            step_function = dill.loads(experiment['step_function'])
            for i in range(experiment['step']):
                exp_id = experiment['id']
                c.execute(
                    'SELECT name,value FROM parameter WHERE ?',
                    (exp_id,)
                )
                inputs = {r['name']:r['value'] for r in c.fetchall()}
                variable = experiment['variable']
                inputs[variable] = step_function(inputs[variable],i) 
                outcome = compute_function(inputs)
                values = [(exp_id,i,k,v) for k,v in outcome.items()]
                values = values + [(exp_id,i,variable,inputs[variable])]
                sql_fact = '''
                    INSERT INTO fact(experiment,step,variable,value) 
                    VALUES (?,?,?,?)
                '''
                c.executemany(sql_fact,values)
        self.commit()

    def plot(self,experiment_id = None):
        """ plot the result chart of the experiment """
        c = self.cursor()
        where_experiment_id = ''
        if not experiment_id is None:
            if isinstance(experiment_id, list):
                exp_ids = ','.join([ str(f) for f in experiment_id ])
                where_experiment_id = ' WHERE id in ({})'.format(exp_ids)
            else:
              where_experiment_id = ' WHERE id = {}'.format(experiment_id)
        c.execute(
            'SELECT id,name,description,variable,step FROM experiment'
            + where_experiment_id
        )
        experiments = c.fetchall()
        exp_count = len(experiments)
        fig, axs = plt.subplots(exp_count)
        if exp_count == 1:
            axs = [axs]
        trend = lambda a,b: np.poly1d(np.polyfit(a, b, 1))(a)
        for i in range(exp_count):
            axs[i].set_title(experiments[i]['name'])
            axs[i].set_xlabel(experiments[i]['description'])
            # build x-axis 
            x_axis = []
            c.execute(
                '''
                SELECT value FROM fact
                WHERE variable = ?
                AND experiment = ?
                ORDER BY step ASC
                ''',
                (
                    experiments[i]['variable'],
                    experiments[i]['id']
                )
            )
            x_axis = [r['value'] for r in c.fetchall()]
            c.execute(
                '''
                    SELECT DISTINCT variable FROM fact 
                    WHERE experiment = ? AND variable != ?
                    ORDER BY variable ASC
                ''',
                (experiments[i]['id'],experiments[i]['variable'])
            )
            variables = [r['variable'] for r in c.fetchall()]
            for variable in variables:
                c.execute(
                    '''
                        SELECT value FROM fact
                        WHERE experiment = ? AND variable = ?
                        ORDER BY step ASC 
                    ''',
                    (experiments[i]['id'], variable)
                )
                y_axis = [r['value'] for r in c.fetchall()]
                axs[i].scatter(x_axis, y_axis)
                axs[i].plot(x_axis,trend(x_axis, y_axis),label=variable)
                axs[i].legend()
        fig.tight_layout()
        # save into image on headless machine
        try:
            plt.show()
        except:
            plt.savefig("plot.png")   
        self.commit()     

    def __del__(self):
        self.disconnect()
    