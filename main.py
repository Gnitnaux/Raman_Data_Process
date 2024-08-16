from RamanFunctions import read_files_from_txt
from RamanFunctions import load_data
from RamanFunctions import plot_data_comp_baseline
from RamanFunctions import plot_data_original
from RamanFunctions import plot_data_without_baseline
from RamanFunctions import SAVE, SHOW
import os  
  
def main():  
    title = '$10^{-3}\ mol/L\ NBT$ 溶液有无基底信号对比'
    directory = "E:\\Research\\新型纳米金属可穿戴柔性贴片的制备和汗液检测\\Raman_Test\\785nm\\2024-7-16" 
    SavePath = "E:\\Research\\新型纳米金属可穿戴柔性贴片的制备和汗液检测\\Raman_Test\\785nm\\2024-7-16\\有无基底型号对比.jpg" 
    data_dict = {}  
    files = read_files_from_txt("Show_Raman\\files.txt")
    labels = read_files_from_txt("Show_Raman\\labels.txt")
    column_names = ['Raman Shift', 'Raw Data'] 
    for filename in files:  
        file_path = os.path.join(directory, filename)  
        data = load_data(file_path, column_names) 
        data_dict[filename] = data  
  
    #plot_data_comp_baseline(data_dict, 'Raman Shift', 'Raw Data', labels, title, SavePath, SAVE) 
    plot_data_original(data_dict, 'Raman Shift', 'Raw Data', labels, title, SavePath, SAVE) 
    #plot_data_without_baseline(data_dict, 'Raman Shift', 'Raw Data', labels, title, SavePath, SHOW)  
  
if __name__ == '__main__':  
    main()