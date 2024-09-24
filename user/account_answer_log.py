import os
import numpy as np

from const import KANA

def create_log(account_name):
    log_path = f"user/logs/{account_name}.npy"
    if not os.path.exists(log_path):
        num = len(KANA)
        np.save(log_path,np.ones((num,2)))

