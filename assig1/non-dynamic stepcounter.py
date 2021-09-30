import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#Simple function to visualize 4 arrays that are given to it
def visualize_data(timestamps, x_arr,y_arr,z_arr,s_arr,m_arr):

  #Plotting accelerometer readings  
  plt.figure(1)
  plt.plot(timestamps, x_arr, color = "yellow",linewidth=1.0)
  plt.plot(timestamps, y_arr, color = "red",linewidth=1.0)
  plt.plot(timestamps, z_arr, color = "green",linewidth=1.0)
  plt.plot(timestamps, s_arr, color = "black",linewidth=1.0)
  plt.plot(timestamps, m_arr, color = "blue",linewidth=1.0)
  plt.show()
  #magnitude array calculation
  m_arr = []
  for i, x in enumerate(x_arr):
    m_arr.append(magnitude(x_arr[i],y_arr[i],z_arr[i]))
  plt.figure(2)
  #plotting magnitude and steps
  plt.plot(timestamps, s_arr, color = "black",linewidth=1.0)
  plt.plot(timestamps, m_arr, color = "red",linewidth=1.0)
  plt.show()

#Function to read the data from the log file
#TODO Read the measurements into array variables and return them
def read_data(filename):

  columns = ["timestamps", "x_array", "y_array", "z_array"]
  #columns = [0, 1, 2, 3]
  data = pd.read_table(filename,",", usecols=columns)
  print(data)
  
  return data.timestamps.tolist(), data.x_array.tolist(), data.y_array.tolist(), data.z_array.tolist()

#Function to count steps.
#Should return an array of timestamps from when steps were detected
#Each value in this arrray should represent the time that step was made.
def count_steps(timestamps, x_arr, y_arr, z_arr, m_arr):
  rv = []
  last = m_arr[0]
  treshold = 10
  for i, time in enumerate(timestamps):
    m_arr[i]
    if(m_arr[i] <= treshold and last >= treshold):
      rv.append(time)
    last = m_arr[i]
  return rv

#Calculate the magnitude of the given vector
def magnitude(x,y,z):
  return np.linalg.norm((x,y,z))

#Function to convert array of times where steps happened into array to give into graph visualization
#Takes timestamp-array and array of times that step was detected as an input
#Returns an array where each entry is either zero if corresponding timestamp has no step detected or 50000 if the step was detected
def generate_step_array(timestamps, step_time):
  s_arr = []
  ctr = 0
  for i, time in enumerate(timestamps):
    if(ctr<len(step_time) and step_time[ctr]<=time):
      ctr += 1
      s_arr.append( 10 )
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

def main():
  #read data from a measurement file, change the inoput file name if needed
  timestamps, x_array, y_array, z_array = read_data("accelerometer_data.csv")
  #Chek that the data does not produce errors
  if(not check_data(timestamps, x_array,y_array,z_array)):
    return
  
  m_array = []
  for i in range(len(timestamps)):
    m_array.append(magnitude(x_array[i],y_array[i],z_array[i]))
  
  #Count the steps based on array of measurements from accelerometer
  st = count_steps(timestamps, x_array, y_array, z_array, m_array)
  #Print the result
  print("This data contains "+str(len(st))+" steps according to current algorithm")
  #convert array of step times into graph-compatible format
  s_array = generate_step_array(timestamps, st)
  #visualize data and steps
  visualize_data(timestamps, x_array,y_array,z_array,s_array,m_array)

main()

