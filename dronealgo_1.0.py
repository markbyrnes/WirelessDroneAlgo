import numpy as np
import time


#complete - generates x by y 1 and 0 matrix, 1 = obstacles
def generate(rows, cols, prob = .15):
  matrix = np.random.choice([0, 1], size=(rows,cols), p=[(1-prob), prob])

  return matrix


#complete - turns the inputed 1 and 0 matrix into movement matrix
def obstomove(arr):
  rows = len(arr)
  cols = len(arr[0])
  rows = rows + 2
  cols = cols + 2
  matrix = np.zeros((rows, cols))
  for i in range(rows-1):
    for j in range(cols-1):
      if arr[i-1][j-1] == 1:
        matrix[i][j] = 8
      if (i == 0) or (j == 0):
        matrix[i][j] = 8
  for i in range(rows-1):
   matrix[i][cols-1] = 8
  for j in range(cols-1):
   matrix[rows-1][j] = 8
  matrix[rows-1][cols-1] = 8


  for i in range(1, rows-1, 1):
    for j in range(1, cols-1, 1):
      if matrix[i][j] != 8:
        counter = 0
        if matrix[i-1][j-1] == 8:
          counter = counter +1

        if matrix[i][j-1] == 8:
          counter = counter +1

        if matrix[i+1][j-1] == 8:
          counter = counter +1
      
        if matrix[i-1][j] == 8:
          counter = counter +1
        
        if matrix[i+1][j] == 8:
          counter = counter +1

        if matrix[i-1][j+1] == 8:
          counter = counter +1

        if matrix[i][j+1] == 8:
          counter = counter +1
        
        if matrix[i+1][j+1] == 8:
          counter = counter +1

        matrix[i][j] = counter
    
  return matrix


#complete - simulates the drone moving
def movedrone(matrix, sposx, sposy, prob):
  rows = len(matrix)
  cols = len(matrix[0])
  cposx = sposx + 1
  cposy = sposy + 1
  #check spawn for an obstacle
  while matrix[cposy][cposx] == 8:
    #print("Starting area an obstacle, regenerating")
    matrix = generate(rows-2,cols-2,prob)
    matrix = obstomove(matrix)
  matrix[cposy][cposx] = 8;
  movecounter = 0

  while (matrix[cposy+1][cposx]+matrix[cposy-1][cposx]+matrix[cposy][cposx+1]+matrix[cposy][cposx-1] == 32): #spawn surrounded
    #print("Starting area surrounded, regenerating")
    matrix = generate(rows-2, cols-2, prob)
    matrix = obstomove(matrix)

   #find a valid default bestmove
  if matrix[cposy][cposx+1] != 8:
    bestmovex = 1
    bestmovey = 0
  elif matrix[cposy][cposx-1] != 8:
    bestmovex = -1
    bestmovey = 0
  elif matrix[cposy+1][cposx] != 8:
    bestmovex = 0
    bestmovey = 1
  elif matrix[cposy-1][cposx] != 8:
    bestmovex = 0
    bestmovey = -1

  
  stackbestmovex = [bestmovex]
  stackbestmovey = [bestmovey]

  x = 1
  while x == 1:
    #check if matrix is fully travelled
    if (np.sum(matrix) == 8*rows*cols):
      break
    #test if started in blocked off area
    if not stackbestmovex:
      #print("Starting area blocked off, regenerating")
      movecounter = 0
      cposx = sposx + 1
      cposy = sposy + 1
      matrix = generate(rows-2,cols-2, prob)
      matrix = obstomove(matrix)  
      while (matrix[cposy+1][cposx]+matrix[cposy-1][cposx]+matrix[cposy][cposx+1]+matrix[cposy][cposx-1] == 32) or (matrix[cposy][cposx] == 8):
        matrix = generate(rows-2,cols-2, prob)
        matrix = obstomove(matrix)     
      
    
    #backtrack
    if (matrix[cposy+1][cposx]+matrix[cposy-1][cposx]+matrix[cposy][cposx+1]+matrix[cposy][cposx-1] == 32):
      cposx = cposx - stackbestmovex.pop()
      cposy = cposy - stackbestmovey.pop()
      movecounter = movecounter+1

    else:
      highest = -1
      #find best move
      if highest < matrix[cposy][cposx+1] < 8:  
        highest = matrix[cposy][cposx+1]
        bestmovex = 1
        bestmovey = 0
      
      if highest < matrix[cposy+1][cposx] < 8:
          highest = matrix[cposy+1][cposx]
          bestmovex = 0
          bestmovey = 1

      if highest < matrix[cposy][cposx-1] < 8:
          highest = matrix[cposy][cposx-1]
          bestmovex = -1
          bestmovey = 0

      if highest < matrix[cposy-1][cposx] < 8:
          highest = matrix[cposy-1][cposx]
          bestmovex = 0
          bestmovey = -1
      
      #move

      cposy = cposy + bestmovey
      cposx = cposx + bestmovex
      movecounter = movecounter + 1

        #add movement to movement stacks
      stackbestmovex.append(bestmovex)
      stackbestmovey.append(bestmovey)
      matrix[cposy][cposx] = 8
        #iterate neighboring of just moved into
      if matrix[cposy+1][cposx] != 8:
        matrix[cposy+1][cposx] = matrix[cposy+1][cposx]+1
      if matrix[cposy-1][cposx] != 8:
        matrix[cposy-1][cposx] = matrix[cposy-1][cposx]+1
      if matrix[cposy][cposx+1] != 8:
        matrix[cposy][cposx+1] = matrix[cposy][cposx+1]+1
      if matrix[cposy][cposx-1] != 8:
        matrix[cposy][cposx-1] = matrix[cposy][cposx-1]+1
      #print current cycle and matrix
      #print("Cycle", movecounter)
      #print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in matrix]))
      

  return movecounter

#Main Function
while True:
    try:
        numcycles=int(input("Enter desired number of fields to test: "))
        break;
    except ValueError:
        print ("Invalid input, please enter an integer.")

while True:
    try:
        x=int(input("Enter desired width of the field: "))
        break;
    except ValueError:
        print ("Invalid input, please enter an integer.")

while True:
    try:
        y=int(input("Enter desired height of the field: "))
        break;
    except ValueError:
        print ("Invalid input, please enter an integer.")

while True:
    try:
        prob=int(input("Enter desired probability of an obstacle in each cell (standard is 15): "))
        break;
    except ValueError:
        print ("Invalid input, please enter an integer.")
prob = prob/100
totalcycles = 0
counter = numcycles
#Run algorithm and average cycles


while(counter > 0):

  matrix = generate(y,x,prob)
  #Print generated obstacle matrix--
  #print("Your generated matrix is:")
  #print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in matrix]))
  matrix = obstomove(matrix)
  #Print generated movement matrix--
  #print("Your movement matrix is:")
  #print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in matrix]))
  cycles = movedrone(matrix, 0, 0, prob)
  #Print number of cycles per field
  #print("Field", numcycles-counter+1, "done in ", cycles, " cycles")
  totalcycles = totalcycles + cycles
  counter = counter -1


average = totalcycles/numcycles
#Print average number of cycles
print("Average cycles for", numcycles, "fields of", x,"x",y,"size is:", average)