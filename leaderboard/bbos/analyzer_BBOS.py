import json
import math
import pandas as pd
import datetime

record_file = r"D:\Doc\data\BBOS.log"
all_records = []

with open(record_file, "r") as f:
    all_line = f.readlines()
    for line in all_line:
        record_time = line[line.index("[") + 1: line.index("]")]
        
        record_order = json.loads(line[line.index("{"):])
        for item in record_order["data"]["otherPositionRetList"]:
            item["time"] = datetime.datetime.fromtimestamp(math.floor(float(record_time)/1000)).strftime(r"%Y-%m-%d %H:%M:%S")
            all_records.append(item)

record_frame = pd.DataFrame(all_records)
print(record_frame.columns)
print(record_frame.sort_values(by=['symbol', 'time'] , ascending=[1,1]))