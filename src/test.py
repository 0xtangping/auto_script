def get_mail(path):
    mails = set()
    with open(path) as file_object:
        for line in file_object:
            mail = line.strip().split("----")[0]
            if len(mail) > 0:
                mails.add(mail)
    return mails

# print(get_mail("./mail.txt"))

import random
from random_words import RandomWords
from random_words import RandomNicknames

rw = RandomWords()
word = rw.random_word()  + rw.random_word() + str(random.randint(0,100))
phone = str(212) + str(random.randint(1000000, 9999999))
rn = RandomNicknames()
first_name = rn.random_nick(gender='u')
print(first_name)