## import modules here 

################# Question 1 #################

import pandas as pd


def update_bag(msg, bag):
    for key, value in msg.items():
        if key not in bag.keys():
            bag[key] = msg[key]
        else:
            bag[key] += msg[key]


def dict_tool(key, dict):
    if key in dict.keys():
        return dict[key]
    else:
        return 0


def cal_prob(msg, class_bag, total_bag):
    prob = 1
    for i in msg:
        if i in total_bag.keys():
            prob = prob * (dict_tool(i, class_bag) + 1) / (sum(class_bag.values()) + len(total_bag.values()))

    return prob


def multinomial_nb(training_data, sms):  # do not change the heading of the function

    ham_bag = {}
    spam_bag = {}
    total_bag = {}
    ham_num, spam_num = 0, 0

    for i in training_data:
        if i[1] == 'ham':
            update_bag(i[0], ham_bag)
            ham_num += 1
        else:
            update_bag(i[0], spam_bag)
            spam_num += 1
        update_bag(i[0], total_bag)

    return cal_prob(sms, spam_bag, total_bag) * spam_num / cal_prob(sms, ham_bag, total_bag) / ham_num
