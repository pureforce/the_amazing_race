**Instructions for running the code**

Call method amazing_race with parameters "_path to the index.json" and "number of processes". The code runs on multiple
processes and combines the data after it reads all the files.

An example of how to run the code can be found in amazing_race.py.__main___

-------------------------------

**Problem Statement:**
A group of friends embark on an "Amazing Race" around the world. Each person in the race
takes a variety of forms of transportation for each leg of the race. Their diaries describing
their travels are encoded in json and spread out over many files. The team has been asked to
write a program that reads in all of the json files and summarizes each person’s trip. The
program should be multi-threaded so that it can efficiently parallel process all of the files; while
the examples only contain a few small files, in production we will be processing an
extraordinary amount of data.

**Input (from json files):**
index.json which contains a list of the full names of each friend participating, as well as their
nicknames. It also has a list of the filenames of the other json files, one for each day of the trip,
as well as the total distance traveled and total number of legs described in each file
data_files.json which contains a list of trip legs, in order of when they were taken, each listed
with who took that leg, what form of transportation they took, how long the leg was in km, and
their average speed on that leg in km/h

**Output (to stdout):**
1. A progress meter, writing to standard out after every 5% of the legs have been
processed
2. A list of all the friends who went on the trip, for each friend listing the total distance
traveled, and their average speed over their whole trip
3. For each friend, a list of all of the forms of transportation used during the trip, ordered
by first appearance