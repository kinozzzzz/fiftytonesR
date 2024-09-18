from rich import print as rprint
from numpy.random import choice,uniform
import numpy as np
import os

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
    'わ','を',
    'ん',
    'ア','イ','ウ','エ','オ',
    'カ','キ','ク','ケ','コ',
    'サ','シ','ス','セ','ソ',
    'タ','チ','ツ','テ','ト',
    'ナ','ニ','ヌ','ネ','ノ',
    'ハ','ヒ','フ','ヘ','ホ',
    'マ','ミ','ム','メ','モ',
    'ヤ','ユ','ヨ',
    'ラ','リ','ル','レ','ロ',
    'ワ','ヲ',
    'ン'
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
    'wa','wo',
    'n'
]


if __name__ == '__main__':
    nums = len(tone_list)
    memory = np.load("memory.npy")

    if os.name == "posix":
        clear_cmd = "clear"
    elif os.name == "nt":
        clear_cmd = "cls"
    try:
        last_pos = -1
        pos = -1
        while True:
            os.system(clear_cmd)
            
            prob = np.exp(memory[:,1] / memory[:,0] / 1.45) / np.log(memory[:,1] + 1)
            prob = prob / np.sum(prob)
            # print(nums,prob.shape)
            while pos == last_pos:
                pos = choice(nums,size=1,replace=True,p=prob)[0]
            show = int(uniform(0,2))
            if show:
                rprint(f"what is the tone of [yellow]{pron_list[pos % 46]}[/yellow]?",end="")
                input()
                rprint(f"[green]{tone_list[pos % 46]}[/green] & [green]{tone_list[pos % 46 + 46]}[/green]")
                
            else:
                rprint(f"what is the pronunciation of [yellow]{tone_list[pos]}[/yellow]?",end="")
                input()
                rprint(f"[green]{pron_list[pos % 46]}[/green]")
            answer = input()
            if not answer:
                memory[pos][0] += 1
            memory[pos][1] += 1


            last_pos = pos
    except KeyboardInterrupt:
        print("saving yout practice results")
        np.save("memory.npy",memory)
