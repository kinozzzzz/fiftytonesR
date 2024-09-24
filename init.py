import os

from user.account_password import account_password_info
from user.account_answer_log import create_log

if __name__ == '__main__':
    if not os.path.exists('user/logs'):
        os.makedirs('user/logs')

    for account in account_password_info.keys():
        create_log(account)