import os, sqlite3,pkgutil
import numpy as np 
import matplotlib.pyplot as plt

class ExperimentCollector(object):
    def __init__(self,database = ':memory:', empty = False):
        self.__database_path = database
        self.__connection = None
        self.__step_function = lambda i,s: i + 1*s
        self.__step = 10
        self.__initial_dict = {}
        self.__compute_function = None
        if empty:
            self.drop()
        self.create()

    def initial(self,intial_values):
        self.__initial_dict = intial_values

    def step(self,step_function,iteration = 10):
        if callable(step_function):
            self.__step_function = step_function
            self.__step = iteration
        else:
            list_data = step_function
            if not isinstance(list_data,list):
                list_data = list(list_data)
            self.__step_function = lambda _,x: list_data[x]
            self.__step = len(list_data)

    def compute(self,compute_function):
        self.__compute_function = compute_function

    def empty(self):
        """ clear the old experiment """
        self.drop()
        self.create()
    
    def drop(self):
        """ remove table in database """
        c = self.cursor()
        for table in ['experiment','fact']:
            c.execute("drop table if exists {}".format(table))
        self.commit()

    def create(self):
        """ create table in database """
        c = self.cursor()
        byte_schema = pkgutil.get_data(__package__, 'schema.sql')
        c.executescript(byte_schema.decode('utf-8'))
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

    def add(self ,variable, name=None, description=None):
        """ add new experiment """
        if not variable in self.__initial_dict:
            raise NameError('"{}" must define in initial method before use'.format(variable))
        c = self.cursor()
        sql_experiment_insert = '''
            INSERT INTO experiment(
                exp_name,
                exp_description,
                var_name
            ) VALUES (
                ?,?,?
            )
        '''
        values = (
            name,
            description,
            variable
        )
        c.execute(sql_experiment_insert,values)
        self.commit()  
        return c.lastrowid 
    
    def run(self):
        """ run the experiment """
        if self.__compute_function == None:
            raise NotImplementedError("compute function is require to implement by user")
        c = self.cursor()
        c.execute('SELECT * FROM experiment')
        experiments_rows = c.fetchall()
        for experiment in experiments_rows:
            for i in range(self.__step):
                exp_id = experiment['exp_id']                
                inputs = self.__initial_dict.copy()
                variable = experiment['var_name']
                inputs[variable] = self.__step_function(inputs[variable], i)
                try:
                    outcome = self.__compute_function(inputs)
                except BaseException as err:
                    sql_crash = '''
                        INSERT INTO fact(exp_id,step_id,var_name,val,errmsg) 
                        VALUES (?,?,?,?,?)
                    '''
                    c.execute(sql_crash,(exp_id,i,variable,inputs[variable],str(err)))
                else:
                    values = [(exp_id,i,k,v) for k,v in outcome.items()]
                    values = values + [(exp_id,i,variable,inputs[variable])]
                    sql_fact = '''
                        INSERT INTO fact(exp_id,step_id,var_name,val) 
                        VALUES (?,?,?,?)
                    '''
                    c.executemany(sql_fact,values)
                finally:
                    self.commit()

    def plot(self,experiment_id = None,image_path = None):
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
            'SELECT exp_id,exp_name,exp_description,var_name FROM experiment'
            + where_experiment_id
        )
        experiments = c.fetchall()
        exp_count = len(experiments)
        fig, axs = plt.subplots(exp_count)
        if exp_count == 1:
            axs = [axs]
        trend = lambda a,b: np.poly1d(np.polyfit(a, b, 1))(a)
        for i in range(exp_count):
            axs[i].set_title(experiments[i]['exp_name'])
            axs[i].set_xlabel(experiments[i]['exp_description'])
            # build x-axis 
            x_axis = []
            c.execute(
                '''
                SELECT val FROM fact
                WHERE var_name = ?
                AND exp_id = ?
                ORDER BY step_id ASC
                ''',
                (
                    experiments[i]['var_name'],
                    experiments[i]['exp_id']
                )
            )
            x_axis = [r['val'] for r in c.fetchall()]
            c.execute(
                '''
                    SELECT DISTINCT var_name FROM fact 
                    WHERE exp_id = ? AND var_name != ?
                    ORDER BY var_name ASC
                ''',
                (experiments[i]['exp_id'],experiments[i]['var_name'])
            )
            variables = [r['var_name'] for r in c.fetchall()]
            for variable in variables:
                c.execute(
                    '''
                        SELECT val FROM fact
                        WHERE exp_id = ? AND var_name = ?
                        ORDER BY step_id ASC 
                    ''',
                    (experiments[i]['exp_id'], variable)
                )
                y_axis = [r['val'] for r in c.fetchall()]
                axs[i].scatter(x_axis, y_axis)
                axs[i].plot(x_axis,trend(x_axis, y_axis),label=variable)
                axs[i].legend()
        fig.tight_layout()
        # save into image on headless machine
        if not image_path is None:
            plt.savefig(image_path)
        else:
            try:
                plt.show()
            except:
                plt.savefig("plot.png")   
        self.commit()     

    def __del__(self):
        self.disconnect()
    