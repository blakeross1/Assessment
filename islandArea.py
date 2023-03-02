import sys
import numpy as np
import os.path
from os import path


# Blake Ross
# 3-1-2023
# Clipper/Local Flavor Technical Assessment


def main():
# Initilize map, areas (set to 0 in case of no islands), and max Columns (used in case map size is not a perfect square)
    map = []
    areas = [0]
    maxCol = 0

    # Get file location argument from terminal line and see if the file exists
    if(len(sys.argv) > 1):
        fileName = str(sys.argv[1])
        if(path.exists(fileName)):
            print("Using Map: ", fileName)
            # If the provided file exists use it for your map. Go to readFromFile to extract the map from the file.
            map, maxCol = readFromFile(fileName, map)

        # If no file is provided or the file does not exist go to readFromStdin to get map from the terminal.
        else:
            print("File: ", fileName," does not exist.")
            print("Please type in your map: (Ctrl+Z on Windows/Ctrl-D on mac when finished)")
            map, maxCol = readFromStdin(map)   
    else:
        print("No file provided.")
        print("Please type in your map: (Ctrl+Z on Windows/Ctrl-D on mac when finished)")
        map, maxCol = readFromStdin(map) 
  
    # Create the array to track what parts of the map have been analized. Base size off the largest column size.
    mapSeen = np.zeros((len(map), maxCol))

    # Iterate through each row and each column of the map.
    for rowNum, row in enumerate(map):
        for colNum in range(len(row)):

            # Ensure location has not been analyzed and is not water before calucating area.
            if mapSeen[rowNum][colNum] != 1 and map[rowNum][colNum] != '~':
                # If location is land '^' Go find the area and add it to teh array of areas
                areas.append(findIslandArea(map, mapSeen, rowNum, colNum))
            else:
                # Set location to 'has been seen'
                mapSeen[rowNum][colNum] = 1

    # Present the island with the max area.
    print("The largest island is:", max(areas), "in size.")


# Function to provide the area of a given island
def findIslandArea(map, mapSeen, row, col):
        # Ensure you are within the bounds of the map
        if(row < len(map) and row >= 0 and col >= 0 and col < len(map[row])):
            # If location has been seen or is water return 0
            if(mapSeen[row][col] == 1 or map[row][col] != '^'):
                mapSeen[row][col] = 1
                return 0
            # If location has not been seen and is land, add 1 and look at adjoining locations to see if they are land.
            else:      
                islandArea = 1  
                mapSeen[row][col] = 1        
                islandArea += findIslandArea(map, mapSeen, row+1, col)
                islandArea += findIslandArea(map, mapSeen, row-1, col)
                islandArea += findIslandArea(map, mapSeen, row, col+1)
                islandArea += findIslandArea(map, mapSeen, row, col-1)
                return islandArea
        return 0

# Function to extract map from provide .txt file.
def readFromFile(fileName, map):
    maxCol = 0
    file = open(fileName, 'r')
    # While lines exist append each line to the map.
    while True:
        line = file.readline()
        map.append(line.strip())
        if(len(line.strip()) > maxCol):
            maxCol = len(line.strip())   
        if not line:
            break
    return map, maxCol

# Function to read map from the terminal.
def readFromStdin(map):
    maxCol = 0
    for line in sys.stdin:
        if line.strip() != "":
            map.append(line.strip())
            if(len(line.strip()) > maxCol):
                maxCol = len(line.strip())  
    return map, maxCol

if __name__ == '__main__':
    main()