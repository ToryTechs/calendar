#!/usr/bin/env python3

import argparse
import datetime
import os
import subprocess

def create_date_range(startdate, N, prev):
    
    base_date = startdate
    range_of_dates = []
    if prev is True:
        range_of_dates = [base_date - datetime.timedelta(days=x) for x in range(N)]
    else:
        range_of_dates = [base_date + datetime.timedelta(days=x) for x in range(N)]

    return range_of_dates

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
    
    one_date_flag = False
    date_range_flag = False
    today_date = None
    current_house = ""
    date_range = []
    the_previous_n = 0
    the_next_n = 0
    
    if args.today is True:
        #call to create a json file just for today
        today_date = datetime.date.today()
        one_date_flag = True
        
    elif args.nextndays is not None:
        #create for next n days
        the_next_n = args.nextndays
        date_range_flag = True
        
    elif args.pastndays is not None:
        #create for past n days
        the_previous_n = args.pastndays
        date_range_flag = True
    
    if args.house in ["Commons", "Lords"]:
        current_house = args.house
    
    if args.outputadirectory is True and one_date_flag is True:
        #Commons len = 7, Lords len = 5, rest len = 10
        
        string_range = len(current_house) + 10 - 2
        path = current_house + "/" + str(today_date)[0:4] + "/" + str(today_date)[5:7] + "/" + str(today_date)[8:10] + ".json"
        
        if not os.path.exists(path[0:int(string_range)]):
            os.makedirs(path[0:int(string_range)])
        
        subprocess.run("./main.py --jsondump --singledate %s --outputfile %s --house %s"  % (str(today_date), path, current_house), check=False, shell=True)
        
    elif args.outputadirectory is True and date_range_flag is True:
        
        string_range = len(current_house) + 10 - 2
        today_date = datetime.date.today()
        date_range = []
        
        if the_next_n != 0:
            date_range = create_date_range(today_date, the_next_n, False)
        elif the_previous_n != 0:
            date_range = create_date_range(today_date, the_previous_n, True)
        
        for date in date_range:
            path = current_house +"/" + str(date)[0:4] + "/" + str(date)[5:7] + "/" + str(date)[8:10] + ".json"
            if not os.path.exists(path[0:int(string_range)]):
                os.makedirs(path[0:int(string_range)])
    
            print(path)
            subprocess.run("./main.py --jsondump --singledate %s --outputfile %s --house %s" % (str(date), path, current_house), check=False, shell=True)
            

if __name__ == '__main__':
    run()
