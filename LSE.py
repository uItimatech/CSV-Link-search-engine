'''-------------------------------------------
              Link search engine
----------------------------------------------
A simple and lightweight search engine for 
.csv link sheets.
Simply put your sheet inside the 'link sheets'
folder and run this script.

Created by ultimatech
First update: 24/07/2022 18:27
Last update: 27/07/2022 18:33
Version: Beta 1.1

                    2022
-------------------------------------------'''

# ------------ Import modules --------------

import os, math
from time import sleep

# Tries to import the termcolor module or asks the user to install it
try:
    from termcolor import colored
except ImportError:
    print('termcolor module not found. Would you like to install it? (y/n)')
    _install = input()
    if _install in ['y','yes','Y','Yes','YES']:
        os.system('python -m pip install termcolor')
        from termcolor import colored
    else:
        print('You can install it manually by running: python -m pip install termcolor\nExiting...')
        sleep(3)
        exit()

# Tries to import the pandas module or asks the user to install it
try:
    from pandas import read_csv
except ImportError:
    print('pandas module not found. Would you like to install it? (y/n)')
    _install = input()
    if _install in ['y','yes','Y','Yes','YES']:
        os.system('python -m pip install pandas')
        from pandas import read_csv
    else:
        print('You can install it manually by running: python -m pip install pandas\nExiting...')
        sleep(3)
        exit()

# Tries to import the pyperclip module or asks the user to install it
try:
    from pyperclip import copy
except ImportError:
    print('pyperclip module not found. Would you like to install it? (y/n)')
    _install = input()
    if _install in ['y','yes','Y','Yes','YES']:
        os.system('python -m pip install pyperclip')
        from pyperclip import copy
    else:
        print('You can install it manually by running: python -m pip install pyperclip\nExiting...')
        sleep(3)
        exit()

# Tries to import the webbrowser module or asks the user to install it
try:
    from webbrowser import open as openWeb
except ImportError:
    print('webbrowser module not found. Would you like to install it? (y/n)')
    _install = input()
    if _install in ['y','yes','Y','Yes','YES']:
        os.system('python -m pip install webbrowser')
        from webbrowser import open as openWeb
    else:
        print('You can install it manually by running: python -m pip install webbrowser\nExiting...')
        sleep(3)
        exit()

# NB: You might need to install those last extensions using the 'pip install termcolor' command etc..

# --------------- Functions ----------------

# Clears the console
# Might need to be changed for other OS
def clearConsole():
  # Windows
  if 'nt' in os.name:
    os.system('cls')
  # Linux and probably Mac
  else:
    os.system('clear')

# Shows the search progress bar
def progressBar(_currentItem,_maxItems):

    _currentProgress = round(_currentItem * 20 / _maxItems)

    # Displays the progress only if different from last cycle
    if _currentProgress != round((_currentItem - 1) * 20 / _maxItems):
        clearConsole()
        print(*[colored('━','green') for _tile in range(_currentProgress)],*[colored('━','red') for _tile in range(20 - _currentProgress)],' ',_currentItem,'/',_maxItems,' links searched',sep="")


# Converts
def convertSize(bytesSize):

   if bytesSize == 0:
       return "0B"

   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(bytesSize, 1024)))
   p = math.pow(1024, i)
   s = round(bytesSize / p, 2)

   return "%s %s" % (s, size_name[i])

# Find titles from specific keyword(s)
def searchKeys(selectedFile,_keywords):

    _titleList  = []
    _titleSizes = []
    _titleLinks = []

    for _filePath in selectedFile:
        _file       = read_csv('link sheets/' + _filePath)
        _titleList  += _file['title'].tolist()
        _titleSizes += _file['size'].tolist()
        _titleLinks += _file['link'].tolist()

    _currentId = 0
    foundIds, foundTitles, foundSizes, foundLinks = [], [], [], []

    for _currentTitle in _titleList:
        _currentId += 1
        _matchKeywords = 0
        progressBar(_currentId,len(_titleList))

        for _currentKeyword in _keywords:
            if _currentTitle.lower().find(_currentKeyword) != -1:
                _matchKeywords +=1

        if _matchKeywords == len(_keywords):
            foundIds.append(_currentId)
            foundTitles.append(_currentTitle)
            foundSizes.append(_titleSizes[_currentId-1])
            foundLinks.append(_titleLinks[_currentId-1])

    return foundIds, foundTitles, foundSizes, foundLinks
 

#searchKeys('link sheets/'+_filePath,'test')
#sleep(5)


# ------------ Get link sheet --------------

clearConsole()

linkSheetFolder = 'link sheets'
linkSheetFiles = []



# Lists .csv files in the sheet folder
for _filePath in os.listdir(linkSheetFolder):

    # Check if current path is a .csv file
    if os.path.isfile(os.path.join(linkSheetFolder, _filePath)) and _filePath[-4:] == '.csv':
        linkSheetFiles.append(_filePath)



# Checks for the number of files found
if len(linkSheetFiles) != 0:

    print(colored(str(len(linkSheetFiles)) + " file(s) found:\n", attrs=['bold']))
    _id = 0

    for _currentFile in linkSheetFiles:
        _id += 1
        print(colored(str(_id)+" - "+_currentFile[:-4],'blue'))

else:
    print(colored("No files found.\n",'red') + colored("Please place your .csv files in the software 'link sheets' folder.",'cyan'))



# Ask the user for the desired file
while True:

    selectedID = input("\nType the desired file Id (all will search through all the csv): ")

    # Check if selectedID is all
    if selectedID == 'all':
      selectedFile = linkSheetFiles
      break

    # Check for valid file id
    if not selectedID in [str(_id) for _id in range(1,len(linkSheetFiles)+1)]:
        print(colored("Please choose a valid file id.",'red'))

    else:
        selectedFile = []
        selectedFile.append(linkSheetFiles[int(selectedID)-1])
        break


clearConsole()

previousKeywords = []

# Search for files containing keyword(s)
while True:
    
    # Prints the found results and highlights keywords in titles
    def printResults(_keywords):

        for _Id in range(0,len(foundIds)):
            _Title = foundTitles[_Id]                                               # Full filename
            _Link = colored(foundLinks[_Id], attrs=['bold'])                        # Link
            _Size = colored(convertSize(foundSizes[_Id]),'red')                     # Size of file
            _Name = colored(_Title[:- len(_Title.split('.')[-1])-1],'blue')         # Filename without extension
            _Extension = colored('.'+_Title.split('.')[-1],'cyan')                  # File extension

            # Highlights keywords
            _keyPos = []
            for _keyword in _keywords:
                _start = _Name.lower().find(_keyword.lower())
                _end = _start + len(_keyword)
                _Name = _Name[:_start] + colored(_Name[_start:_end], attrs=['reverse']) + colored(_Name[_end:],'blue')

            # Prints all informations
            print(colored(str(_Id+1)+' -','yellow'),  colored('#' + str(foundIds[_Id]),'magenta'),  _Name + _Extension,  _Size,  _Link)



    # Ask user for keywords, uses previous keywords if no keywords are given
    print("Please enter desired keywords:",colored("(syntax: word1,word2,...)", attrs=['bold']))
    keywords = str(input("{} \r".format(colored(str(previousKeywords).replace('[','').replace(']','').replace("'",''),'cyan'))) or (str(previousKeywords).replace('[','').replace(']','').replace("'",''))).lower().split(',')
    keywords += previousKeywords[len(keywords):]
    previousKeywords = keywords


    # Gets a list of ids corresponding to each title matching desired keywords
    foundIds, foundTitles, foundSizes, foundLinks = searchKeys(selectedFile, keywords)

    # Prints the found results and highlights keywords in titles
    clearConsole()
    print(colored("Found " + str(len(foundIds)) + " results.",'green'))
    printResults(keywords)

    # Ask user for next action
    print(colored("\nAvailable actions:\n", attrs=['bold']) + "\n1 - Edit search\n2 - Copy all links to clipboard\n3 - Open all links in chrome\n4 - Copy desired links to clipboard\n5 - Open desired links in chrome\n6 - Exit\n" + colored("\nEnter the number of the desired action:",'cyan'))

    # Get user input
    while True:
        userInput = input()

        # Check for valid input
        if userInput in ['1','2','3','4','5','6']:
            if userInput == '1':
                # Edit last keywords
                clearConsole()

            elif userInput == '2':
                # Copy all links to clipboard
                _toCopy = []
                for _Id in range(0,len(foundIds)):
                    _toCopy.append(foundLinks[_Id]+'\n')

                copy(''.join(_toCopy)) # Copy link(s) to clipboard

                clearConsole()
                print(colored("Link(s) copied to clipboard.\n",'green'))

            elif userInput == '3':
                # Open all links in browser
                clearConsole()

                if len(foundIds) > 10:
                    print(colored("Warning: opening too many links may cause your browser to crash or pages to load incorrectly.\n",'red') + colored("Continue? (y/n)",'cyan'))

                    while True:
                        _userInput = input()
                        if _userInput in ['y','yes','Y','Yes','YES']:
                            print(colored("\nPlease wait while links are opened in browser...\n",'cyan'))
                            for _Id in range(0,len(foundIds)):
                                openWeb(foundLinks[_Id])
                            break

                        elif _userInput in ['n','no','N','No','NO']:
                            break

                        else:
                            print(colored("Please choose a valid option.",'red'))

                    clearConsole()

                else:
                    print(colored("\nPlease wait while links are opened in browser...\n",'cyan'))

                    for _Id in range(0,len(foundIds)):
                        openWeb(foundLinks[_Id]) # Open link(s) in browser

                clearConsole()

            elif userInput == '4':
                # Copy desired links to clipboard

                while True:
                    # Ask user for desired links ids separated by commas and turn them into a list
                    print("\nPlease enter desired link ids:",colored("(syntax: 1,3,7,...)", attrs=['bold']))
                    _userInput = input().split(',')

                    # Check for valid input
                    if not all([_id in [str(_id) for _id in range(1,len(foundIds)+1)] for _id in _userInput]):
                        print(colored("Please choose valid link(s) id(s).",'red'))
                    else:
                        break

                # Copy desired links to clipboard
                _toCopy = []
                for _Id in _userInput:
                    _toCopy.append(foundLinks[int(_Id)-1]+'\n')

                copy(''.join(_toCopy)) # Copy link(s) to clipboard

                clearConsole()
                print(colored("Link(s) copied to clipboard.\n",'green'))


            elif userInput == '5':
                # Open desired links in browser

                while True:
                    # Ask user for desired links ids separated by commas and turn them into a list
                    print("\nPlease enter desired link ids:",colored("(syntax: 1,3,7,...)", attrs=['bold']))
                    _userInput = input().split(',')

                    # Check for valid input
                    if not all([_id in [str(_id) for _id in range(1,len(foundIds)+1)] for _id in _userInput]):
                        print(colored("Please choose valid link(s) id(s).",'red'))
                    else:
                        break

                # Open desired links in browser
                print(colored("\nPlease wait while links are opened in browser...\n",'cyan'))

                for _Id in _userInput:
                    openWeb(foundLinks[int(_Id)-1]) # Open link(s) in browser

                clearConsole()


            elif userInput == '6':
                # Close program
                clearConsole()
                exit()

            break

        else:
            print(colored("Please choose a valid option.",'red'))
