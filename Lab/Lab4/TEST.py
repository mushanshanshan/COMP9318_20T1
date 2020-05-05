## import modules here
from collections import Counter
import pandas as pd

################# Question 1 #################
def multinomial_nb(training_data, sms):# do not change the heading of the function
    vocabulary, conditional_prob, prior_prob = train(training_data)
    print(vocabulary)
    print(conditional_prob)
    print(prior_prob)
    result = predict(sms, vocabulary, conditional_prob,prior_prob)
    return result

def train(training_data):
    smooth = 1
    vocabulary = set()
    data_value = {'spam':0,'ham':0}
    data_set= {'spam':[],'ham':[]}
    prior_prob = {'spam':0,'ham':0}
    conditional_prob = dict()


    for data in training_data:
        prior_prob[data[1]] += 1
        data_value[data[1]] += sum(data[0].values())
        for i in data[0].items():
            data_set[data[1]].append(i)
            vocabulary.add(i[0])
    # print(len(vocabulary))
    prior_prob['spam'] /=  len(training_data)
    prior_prob['ham'] /= len(training_data)
    # print(prior_prob)
    # print(data_value)
    # print(data_set)


    for data in training_data:
        for i in data[0]:
            for j in ('spam', 'ham'):
                conditional_prob[(i, j)] = (sum([x[1] for x in data_set[j] if x[0] == i]) + smooth )/ ((data_value[j] + len(vocabulary)))
    # print(conditional_prob)
    return vocabulary, conditional_prob, prior_prob


def predict(sms ,vocabulary, conditional_prob, prior_prob):
    result ={'spam': prior_prob['spam'], 'ham': prior_prob['ham']}
    for token in sms:
        if token in vocabulary:
            for i in ['spam', 'ham']:
                # print((token,i),':' ,conditional_prob[(token,i)])
                result[i] *= conditional_prob[(token, i)]
    # print(result['spam'])
    # print(result['ham'])
    return result['spam']/ result['ham']

raw_data = pd.read_csv('./asset/data.txt', sep='\t')
raw_data.head()


def tokenize(sms):
    return sms.split(' ')

def get_freq_of_tokens(sms):
    tokens = {}
    for token in tokenize(sms):
        if token not in tokens:
            tokens[token] = 1
        else:
            tokens[token] += 1
    return tokens

training_data = []
for index in range(len(raw_data)):
    training_data.append((get_freq_of_tokens(raw_data.iloc[index].text), raw_data.iloc[index].category))


sms = 'I am not spam'

print(multinomial_nb(training_data, tokenize(sms)))