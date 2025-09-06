from random import uniform

from config import dep_step


def get_k_signal(balance: float, next_k: float | None):
    if next_k:
        return next_k

    if balance < dep_step:
        signal = round(uniform(1.2, 1.5), 2)
    elif balance < dep_step * 2:
        signal = round(uniform(1.3, 3), 2)
    else:
        signal = round(uniform(1.4, 3), 2)
    
    return signal