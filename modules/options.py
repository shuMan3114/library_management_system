import getpass
from passlib.hash import bcrypt


def pass_input():
    new_password = getpass.getpass(prompt="Enter new password: ")
    re_entered_pass = getpass.getpass(prompt="Re-enter new password: ")
    while new_password != re_entered_pass:
        re_entered_pass = getpass.getpass(prompt="Incorrect! Passwords do not match! Re-enter: ")
    hasher = bcrypt.using(rounds=13)
    new_pass = hasher.hash(new_password)
    return new_pass


def optionValidator(prompt,escape_pormpt="Return",error_prompt="Wrong Option",lower_limit=None,higher_limit=None,check_value=None):
    if(lower_limit == None):
        menu_choice = -1
    else:
        menu_choice = lower_limit - 1
    new_prompt = prompt + f'Enter {menu_choice} to {escape_pormpt}'   
    if(lower_limit != None):
        option_selected = input(new_prompt)
        while option_selected not in [str(x) for x in range(lower_limit -1 , higher_limit + 1)]:
            print(error_prompt)
            option_selected = input(new_prompt)
        return int(option_selected)
    else:
        option_selected = input(new_prompt)
        while option_selected != str(check_value) or option_selected != str(menu_choice):
            print(error_prompt)
            option_selected = input(new_prompt)
        return option_selected


def ID_generation(seed):
    num = int(seed[5:])
    num += 1
    padding = len(str(num))%4
    if(padding):
        num = "".join((4-padding)*['0']) + str(num)
    else:
        num = str(num)
    return seed[:5] + num
