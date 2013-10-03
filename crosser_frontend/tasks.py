import subprocess
import datetime
from celery import task
 
@task()
def process_scheme(calc_id): 
    calc = Calculation.objects.get(pk=calc_id)
    calc.start_time = datetime.datetime.now() 
    calc.save()
    output_dir = "../static/" + calc.output_dir()
    url = calc.backend_url()
    cmd = ["mkdir", "-p",  output_dir] 
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE)

    out, err = p.communicate()   
    ret = p.wait()

    cmd = ["./crosser/runCrosser.sh", 
                "-u", url, 
                "-o", output_dir] 
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE)

    out, err = p.communicate()   
    ret = p.wait()

    cmd = ["./crosser/runR.RScript", output_dir]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE)

    out, err = p.communicate()   
    ret = p.wait()

    del calc
    calc = Calculation.objects.get(pk=calc_id)
    calc.end_time  = datetime.datetime.now() 
    calc.save()

    return out, err, ret 

from crosser_frontend.models import Calculation
