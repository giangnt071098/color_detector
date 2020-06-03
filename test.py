import xlsxwriter
import numpy as np


def insert_var(var_array):
    x = np.sum((var_array-np.array([2,2,2]))**2, axis = 0)/len(var_array)
    return x

array_value=[[2,5,1],[1,2,3],[3,3,3],[5,5,5]]
print(np.sum((array_value-np.array([2,2,2]))**2, axis = 0)/len(array_value))
print((np.square(array_value - np.array([2,2,2]))).mean(axis=0))
print(np.sqrt(insert_var(array_value)))
print(np.sqrt(2))

