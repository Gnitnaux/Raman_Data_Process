# Introdution
- The code is used to process data of Raman Spectroscopy and visualize them
- Author : Xuanting Liu, School of Biomedical Engineering, Shanghai Jiao Tong University

# Way To Use
- To visualize your data, you first need to put the location of your Raman data folder in `directory`  and the location you want to save the data after processing in `SavePath`, also other names according to the variable names 
  
- Then put the file names in files.txt
  
- Then put the labels of each file in labels.txt accordingly, if you want to use `plot_data_comp_baseline` (which will be introduced later), then you should the labels of data after calculating at the end of the labels of original data, which means the number of labels will be twice of the number of files
  
- In consideration of the influence of integration time when using the instrument, please write the multiple of the spectral data corresponding to each file in the times.txt file

- In main.py, there are three funtion:
  
   * `plot_data_comp_baseline` you can use this funtion to get the Raman spectrum of both original data and data without baseline
   * `plot_data_original` you can use this funtion to get the Raman spectrum of original data
   * `plot_data_without_baseline` you can use this funtion to get the Raman spectrum of data without baseline
  
  Remember three of the funtion all have two functions. If you just want the programme to show the Raman spectrum, then set the last parameter of the funtion "SHOW". If you want to save the picture, then set it "SAVE"