HEADER = """#!/bin/zsh

export SOME_VAR=123
export PYTHONPATH=$PYTHONPATH:/scratch/cluster/stephane/

cd /scratch/cluster/stephane/Carla_0.9.10

"""

#PARAMS = {
#        'arg1': [2020, 1337],
#        'arg2': ['foo', 'bar']
#        }


#def get_job(arg1, arg2):
#    return HEADER + ('python3 run.py %s %s' % (arg1, arg2)), f'exp-name-{arg1}-{arg2}'

def get_job():
    return HEADER + ('./CarlaUE4.sh')
