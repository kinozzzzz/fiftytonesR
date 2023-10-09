from rich import print as rprint
from numpy.random import choice,uniform
import numpy as np
import os
from pynput.keyboard import Key,Listener

tone_list = [
    'あ','い','う','え','お',
    'か','き','く','け','こ',
    'さ','し','す','せ','そ',
    'た','ち','つ','て','と',
    'な','に','ぬ','ね','の',
    'は','ひ','ふ','へ','ほ',
    'ま','み','む','め','も',
    'や','ゆ','よ',
    'ら','り','る','れ','ろ',
    'わ','を'
]
pron_list = [
    'a','i','u','e','o',
    'ka','ki','ku','ke','ko',
    'sa','shi','su','se','so',
    'ta','chi','tsu','te','to',
    'na','ni','nu','ne','no',
    'ha','hi','fu','he','ho',
    'ma','mi','mu','me','mo',
    'ya','yu','yo',
    'ra','ri','ru','re','ro',
    'wa','wo'
]


if __name__ == '__main__':
    nums = len(tone_list)
    memory = np.load("memory.npy")
    try:
        last_pos = -1
        pos = -1
        while True:
            os.system("cls")

            prob = np.exp(memory[:,1] / memory[:,0] / 1.45) / np.log(memory[:,1] + 1)
            prob = prob / np.sum(prob)
            while pos == last_pos:
                pos = choice(nums,size=1,replace=True,p=prob)[0]
            show = int(uniform(0,2))
            if show:
                rprint(f"what is the pronunciation of [yellow]{tone_list[pos]}[/yellow]?",end="")
                input()
                rprint(f"[green]{pron_list[pos]}[/green]")
            else:
                rprint(f"what is the tone of [yellow]{pron_list[pos]}[/yellow]?",end="")
                input()
                rprint(f"[green]{tone_list[pos]}[/green]")
            answer = input()
            if not answer:
                memory[pos][0] += 1
            memory[pos][1] += 1


            last_pos = pos
    except KeyboardInterrupt:
        np.save("memory.npy",memory)
