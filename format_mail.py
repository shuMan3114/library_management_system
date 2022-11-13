def format_mail(email):
    parsedEmail = email.split('@')
    usernameList = list(parsedEmail[0])
    if(len(usernameList)>4):
        for i in range(4,len(parsedEmail[0])):
            usernameList[i] = 'X'
    usernameList = "".join(usernameList)
    return usernameList + "@" +parsedEmail[1]



    