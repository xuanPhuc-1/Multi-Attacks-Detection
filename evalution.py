import os
import time
from detection import Entropy
import numpy as numpy
import datetime
import sys

diction = {}
timerSet =False
#port = sys.argv[1]

# Gan doi tuong cho class Entropy da dinh nghia tu file detectionUsingEntropy.py

aveEntropy = []	######
set_Timer = False     
defendDDOS=False      
temp = []	######
stanDeviation = []	######
thresList = []		######

while(1):
  ent_obj = Entropy()
  resp_obj = Entropy()	#####
  ent_obj.start() #.#
  resp_obj.start() #.#

  # Neu cac list co >= 10 phan tu thi xoa het phan tu, tro lai list rong
  if len(thresList) == 15:	######
      del aveEntropy[:]	######
      del temp[:]	######
      del stanDeviation[:]	######

      # Reset entropy = 1.0
      ent_obj.value = 1.0	######
      del thresList[:]	######

      
  # Them gia tri entropy vao list aveEntropy
  if ent_obj.value not in aveEntropy:	######
      aveEntropy.append(ent_obj.value)	######


  # Tinh gia tri trung binh cua cac gia tri entropy co trong list
  ave = numpy.mean(aveEntropy)	######


  # Tinh do lech chuan
  if ent_obj.value not in temp:	######
      temp.append(ent_obj.value)	######
      stanDeviation.append(pow(ent_obj.value - ave, 2))	######

  std = numpy.mean(stanDeviation)	######

  # Tinh entropy dong theo cong thuc
  dynamicThres = ave - 2*std	######

  print ("Entropy: ", str(ent_obj.value))
  print ("Average Entropy: ", ave)	######
  print ("Standard Deviation: ", std)	######
  print ("Dynamic Threshold: ", dynamicThres)	###### 

  if dynamicThres not in thresList:	######
      thresList.append(dynamicThres)	######

  # # So sanh neu gia tri entropy tuc thoi < nguong entropy dong
  if ent_obj.value < dynamicThres:	######
      # preventing()
      
    with open('result.txt', 'w') as f:
                f.write("1")
  else :
    with open('result.txt', 'w') as f:
                f.write("0")
                
  time.sleep(5)