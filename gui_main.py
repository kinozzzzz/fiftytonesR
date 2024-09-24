import numpy as np
import streamlit as st
import time

from const import KANA, IVCODE
from user.account_password import account_password_info


def init_settings():
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
    if 'action_time' not in st.session_state:
        st.session_state.action_time = time.time()

if __name__ == '__main__':
    init_settings()

    st.markdown('# 五十音记忆')

    if 'account_name' in st.session_state and time.time() - st.session_state.action_time > 60:
        np.save(f"user/logs/{st.session_state.account_name}.npy",st.session_state.account_answer_info)
        st.session_state.action_time = time.time()

    if not st.session_state.login:
        if not st.session_state.register:
            username = st.text_input("用户名")
            password = st.text_input("密码", type="password")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("登录"):
                    if username in account_password_info.keys() and password == account_password_info[username]:
                        st.session_state.login = True
                        st.session_state.account_name = username
                        st.session_state.account_answer_info = np.load(f"user/logs/{username}.npy")
                        st.rerun()
                    else:
                        st.error("用户名或密码错误！")   
            with col2:
                if st.button("注册"):
                    # do nothing
                    pass
        t = '''
                    # st.session_state.register = True
                    # st.rerun()
        # 注册界面
        else:
            username = st.text_input("用户名", key="regs_account")
            password = st.text_input("密码", type="password", key="regs_pw")
            invite_code = st.text_input("邀请码")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("返回登录"):
                    st.session_state.register = False
                    st.rerun()                      
            with col2:
                if st.button("注册"):
                    pass
                    # if invite_code != IVCODE:
                    #     st.error("邀请码错误！")
                    # elif username in users:
                    #     st.error("用户名已存在！")
                    # elif not re.search(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", password):
                    #     st.error("密码应不少于8位, 且同时包含英文字母和数字")
                    # else:
                    #     user_info = {"username": username, 
                    #                  "password": password}
                    #     try:
                    #         with open(os.path.join(user_dir, f"{username}.json"), "w") as file:
                    #             json.dump(user_info, file, indent=4)
                    #         st.success("注册成功")
                    #     except Exception as e:
                    #         st.error(e)
                    #         st.error("用户名不符合规范！")
        '''
    elif st.session_state.login:
        nums = len(KANA)
        
        if st.session_state.process_done == True:
            answer = st.session_state.account_answer_info
            prob = np.exp(answer[:,1] / answer[:,0] / 1.45) / np.log(answer[:,1] + 1)
            prob = prob / np.sum(prob)
            while st.session_state.pos == st.session_state.last_pos:
                st.session_state.pos = np.random.choice(nums,size=1,replace=True,p=prob)[0]
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
                    st.session_state.account_answer_info[st.session_state.pos][0] += 1
                    st.session_state.process_done = True
                    st.session_state.view_the_answer = False
            with col2:
                if st.button("No"):
                    st.session_state.process_done = True
                    st.session_state.view_the_answer = False
            
            if st.session_state.process_done:
                st.session_state.account_answer_info[st.session_state.pos][1] += 1
                st.session_state.last_pos = st.session_state.pos
                st.rerun()
