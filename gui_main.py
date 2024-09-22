from rich import print as rprint
from numpy.random import choice,uniform
import numpy as np
import os
import streamlit as st
import time
from const import tone_list,pron_list

if 'process_done' not in st.session_state:
    st.session_state.process_done = True
if 'view_the_answer' not in st.session_state:
    st.session_state.view_the_answer = False
if 'show' not in st.session_state:
    st.session_state.show = 0
if 'pos' not in st.session_state:
    st.session_state.pos = -1
if 'last_pos' not in st.session_state:
    st.session_state.last_pos = -1

if __name__ == '__main__':
    nums = len(tone_list)
    memory = np.load("memory.npy")
    
    
    st.title('五十音记忆')
    try:
        
        if st.session_state.process_done == True:
            prob = np.exp(memory[:,1] / memory[:,0] / 1.45) / np.log(memory[:,1] + 1)
            prob = prob / np.sum(prob)
            while st.session_state.pos == st.session_state.last_pos:
                st.session_state.pos = choice(nums,size=1,replace=True,p=prob)[0]
            st.session_state.show = int(uniform(0,2))
        # print("st.session_state.process_done",st.session_state.process_done)
        st.session_state.process_done = False
        
        
        if st.session_state.show == 0:
            st.text(f"what is the tone of {pron_list[st.session_state.pos % 46]}?")
        elif st.session_state.show == 1:
            st.text(f"what is the pronunciation of {tone_list[st.session_state.pos]}?")

        # print("st.session_state.view_the_answer",st.session_state.view_the_answer)
        if not st.session_state.view_the_answer:
            if st.button("view the answer","vta"):
                st.session_state.view_the_answer = True
                st.rerun()
        
        # print("st.session_state.view_the_answer",st.session_state.view_the_answer)
        if st.session_state.view_the_answer:
            if st.session_state.show == 0:
                st.text(f"{tone_list[st.session_state.pos % 46]} & {tone_list[st.session_state.pos % 46 + 46]}")
            elif st.session_state.show == 1:
                st.text(f"{pron_list[st.session_state.pos % 46]}")

            st.text("Is your answer correct?")      
            col1, col2 = st.columns(2)
            with col1:
                if st.button('Yes'):
                    memory[st.session_state.pos][0] += 1
                    st.session_state.process_done = True
                    st.session_state.view_the_answer = False
            with col2:
                if st.button('No'):
                    st.session_state.process_done = True
                    st.session_state.view_the_answer = False
            
            if st.session_state.process_done:
                memory[st.session_state.pos][1] += 1
                st.session_state.last_pos = st.session_state.pos
                st.rerun()
        
    except KeyboardInterrupt:
        print("saving yout practice results")
        np.save("memory.npy",memory)
