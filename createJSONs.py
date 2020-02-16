import argparse
import datetime
import os

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

    args = argParser.parse_args()
    
    onedateFlag = False
    daterangeFlag = False
    todayDate = None 
    dateRange = []
    
    if args.today is True:
        #call to create a json file just for today
        todayDate = datetime.date.today()
        
    elif args.nextndays is not None:
        #create for next n days
        pass
    elif args.pastndays is not None:
        #create for past n days
        pass
    
    if args.outputadirectory is True and onedateFlag is True:
        
        path = str(todayDate)[0:4] + "/" + str(todayDate)[5:7] + "/" + str(todayDate)[8:10] + ".json"
        if not os.path.exists(path[0:8]):
            os.makedirs(path[0:8])
        os.system("main.py --jsondump --singledate "+str(todayDate)+" --outputfile "+path)
        
    elif args.outputadirectory is True and daterangeFlag is True:
        
        pass

if __name__ == '__main__':
    run()