import numpy as np
from rich import print as rprint
from main import tone_list

if __name__ == '__main__':
    memory = np.load("memory.npy")
    for i,tone in enumerate(tone_list):
        rprint(f"[green]{tone}[/green]: {memory[i][0]}/{memory[i][1]}")