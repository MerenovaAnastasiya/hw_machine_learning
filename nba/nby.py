import pandas
import numpy as np


def read_file(file):
    return pandas.read_csv(file, delimiter=';', sep='\t')


symptoms = read_file('symptom.csv')
diseases = read_file('disease.csv')

diseases_probabilities = []
diseases_num = diseases['кол-во пациентов'].values
patient_count = diseases_num[-1]
for i in diseases_num[:-1]:
    diseases_probabilities.append(i / patient_count)

r_symptoms = [np.random.randint(0, 2) for i in range(len(symptoms) - 1)]
r_probabilities = [1] * (len(diseases['Болезнь']) - 1)

for i in range(len(diseases['Болезнь']) - 1):
    r_probabilities[i] *= diseases_probabilities[i]
    for j in range(len(symptoms) - 1):
        if r_symptoms[j] == 1:
            r_probabilities[i] *= float(symptoms.iloc[j][i + 1].replace(',', '.'))

max = 0
maxI = -1
for i in range(len(r_probabilities)):
    if r_probabilities[i] > max:
        max = r_probabilities[i]
        maxI = i

print('С большей вероятностью у Вас ' + diseases['Болезнь'].values[maxI])