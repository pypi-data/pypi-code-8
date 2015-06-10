__author__ = 'Stephan Conrad <stephan@conrad.pics>'

def readfile(filename):
    data = ""
    with open(filename) as file:
        data="\n".join(line.rstrip() for line in file)
    return data

def writefile(filename, data):
    with open(filename, "w") as file:
        file.write(data)

def readfileAsArray(filename):
    data = ""
    with open(filename) as file:
        data="\n".join(line.rstrip() for line in file)
    return data.split("\n")

def writefileFromArray(filename, data):
    data = "\n".join(data)
    with open(filename, "w") as file:
        file.write(data)