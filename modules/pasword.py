from passlib.hash import bcrypt
import getpass
from mailing import send_mail,format_mail

def pass_input(obj):
    new_password = getpass.getpass(prompt="Enter new password: ")
    re_entered_pass = getpass.getpass(prompt="Re-enter new password: ")
    while new_password != re_entered_pass:
        re_entered_pass = getpass.getpass(prompt="Incorrect! Passwords do not match! Re-enter: ")
    hasher = bcrypt.using(rounds=13)
    new_pass = hasher.hash(new_password)
    obj.password = new_pass


class Password():
    prompts = {
        
    }

    def __init__(self):
        pass