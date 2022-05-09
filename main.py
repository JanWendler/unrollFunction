# This is a sample Python script.

# Authors: Jan und nochmals einer
# Date: 02.05.2022

import sys
import re

# Make a regular expression
# for identifying a digit
regex = '^[0-9]+$'


def findForLoopInfo(line):
    tmp = line.split("(")[1]
    tmp = tmp.split(")")[0]
    tmp = tmp.split(";")
    init = tmp[0].split()
    cond = tmp[1].split()
    change = tmp[2].split(init[0])
    return [init[2], cond[2], change[1], init[0]]


def unrollForLoops(path):
    dataFile = []
    brackets = 0
    forFound = 0
    endOfFor = 0
    tmp = []

    with open(path, "r+") as temp_f:
        dataFile = temp_f.readlines()

    while True:
        for number, line in enumerate(dataFile):
            if "for" in line and forFound == 0:
                forFound = number
                brackets = 0
            if forFound and "{" in line:
                brackets += 1
            if forFound and "}" in line:
                brackets -= 1
            if brackets == 0 and forFound > 0 and forFound != number:
                endOfFor = number
                break
        if forFound == 0:
            return dataFile

        start, stop, change, itVar = findForLoopInfo(dataFile[forFound])

        preFor = dataFile[0:forFound]
        postFor = dataFile[endOfFor+1:]
        tmp = []
        for number in range(int(start), int(stop), 1):
            for line in dataFile[forFound + 1:endOfFor+1]:
                # tmp.append(line.replace(itVar, str(number)))
                tmp.append(re.sub(r"\b%s\b" % itVar, str(number), line))
        dataFile = preFor + tmp + postFor
        forFound = 0


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    inputFilePath = "Z:/BASecurosys/Falcon-impl-original/cmake-build-debug/falcon_inner_prng_refill.txt"  # sys.argv[0]
    outputFilePath = "Z:/BASecurosys/Falcon-impl-original/cmake-build-debug/out.txt"  # sys.argv[1]
    output = unrollForLoops(inputFilePath)
    outputFile = open(outputFilePath, "w")
    outputFile.writelines(output)
    outputFile.close()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
