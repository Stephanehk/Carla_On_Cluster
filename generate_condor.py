import os

from pathlib import Path


SUBMIT = """Executable = train_{job_name}.sh

+Group="GRAD"
+Project="AI_ROBOTICS"
+ProjectDescription="Training model"
+GPUJob=true

Requirements=(TARGET.GPUSlot && Eldar == True)
Rank=memory
Universe=vanilla
Getenv=True
Notification=Complete

Log={log_dir}/$(ClusterId)_{job_name}.log
Output={log_dir}/$(ClusterId)_{job_name}.out
Error={log_dir}/$(ClusterId)_{job_name}.err

Queue 1
"""

import sys
import itertools
import importlib


def product_dict(**kwargs):
    keys = kwargs.keys()
    vals = kwargs.values()

    for instance in itertools.product(*vals):
        yield dict(zip(keys, instance))


params_py = Path(sys.argv[1])
package_path = str(params_py).split('.')[0].replace('/', '.')
package = importlib.import_module(package_path)

log_dir = params_py.resolve().parent / 'logs'
log_dir.mkdir(exist_ok=True)


for i, job_dict in enumerate(product_dict(**package.PARAMS)):
    job_name = '_'.join('%s=%s' % (k, v) for k, v in sorted(job_dict.items()))
    job = package.get_job(**job_dict)

    (params_py.parent / ('%s.submit' % job_name)).write_text(SUBMIT.format(log_dir=log_dir, job_name=job_name))
    (params_py.parent / ('%s.sh' % job_name)).write_text(job)

    os.chmod(params_py.parent / ('%s.sh' % job_name), 509)

    print(job_name)