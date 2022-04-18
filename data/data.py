import numpy as np, matplotlib.pyplot as plt
from scipy.interpolate import interp1d

fd = open("C:\\Users\\ilatei\\Desktop\\coflowgym\\data\\data-4.1.txt", "r")
ff = open("output.txt", "w")
# up down flow xdate
# list data name

trace_data = dict()
trace_time = 1440
trace_job = 0

line = fd.readline()
datas = eval(line)
x = [i for i in range(24 * 12 + 1)]
x = [i * 5 for i in x] 
xx = [i for i in range(24*60)]

for data0 in datas["down"]:
    data_name = data0["name"]
    data_data = data0["data"]
    if len(data_data) == 0:
        break
    data_data.append(data_data[0])
    f = interp1d(x,data_data,kind="cubic")
    yy = f(xx)
    trace_data[data_name] = yy

trace_job = trace_data.__len__()
job_index = 1
ff.write("1 {} {}\n".format(trace_job, trace_time))
for name in trace_data:
    ff.write("{} 1 ".format(job_index))
    job_index += 1
    for num in trace_data[name]:
        ff.write("{} ".format(int(num / 1024)))
    ff.write("0\n")
