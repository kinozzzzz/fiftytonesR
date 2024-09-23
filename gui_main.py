from rich import print as rprint
from numpy.random import choice, uniform
import numpy as np
import os
import streamlit as st
import time
import re
import json
from const import tone_list, pron_list, KANA, IVCODE

if "login" not in st.session_state:
    st.session_state.login = False
if "register" not in st.session_state:
    st.session_state.register = False

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
    st.title('五十音记忆')

    if not st.session_state.login:
        # 登录界面
        user_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users")
        users = [file_name[: -5] for file_name in os.listdir(user_dir)]
        if not st.session_state.register:
            username = st.text_input("用户名")
            password = st.text_input("密码", type="password")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("登录"):
                    if username in users:
                        with open(os.path.join(user_dir, f"{username}.json"), "r") as file:
                            user_info = json.load(file)
                        if password == user_info["password"]:
                            st.session_state.login = True
                            st.rerun()
                        else:
                            st.error("用户名或密码错误！")
                    else:
                        st.error("用户名或密码错误！")   
            with col2:
                if st.button("注册"):
                    st.session_state.register = True
                    st.rerun()
        # 注册界面
        else:
            username = st.text_input("用户名", key="regs_un")
            password = st.text_input("密码", type="password", key="regs_pw")
            invite_code = st.text_input("邀请码")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("返回登录"):
                    st.session_state.register = False
                    st.rerun()                      
            with col2:
                if st.button("注册"):
                    if invite_code != IVCODE:
                        st.error("邀请码错误！")
                    elif username in users:
                        st.error("用户名已存在！")
                    elif not re.search(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", password):
                        st.error("密码应不少于8位, 且同时包含英文字母和数字")
                    else:
                        user_info = {"username": username, 
                                     "password": password}
                        try:
                            with open(os.path.join(user_dir, f"{username}.json"), "w") as file:
                                json.dump(user_info, file, indent=4)
                            st.success("注册成功")
                        except Exception as e:
                            st.error(e)
                            st.error("用户名不符合规范！")
    else:
        nums = len(KANA)
        
        if st.session_state.process_done == True:
            # prob = np.exp(memory[:,1] / memory[:,0] / 1.45) / np.log(memory[:,1] + 1)
            # prob = prob / np.sum(prob)
            while st.session_state.pos == st.session_state.last_pos:
                # st.session_state.pos = choice(nums,size=1,replace=True,p=prob)[0]
                st.session_state.pos = np.random.choice(nums, size=1, replace=True)[0]
            # st.session_state.show = int(uniform(0,2))
            st.session_state.show = np.random.randint(0, 3)
        # print("st.session_state.process_done",st.session_state.process_done)
        st.session_state.process_done = False
        
        
        if st.session_state.show in [0, 1]:
            st.text(f"what is the pronunciation of {KANA[st.session_state.pos][st.session_state.show]}?")
        elif st.session_state.show == 2:
            st.text(f"what is the tone of {KANA[st.session_state.pos][st.session_state.show]}?")

        # print("st.session_state.view_the_answer",st.session_state.view_the_answer)
        if not st.session_state.view_the_answer:
            if st.button("view the answer","vta"):
                st.session_state.view_the_answer = True
                st.rerun()
        
        # print("st.session_state.view_the_answer",st.session_state.view_the_answer)
        if st.session_state.view_the_answer:
            if st.session_state.show in [0, 1]:
                st.text(f"{KANA[st.session_state.pos][2]}")
            elif st.session_state.show == 2:
                st.text(f"{KANA[st.session_state.pos][0]} & {KANA[st.session_state.pos][1]}")

            st.text("Is your answer correct?")      
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Yes"):
                    # memory[st.session_state.pos][0] += 1
                    st.session_state.process_done = True
                    st.session_state.view_the_answer = False
            with col2:
                if st.button("No"):
                    st.session_state.process_done = True
                    st.session_state.view_the_answer = False
            
            if st.session_state.process_done:
                # memory[st.session_state.pos][1] += 1
                st.session_state.last_pos = st.session_state.pos
                st.rerun()
                
        # nums = len(tone_list)
        # memory = np.load("memory.npy")

        # try:  
        #     if st.session_state.process_done == True:
        #         prob = np.exp(memory[:,1] / memory[:,0] / 1.45) / np.log(memory[:,1] + 1)
        #         prob = prob / np.sum(prob)
        #         while st.session_state.pos == st.session_state.last_pos:
        #             st.session_state.pos = choice(nums,size=1,replace=True,p=prob)[0]
        #         st.session_state.show = int(uniform(0,2))
        #     # print("st.session_state.process_done",st.session_state.process_done)
        #     st.session_state.process_done = False
            
            
        #     if st.session_state.show == 0:
        #         st.text(f"what is the tone of {pron_list[st.session_state.pos % 46]}?")
        #     elif st.session_state.show == 1:
        #         st.text(f"what is the pronunciation of {tone_list[st.session_state.pos]}?")

        #     # print("st.session_state.view_the_answer",st.session_state.view_the_answer)
        #     if not st.session_state.view_the_answer:
        #         if st.button("view the answer","vta"):
        #             st.session_state.view_the_answer = True
        #             st.rerun()
            
        #     # print("st.session_state.view_the_answer",st.session_state.view_the_answer)
        #     if st.session_state.view_the_answer:
        #         if st.session_state.show == 0:
        #             st.text(f"{tone_list[st.session_state.pos % 46]} & {tone_list[st.session_state.pos % 46 + 46]}")
        #         elif st.session_state.show == 1:
        #             st.text(f"{pron_list[st.session_state.pos % 46]}")

        #         st.text("Is your answer correct?")      
        #         col1, col2 = st.columns(2)
        #         with col1:
        #             if st.button('Yes'):
        #                 memory[st.session_state.pos][0] += 1
        #                 st.session_state.process_done = True
        #                 st.session_state.view_the_answer = False
        #         with col2:
        #             if st.button('No'):
        #                 st.session_state.process_done = True
        #                 st.session_state.view_the_answer = False
                
        #         if st.session_state.process_done:
        #             memory[st.session_state.pos][1] += 1
        #             st.session_state.last_pos = st.session_state.pos
        #             st.rerun()
            
        # except KeyboardInterrupt:
        #     print("saving yout practice results")
        #     np.save("memory.npy", memory)
