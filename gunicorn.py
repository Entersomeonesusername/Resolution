# import multiprocessing

# bind = f":8000"  # noqa

# hard_coded_cpu_limit = min(multiprocessing.cpu_count(), 2) 
# workers = hard_coded_cpu_limit * 2 + 1
# threads = 4 
# gunicorn.py

import multiprocessing

bind = ":8000"
workers = 3  # Adjust the number of workers based on your requirements
threads = 4
timeout = 900  # Increase the timeout value as needed

# Optional: You can configure other Gunicorn settings here

# Hard-coded CPU limit for worker count
hard_coded_cpu_limit = min(multiprocessing.cpu_count(), 2) 
workers = hard_coded_cpu_limit * 2 + 1
#cpu_count = multiprocessing.cpu_count()
# workers = cpu_count * 2 + 1
# # Ensure the number of workers is within a reasonable range
# # Log the final number of workers
# print(f"Number of Gunicorn workers: {workers}")
