import sys, os, operator

file = "data.txt"
successFile = open("parse_data/success.txt", "w")
failedFile = open("parse_data/failed.txt", "w")
error_log = open("parse_data/error_log.txt", "w")

success = 0
failed = 0
error_table = {}

with open(file) as f:
    line = f.readline()
    count = 1
    while line:
        num = line.split(' ')

        if str(num[0]) == str(count):
            count += 1

            # Count success or fail
            if (num[1] == "**SUCCESS"):
                success += 1
                successFile.write(num[2].strip() + "\n")
                
            elif (num[1] == "***Failed"):
                failed += 1
                failedFile.write(num[4].strip() + "\n")

                if (num[5][0:5] == "[Line"):
                    together = num[5] + " " + num[6] + " " + num[7] + " " + num[8]
                    error = line.split(str(together), 1)[1].lstrip().rstrip()

                # Combines the 'utf-8' errors (comment out if you want each one seperate)
                elif (num[5] == "'utf-8'"):
                    error = num[5] + " " + num[6] + " " + num[7] + " " + num[8] + " " + num[9]

                else:
                    error = line.split(num[4], 1)[1].lstrip().rstrip()

                if error in error_table.keys():
                    value = error_table[str(error)].split(' ')
                    newCount = int(value[0]) + 1
                    endResult = str(newCount) + " " + value[1]
                    error_table[str(error)] = endResult
                else:
                    value = str(1) + " " + num[4]
                    error_table[str(error)] = value

        line = f.readline()


print("Success: " + str(success))
print("Failed: " + str(failed))

for key, value in error_table.items():
    # print("Num: " + str(value) + " | " + str(key))
    splitting = value.split(' ')
    error_log.write("Count: " + str(splitting[0]) + " | File: " + str(splitting[1]) + " | " + str(key) + "\n")
