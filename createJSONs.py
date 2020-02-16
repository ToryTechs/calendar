import argparse
import datetime
import os
import subprocess

def createDateRange(startdate, N, prev):
    
    baseDate = startdate
    rangeOfDates = []
    if prev is True:
        rangeOfDates = [baseDate - datetime.timedelta(days=x) for x in range(N)]
    else:
        rangeOfDates = [baseDate + datetime.timedelta(days=x) for x in range(N)]

    return rangeOfDates

def run():
    
    argParser = argparse.ArgumentParser()
    #change --today into today's date and generate a json file for that
    argParser.add_argument("--today", help="Generate JSON file for today", action="store_true", required=False)
    #next n amount of days
    argParser.add_argument("--next-n-days", dest="nextndays", type=int, help="Generate JSON for next N consecutive days", required=False)
    #past n days
    argParser.add_argument("--past-n-days", dest="pastndays", type=int, help="Generate JSON for past N days in a row", required=False)
    #flag to output a directory
    argParser.add_argument("--outputadirectory", help="Output JSON files to directories [HOUSE]/[YEAR]/[MONTH]/[DAY]+[Timestamp].json", action="store_true", required=False)
    # The House - Commons or Lords
    argParser.add_argument("--house", help="The House (default: Commons)", required=False, default="Commons")
    
    args = argParser.parse_args()
    
    onedateFlag = False
    daterangeFlag = False
    todayDate = None
    currentHouse = ""
    dateRange = []
    thePrevN = 0
    theNextN = 0
    
    if args.today is True:
        #call to create a json file just for today
        todayDate = datetime.date.today()
        onedateFlag = True
        
    elif args.nextndays is not None:
        #create for next n days
        theNextN = args.nextndays
        daterangeFlag = True
        
    elif args.pastndays is not None:
        #create for past n days
        thePrevN = args.pastndays
        daterangeFlag = True
    
    if args.house in ["Commons", "Lords"]:
        currentHouse = args.house
    
    if args.outputadirectory is True and onedateFlag is True:
        #Commons len = 7, Lords len = 5, rest len = 10
        
        stringRange = len(currentHouse) + 10 - 2
        path = currentHouse+"/"+str(todayDate)[0:4] + "/" + str(todayDate)[5:7] + "/" + str(todayDate)[8:10] + ".json"
        
        if not os.path.exists(path[0:int(stringRange)]):
            os.makedirs(path[0:int(stringRange)])
        
        os.system("main.py --jsondump --singledate "+str(todayDate)+" --outputfile "+path)
        
    elif args.outputadirectory is True and daterangeFlag is True:
        
        stringRange = len(currentHouse) + 10 - 2
        todayDate = datetime.date.today()
        dateRange = []
        
        if theNextN != 0:
            dateRange = createDateRange(todayDate, theNextN, False)
        elif thePrevN != 0:
            dateRange = createDateRange(todayDate, thePrevN, True)
        
        for date in dateRange:
            path = currentHouse+"/"+str(date)[0:4] + "/" + str(date)[5:7] + "/" + str(date)[8:10] + ".json"
            if not os.path.exists(path[0:int(stringRange)]):
                os.makedirs(path[0:int(stringRange)])
    
            print(path)
            # os.system("main.py --jsondump --singledate "+str(todayDate)+" --outputfile "+path) 
            subprocess.run("main.py --jsondump --singledate "+str(date)+" --outputfile " + path, check=False, shell=True)
            

if __name__ == '__main__':
    run()