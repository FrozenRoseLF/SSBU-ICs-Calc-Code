# SSBU-ICs-Calc-Code
Coding project spawned from ICcord for furthering resources and meta.

To use, first change all "PathToFile" like mentions to their appropiate files. Such as attribute data to "Character_Attribute_Data.xlsx" and output spreadsheet to a folder and file name of your desire. There is also a dump file of the KuroganeHammer API data that needs to be set or commented out to run. The dump file is useful for getting a look at what data you are using and to understand how the data is conatined if you wish to modify the code. 

When generating, set your desired knockback value, which will be used to find the percent at which the selected move will deal that amount of knockback. It already takes into account character specific knockback multipliers and damage multipliers as specified in the Character Attribute Data spreadsheet. Other values to set are freshness/staleness multiplier of the move also in the defined function, rage via keyword arguments when calling a function, and shorthop multiplier via keyword arguments when calling a function.

Lastly, input your desired move using "MD.LP['Move Name Here']". At the botttom of "Calc_Iteration_Code.py" is a print call that will print all of the move names to the IDLE.
