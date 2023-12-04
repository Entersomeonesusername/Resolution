import multiprocessing

bind = f":8000"  # noqa

hard_coded_cpu_limit = min(multiprocessing.cpu_count(), 2) 
workers = hard_coded_cpu_limit * 2 + 1
threads = 4 
