from RamanFunctions import read_files_from_txt
from RamanFunctions import load_data
import pandas as pd  
import matplotlib.pyplot as plt  
import numpy as np  
from matplotlib.ticker import MultipleLocator  
from matplotlib import rcParams  
import math
from scipy.sparse import spdiags
from scipy.linalg import cholesky
from scipy.linalg import inv
import os  


def airPLS(X_df, lam, order, wep=0.5, p=0.05, itermax=20):  
    X = X_df.iloc[:, 1].values
    X = X.T  
    n = X.shape[0]
    Z = np.empty(n)  
    D = np.diff(np.eye(n), order, axis=0) 
    DD = np.matmul(lam * D.T, D) 
      
    w = np.ones(n).T  
    x = X
    for j in range(1, itermax + 1):  
            W = spdiags(w, 0, n, n)  
            C = cholesky(W + DD)  
            z = np.matmul(inv(C), np.matmul(inv(C.T), (w * x).T)).T  
            d = x - z  
            dssn = np.abs(sum(d[d < 0]))  
            if dssn < 0.001 * sum(np.abs(x)):  
                break  
            w[d >= 0] = 0  
            w[:math.ceil(n * wep)] = p 
            w[n - math.floor(n * wep) - 1:] = p  
            to_exp = np.abs(d[d < 0]) / dssn  
            w[d < 0] = j * np.exp(to_exp)  
    Z = z  
    X = X-Z  
    X = X.T
    Xc_df = X_df.copy()  
    Xc_df.iloc[:, 1] = X  
    return Xc_df

def plot_data_without_baseline(data_dict, x_column, y_column, labels, title, SavePath, files, directory, column_names):  
    colors = plt.cm.viridis(np.linspace(0, 1, 7))  
    for filename in files:  
        file_path = os.path.join(directory, filename)  
        data = load_data(file_path, column_names) 
        data_dict[filename] = data  
    for i, (filename, data) in enumerate(data_dict.items()):
            plt.plot(data[x_column], data[y_column], linestyle='-', linewidth=1, color=colors[5], label='原始谱线') 
            data = airPLS(data, 10000, 2)
            plt.plot(data[x_column], data[y_column], linestyle='-', linewidth=1, color=colors[0], label='$\lambda=10000$')  
    for filename in files:  
        file_path = os.path.join(directory, filename)  
        data = load_data(file_path, column_names) 
        data_dict[filename] = data  
    for i, (filename, data) in enumerate(data_dict.items()):
            data = airPLS(data, 100000, 2)
            plt.plot(data[x_column], data[y_column], linestyle='-', linewidth=1, color=colors[1], label='$\lambda=100000$')  
    for filename in files:  
        file_path = os.path.join(directory, filename)  
        data = load_data(file_path, column_names) 
        data_dict[filename] = data  
    for i, (filename, data) in enumerate(data_dict.items()):
            data = airPLS(data, 1000000, 2)
            plt.plot(data[x_column], data[y_column], linestyle='-', linewidth=1, color=colors[2], label='$\lambda=1000000$')  
    for filename in files:  
        file_path = os.path.join(directory, filename)  
        data = load_data(file_path, column_names) 
        data_dict[filename] = data  
    for i, (filename, data) in enumerate(data_dict.items()):
            data = airPLS(data, 10000000, 2)
            plt.plot(data[x_column], data[y_column], linestyle='-', linewidth=1, color=colors[3], label='$\lambda=10000000$') 
    for i, (filename, data) in enumerate(data_dict.items()):
            data = airPLS(data, 100000000, 2)
            plt.plot(data[x_column], data[y_column], linestyle='-', linewidth=1, color=colors[4], label='$\lambda=100000000$') 
    for i, (filename, data) in enumerate(data_dict.items()):
            data = airPLS(data, 1000000000, 2)
            plt.plot(data[x_column], data[y_column], linestyle='-', linewidth=1, color=colors[6], label='$\lambda=1000000000$')     
    plt.title(title)  
    plt.xlabel(r'$Raman Shift (cm^{-1})$')  
    plt.ylabel(r'$Intensity$')  
    plt.grid(True)  
    plt.xticks(rotation=45)  
    plt.legend()  
    plt.tight_layout()  
    plt.show()
    #plt.savefig(SavePath, dpi = 1000)
  
def main():  
    title = '不同平滑度下去基线效果对比 ($10^{-7}\ mol/L\ NBT$)'
    directory = "E:\\Research\\新型纳米金属可穿戴柔性贴片的制备和汗液检测\\Raman_Test\\785nm\\2024-7-21"  
    SavePath = "E:\\Research\\新型纳米金属可穿戴柔性贴片的制备和汗液检测\\Raman_Test\\785nm\\2024-7-21\\不同平滑度下去基线效果对比.jpg" 
    data_dict = {}  
    files = read_files_from_txt("Show_Raman\\files.txt")
    labels = read_files_from_txt("Show_Raman\\labels.txt")
    column_names = ['Raman Shift', 'Raw Data'] 
  
    plot_data_without_baseline(data_dict, 'Raman Shift', 'Raw Data', labels, title, SavePath, files, directory, column_names)  
  
if __name__ == '__main__':  
    main()