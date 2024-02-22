import numpy as np
import time

def generate_sample_data():

    int_random_array = np.random.rand(5)*50
    names = ['volts', 'amps', 'power', 'temp', 'randvar1']
    old_dict = {n: int_random_array[i] for i, n in enumerate(names)}
    while True:
        rand_increment = np.random.uniform(-1, 1, 5)

        new_dict = {name: old_dict[name]+rand_increment[i] for i, name in enumerate(names)}
        print(new_dict)
        time.sleep(1)


generate_sample_data()