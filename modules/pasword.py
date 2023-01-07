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
    return "Password updated!"


class Password():

    def __init__(self,UserID):
        self.UserID = UserID
        print(pass_input(self))
    
    def verify_login(self,entered_password):
        hasher = bcrypt.using(rounds=13)
        verdict = hasher.verify(entered_password, self.password)
        return verdict


    def forgot_password(self):
        code = 'alphanumeric_string'
        send_mail(self.contact,code)
        code_entered = input(f"Enter code sent to {format_mail(self.contact)}: ")
        while code_entered != code:
            code_entered = input(f"Enter code sent to {format_mail(self.contact)}: ")
        return pass_input(self)


    def change_password(self):
        hasher = bcrypt.using(rounds=13)
        pass_entered = getpass(prompt = f"Enter password: ")
        if(hasher.verify(pass_input, self.password)):
            verdict = pass_input(self)
        else:
            verdict = "Wrong password"
        return verdict