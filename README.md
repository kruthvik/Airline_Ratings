# Airline_Ratings
Basically a bunch of commands to find airline ratings

# **NOTE**:
Multiple airlines can be used at once, so to prevent spaces getting in the way, you would need to use a underscore. Virgin Atlantic would be virgin_atlantic.

#### **Eg**.
To find the rating of the airline Virgin Atlantic:
` py main.py -c[--command] ratings -a[--airline] virgin_atlantic `

## **Commands**
    py main.py --command add...: Adds an airplane to the airplane list
    py main.py --command get...: Returns csv file in a pandas table format
    py main.py --command help...: Provides a list of commands
    py main.py --command list...: Lists all the airplanes in the airplane list.
    py main.py --command mode...: Changes the mode of the program from emoji mode to the text mode (defualt) and vice versa
    py main.py --command ratings...: Returns the ratings of given airlines without affecting the csv file
    py main.py --command remove...: Removes the airplane from the airplane list
    py main.py --command update...: Updates the csv file to include the ratings of each airline

