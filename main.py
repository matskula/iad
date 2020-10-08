import sys

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from data_parser import preprocess_data

df = pd.read_csv('data/DATABASE (2).csv', sep=';')
preprocess_data(df)


def plot_bar(single_column: pd.Series):
    single_column.value_counts().plot(kind='bar')


def plot_hist(single_column: pd.Series):
    single_column.plot.hist()


def plot_box(single_column: pd.Series):
    single_column.plot.box()


one_column_c_graphs = {
    'bar': plot_bar,
}

one_column_n_graphs = {
    'boxplot': plot_box,
    'hist': plot_hist,
}


def plot_nc_boxplot(dataframe: pd.DataFrame, col1: str, col2: str):
    dataframe.boxplot(column=col1, by=col2)


two_columns_nc_graphs = {
    'boxplot': plot_nc_boxplot,
}


def plot_scatter(dataframe: pd.DataFrame, col1: str, col2: str):
    dataframe.plot.scatter(x=col1, y=col2)


def plot_line(dataframe: pd.DataFrame, col1: str, col2: str):
    dataframe.plot.line(x=col1, y=col2)


two_columns_nn_graphs = {
    'scatter': plot_scatter,  # n, n
    'line': plot_line,  # n, n
}


def determine_datatype(single_column: pd.Series):  # TODO rework
    if isinstance(single_column[0], str) or isinstance(single_column[0], bool):
        return 'c'
    if isinstance(single_column[0], int) or\
            isinstance(single_column[0], float) or\
            isinstance(single_column[0], np.int64):
        return 'n'
    print(type(single_column[0]), file=sys.stderr)


print(f"Available columns: {', '.join(df.columns)}")
print("Input 1 or 2 needed columns 1 or 2, press enter after each or to skip 2 column")
columns = [input(), input()]
if not columns[-1]:
    columns.pop()
for column in columns:
    if column not in df.columns:
        print(f"Column {column} not found in dataset!", file=sys.stderr)
        sys.exit()

if len(columns) == 2:
    column1 = df[columns[0]]
    column2 = df[columns[1]]
    datatype1 = determine_datatype(column1)
    datatype2 = determine_datatype(column2)
    if datatype1 == 'n' and datatype2 == 'n':
        available_graphs = two_columns_nn_graphs
    elif datatype1 == 'n' and datatype2 == 'c':
        available_graphs = two_columns_nc_graphs
    elif datatype1 == 'c' and datatype2 == 'n':
        columns[0], columns[1] = columns[1], columns[0]
        column1 = df[columns[0]]
        column2 = df[columns[1]]
        datatype1 = determine_datatype(column1)
        datatype2 = determine_datatype(column2)
        available_graphs = two_columns_nc_graphs
    else:
        print(f"Unsupported datatype combination '{datatype1}' and '{datatype2}'", file=sys.stderr)
        sys.exit()
    print(
        f"Available graphs: {', '.join(available_graphs.keys())}"
    )
    graphs = input('Enter graph names separated by whitespace: ').split()
    for graph in graphs:
        if graph not in list(available_graphs.keys()):
            print(f"Graph {graph} is not allowed here!", file=sys.stderr)
            sys.exit()
    for i, graph in enumerate(graphs):
        plt.subplot(int(f"1{len(graphs)}{i+1}"))
        plt.title(f"{columns[0]} and {columns[1]} {graph}")
        available_graphs[graph](df, columns[0], columns[1])
        plt.savefig("output.png")

else:
    column = df[columns[0]]
    datatype = determine_datatype(column)
    if datatype == 'c':
        available_graphs = one_column_c_graphs
    elif datatype == 'n':
        available_graphs = one_column_n_graphs
    else:
        print(f"Unsupported datatype '{datatype}'", file=sys.stderr)
        sys.exit()
    print(
        f"Available graphs: {', '.join(available_graphs.keys())}"
    )
    graphs = input('Enter graph names separated by whitespace: ').split()
    for graph in graphs:
        if graph not in list(available_graphs.keys()):
            print(f"Graph {graph} is not allowed here!", file=sys.stderr)
            exit()
    for i, graph in enumerate(graphs):
        plt.subplot(int(f"1{len(graphs)}{i+1}"))
        plt.title(f"{columns[0]} {graph}")
        available_graphs[graph](column)
        plt.savefig("output.png")

print('Graphs was plotted successfully!')
