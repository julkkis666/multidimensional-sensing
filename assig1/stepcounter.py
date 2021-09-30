import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import statistics

#Simple function to visualize 4 arrays that are given to it
def visualize_data(timestamps, x_arr,y_arr,z_arr,s_arr,m_arr):

  #Plotting accelerometer readings  
  plt.figure(1)
  plt.plot(timestamps, s_arr, color = "black",linewidth=1.0)
  plt.plot(timestamps, m_arr, color = "blue",linewidth=1.0)
  plt.show()

#Function to read the data from the log file
def read_data(filename):

  columns = ["timestamps", "x_array", "y_array", "z_array"]
  data = pd.read_table(filename,",", usecols=columns)
  
  return data.timestamps.tolist(), data.x_array.tolist(), data.y_array.tolist(), data.z_array.tolist()

#Function to count steps.
#Should return an array of timestamps from when steps were detected
#Each value in this arrray should represent the time that step was made.
def count_steps(timestamps, x_arr, y_arr, z_arr, m_arr):
  rv = []
  th = []
  last = m_arr[0]

  #handle dynamic array
  treshold = 0
  d_size = 5
  d_arr = []
  isLow = True
  for i in range(d_size):
    d_arr.append(treshold)
  non_dynamic_ans = 0

  
  for i, time in enumerate(timestamps):
    
    di = i % d_size#dynamic index
    d_arr[di] = m_arr[i]
    old_treshold = treshold
    threshold = ((max(d_arr) + min(d_arr)) / 2)

    #NonDynamic 
    if(m_arr[i] >= 10 and last <= 10):
      non_dynamic_ans = non_dynamic_ans+1
    #m_arr[i]
    #print(m_arr[i], treshold)
    #print((max(d_arr) + min(d_arr)) / 2)
    if(m_arr[i] > threshold and isLow):
      isLow = False
      rv.append(time-1)
      th.append(threshold)
    elif(m_arr[i] < threshold and (isLow == False)):
      isLow = True
    last = m_arr[i]
  print("Static Algorithm gives:",non_dynamic_ans)
  return rv, th

#Calculate the magnitude of the given vector
def magnitude(x,y,z):
  return np.linalg.norm((x,y,z))

#Function to convert array of times where steps happened into array to give into graph visualization
#Takes timestamp-array and array of times that step was detected as an input
#Returns an array where each entry is either zero if corresponding timestamp has no step detected or 50000 if the step was detected
def generate_step_array(timestamps, step_time, treshold):
  s_arr = []
  ctr = 0
  for i, time in enumerate(timestamps):
    if(ctr<len(step_time) and step_time[ctr]<=time):
      s_arr.append( treshold[ctr] )
      ctr += 1
    else:
      s_arr.append( 0 )
  while(len(s_arr)<len(timestamps)):
    s_arr.append(0)
  return s_arr

#Check that the sizes of arrays match
def check_data(t,x,y,z):
  if( len(t)!=len(x) or len(y)!=len(z) or len(x)!=len(y) ):
    print("Arrays of incorrect length")
    return False
  print("The amount of data read from accelerometer is "+str(len(t))+" entries")
  return True

def magnitudeArray(timestamps, x_array, y_array, z_array):
  m_array = []
  for i in range(len(timestamps)):
    m_array.append(magnitude(x_array[i],y_array[i],z_array[i]))
  return m_array

def main():
  #read data from a measurement file, change the inoput file name if needed
  datafile1 = "out_29steps.csv"
  datafile2 = "out_sabsa_manysteps.csv"
  datafile3 = "out_sabsa_diffusasteps.csv"
  datafile4 = "out_sabsa_inpantssteps.csv"
  datafile5 = "out_sabsa_29steps.csv"

  datafiles = [datafile1, datafile2, datafile3, datafile4, datafile5]

  for datafile in datafiles:
    timestamps, x_array, y_array, z_array = read_data(datafile)
    #Chek that the data does not produce errors
    if(not check_data(timestamps, x_array,y_array,z_array) and check_data(timestamps, x_array,y_array,z_array)):
      return

    #get magnitude arrays
    m_array = magnitudeArray(timestamps, x_array, y_array, z_array)
    
    #Count the steps based on array of measurements from accelerometer
    st, th = count_steps(timestamps, x_array, y_array, z_array, m_array)
    #Print the result
    print(datafile,"contains "+str(len(st)),"steps according to current algorithm\n")
    #convert array of step times into graph-compatible format
    s_array = generate_step_array(timestamps, st, th)
    #visualize data and steps
    visualize_data(timestamps, x_array, y_array, z_array, s_array, m_array)

main()

