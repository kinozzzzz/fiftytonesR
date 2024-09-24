import numpy as np
from rich import print as rprint
from const import KANA

if __name__ == '__main__':
    memory = np.load("user/logs/kkk.npy")
    for i,tone in enumerate(KANA):
        rprint(f"[green]{tone[0]}[/green]: {memory[i][0]}/{memory[i][1]}")