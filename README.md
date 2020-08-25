### Contact Author :- 
mayankjainllrl@gmail.com

### LinkedIn :- 
https://www.linkedin.com/in/mayank-jain-731325148/

#### Benefit
General purpose code for baseball data analysis.

#### How to use
User can Analyse their own data by :-
  Changing baseballdatainfo dictionary present in test_baseball_statistics.
    baseballdatainfo contains :-
      "masterfile": the name of the master CSV file that includes columns with player IDs and names.
      "battingfile": the name of the CSV file that includes columns with player IDs and batting data.
      "separator": the delimiter character used in the two CSV files.
      "quote": the quote character used in the two CSV files.
      "playerid": the name of the column header for player IDs in both the master and batting CSV files.
      "firstname": the name of the column header for player's first names in the master CSV file.
      "lastname": the name of the column header for player's last names in the master CSV file.
      "yearid": the name of the column header for the year in the batting CSV file.
      "atbats": the name of the column header for at-bats data in the batting CSV file.
      "hits": the name of the column header for hits data in the batting CSV file.
      "doubles": the name of the column header for doubles data in the batting CSV file.
      "triples": the name of the column header for triples data in the batting CSV file.
      "homeruns": the name of the column header for home runs data in the batting CSV file.
      "walks": the name of the column header for walks data in the batting CSV file.
      "battingfields": a list of column header names that correspond to batting data in the batting CSV file.
    Change this values as per the requirements of your own data.
  I have provided with three functions in this code which are :-
    1. batting_average
    2. slugging_percentage
    3. onbase_percentage
  You can write your own functions for your analysis.

###### Note :-
###### I have provided with batting data and master data of year 2016 you can use your own different data if you want.


