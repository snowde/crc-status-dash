#!/usr/bin/env python
import pymongo
import subprocess
from datetime import datetime, timedelta


# Function to return CPUs allocated and total
def return_allocated_total(cluster):
    # Generate output, strip the final newline, split by newlines, grab everything after first entry (it's a title)
    output = subprocess.check_output('sinfo -h -M {0} -o "%15n %t %10C" -t idle,allocated,mix'.format(cluster), shell=True).rstrip().split('\n')[1:]
    # Grab the 'A/I/O/T' part of the output
    count = [0] * len(output)
    for index, item in enumerate(output):
        count[index] = item.split()[-1]
    # Generate lists for allocated and total only
    allocated = [0] * len(count)
    total = [0] * len(count)
    for i, slash_separated_string in enumerate(count):
        spl = [int(x) for x in slash_separated_string.split('/')]
        allocated[i] = spl[0]
        total[i] = spl[3]
    # Return the sum of the lists
    return sum(allocated), sum(total)


# Function to return GPU counts, slightly different due to the nature of retrieving the information
def return_gpu_count(command):
    # Generate output, strip the final newline, split by newlines, grab everything after first entry (it's a title)
    output = subprocess.check_output(command, shell=True).rstrip().split('\n')[1:]
    # Generate the counts by taking the sum of the final column
    count = [0] * len(output)
    for index, item in enumerate(output):
        if not '(null)' in item:
            count[index] = int(item.split(':')[-1])
    return sum(count)        


# Get SMP/MPI Allocated and Total
allocated_smp, total_smp = return_allocated_total('smp')
allocated_mpi, total_mpi = return_allocated_total('mpi')

# GPU nodes are a slightly different because to generate totals/allocated you need two commands
total_gpu = return_gpu_count('sinfo -h -M gpu -o "%n %G"')
allocated_gpu = return_gpu_count('squeue -h -M gpu -t RUNNING -o %b')

# Connect to the MongoDB at mlab
uri = "<URI STRING>"
client = pymongo.MongoClient(uri)
db = client.get_default_database()

# Get the time, rounded down to the nearest 15 minutes
time = datetime.now()
time = time - timedelta(minutes=time.minute % 15,
                        seconds=time.second,
                        microseconds=time.microsecond)
time_string = time.strftime('%m/%d/%y-%H:%M')

# Write data
db['status'].insert_one({'cluster': 'smp', 'allocated': allocated_smp, 'total': total_smp, 'time': time_string})
db['status'].insert_one({'cluster': 'gpu', 'allocated': allocated_gpu, 'total': total_gpu, 'time': time_string})
db['status'].insert_one({'cluster': 'mpi', 'allocated': allocated_mpi, 'total': total_mpi, 'time': time_string})
