import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def read_file(file_name):
    return pd.read_csv(file_name)


def get_sorted_labels(data, column_name):
    return sorted(data[column_name].unique())


def add_data(labels, dictionary, sex):
    for label in labels:
        for line in data.itertuples():
            if line.Sex == sex and line.Pclass == label and line.Survived:
                if dictionary.get(label) is None:
                    dictionary[label] = 1
                else:
                    dictionary[label] = dictionary[label] + 1


def draw_bar(labels, first_group, second_group, title, y_label,
             first_group_label, second_group_label,
             first_group_color, second_group_color):
    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots()
    ax.bar(x - width / 2, first_group, width, label=first_group_label, color=first_group_color)
    ax.bar(x + width / 2, second_group, width, label=second_group_label, color=second_group_color)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    fig.tight_layout()
    plt.show()


data = read_file('titanic.csv')
labels = get_sorted_labels(data, 'Pclass')
print(labels)
men_means_by_class = {}
women_means_by_class = {}
add_data(labels, men_means_by_class, 'male')
add_data(labels, women_means_by_class, 'female')
draw_bar(labels, men_means_by_class.values(), women_means_by_class.values(),
         'Survivors by class and gender', 'Number of survivors', 'Men', 'Women',
         'grey', 'pink')




