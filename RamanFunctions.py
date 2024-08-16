import pandas as pd  
import matplotlib.pyplot as plt  
import numpy as np  
from matplotlib.ticker import MultipleLocator  
from matplotlib import rcParams  
import math
from scipy.sparse import spdiags
from scipy.linalg import cholesky
from scipy.linalg import inv

SAVE = 1
SHOW = 0

MyColors = [ (155/256, 46/256, 43/256), (69/256, 156/256, 215/256), (226/256, 83/256, 61/256), (49/256, 92/256, 181/256), (249/256, 228/256, 169/256),
        (178/256, 223/256, 227/256)]
  
# 设置matplotlib参数以显示中文  
rcParams['font.sans-serif'] = ['kaiti']  # 指定默认字体为楷体  
rcParams['axes.unicode_minus'] = False  # 用来正常显示负号 

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


def read_files_from_txt(filename):  
    files = []  
    with open(filename, 'r') as f:  
        for line in f:  
            # 去除行尾的换行符并添加到列表中  
            files.append(line.strip())  
    return files  

  
def load_data(filename, column_names):  
    data = pd.read_csv(filename, sep = ';', header=0, names=column_names)
    return data  
  

def plot_data_comp_baseline(data_dict, x_column, y_column, labels, title, SavePath, option):  
    #colors = plt.cm.viridis(np.linspace(0, 1, len(data_dict)*2))  
    for i, (filename, data) in enumerate(data_dict.items()): 
            data = processTimes(data, i) 
            plt.plot(data[x_column], data[y_column], linestyle='-', linewidth=1, color=MyColors[i%6], label=labels[i])  
            data = airPLS(data, 100000, 2)
            plt.plot(data[x_column], data[y_column], linestyle='-', linewidth=1, color=MyColors[(i+len(data_dict))%6], label=labels[i+len(data_dict)])  
    plt.title(title)  
    plt.xlabel(r'$Raman Shift (cm^{-1})$')  
    plt.ylabel(r'$Intensity$')  
    plt.grid(True)  
    plt.xticks(rotation=45)  
    plt.legend()  
    plt.tight_layout()  
    if option == 0:
         plt.show()
    else:
         plt.savefig(SavePath, dpi = 1000)


def plot_data_original(data_dict, x_column, y_column, labels, title, SavePath, option):  
    colors = plt.cm.viridis(np.linspace(0, 1, len(data_dict)))  
    for i, (filename, data) in enumerate(data_dict.items()): 
            data = processTimes(data, i) 
            plt.plot(data[x_column], data[y_column], linestyle='-', linewidth=1, color=MyColors[i%6], label=labels[i])  
            #plt.plot(data[x_column], data[y_column], linestyle='-', linewidth=1, color=colors[i], label=labels[i])  
    plt.title(title)  
    plt.xlabel(r'$Raman Shift (cm^{-1})$')  
    plt.ylabel(r'$Intensity$')  
    plt.grid(True)  
    plt.xticks(rotation=45)  
    plt.legend()  
    plt.tight_layout()  
    if option == 0:
         plt.show()
    else:
         plt.savefig(SavePath, dpi = 1000)


def plot_data_without_baseline(data_dict, x_column, y_column, labels, title, SavePath, option):  
    #colors = plt.cm.viridis(np.linspace(0, 1, len(data_dict)))  
    for i, (filename, data) in enumerate(data_dict.items()):
            data = processTimes(data, i)
            data = airPLS(data, 100000, 2)
            plt.plot(data[x_column], data[y_column], linestyle='-', linewidth=1, color=MyColors[i%6], label=labels[i])  
    plt.title(title)  
    plt.xlabel(r'$Raman Shift (cm^{-1})$')  
    plt.ylabel(r'$Intensity$')  
    plt.grid(True)  
    plt.xticks(rotation=45)  
    plt.legend()  
    plt.tight_layout()  
    if option == 0:
         plt.show()
    else:
         plt.savefig(SavePath, dpi = 1000)

def processTimes(data, i):
     times = np.loadtxt("Show_Raman\\times.txt")
     data['Raw Data'] = data['Raw Data'] * times[i]
     return data