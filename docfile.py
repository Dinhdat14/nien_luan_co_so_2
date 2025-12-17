from datetime import datetime
with open("thamdu.csv", 'r+', encoding='utf-8') as f:

        myDatalist = f.readlines()
        print(myDatalist)
        for line in myDatalist:
                entry = line.split(",") #tach theo dau ,
                print(entry)
                print(line)
now = datetime.now()
print(now)