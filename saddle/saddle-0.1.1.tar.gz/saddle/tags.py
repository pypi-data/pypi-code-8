## TAGS

#import os, unicodecsv, ast
#import ast
#import sys
#CURRENTFOLDER = os.path.dirname(os.path.realpath(__file__))
#SKIPFOLDERS = ['firefoxprofile', 'firefoxbinary']

#def underscore_to_camelcase(value):
#    def camelcase(): 
#        yield str.lower
#        while True:
#            yield str.capitalize

#    c = camelcase()
#    return "".join(c.next()(x) if x else '_' for x in value.split("_"))

## Get features.csv
#csvfeatures = []
#with open(CURRENTFOLDER + '/features.csv', "r") as csvfilehandle:
#    csvreader = unicodecsv.reader(csvfilehandle.readlines(), encoding='utf-8').reader
#    for row in csvreader:
#        csvfeatures.append(row)

## Drop first (title) row
#csvfeatures = csvfeatures[1:]

#testfolders = []

## Get a list of top level test folders (25marriott, howardjohnson, etc.)
#for item in os.listdir(CURRENTFOLDER):
#    if os.path.isdir(CURRENTFOLDER + '/' + item) and item not in SKIPFOLDERS:
#        testfolders.append(item)

## Get a list of all test filenames that we have
#testfilelist = []
#for testfolder in testfolders:
#    for root, dirs, filenames in os.walk(CURRENTFOLDER + '/' + testfolder):
#        for filename in filenames:
#            if filename.endswith(".py") and filename != "__init__.py":
#                testfilelist.append(root + '/' + filename)

## Get a list of associated configballs and tags with tests
#configballs = {}
#tags = {}

#for testfilename in testfilelist:
#    # Parse python tests
#    shorttestfilename = testfilename.replace(CURRENTFOLDER + '/', "")
#    with open(testfilename, "r") as testfile_handle:
#        testfilecontents = testfile_handle.read()
#    fileast = ast.parse(testfilecontents)
#    
#    # Get class object and class variables
#    classobj = [item for item in fileast.body if type(item) is ast.ClassDef][0]
#    variables = [item for item in classobj.body if type(item) is ast.Assign]
#    testfunc = [item for item in classobj.body if type(item) is ast.FunctionDef and item.name.startswith("test_")][0]
#    
#    testfiletaglist = []
#    for variable in variables:
#        if variable.targets[0].id == 'CONFIGBALL':
#            configballname = variable.value.s

#        if variable.targets[0].id == 'TAGS':
#            for tag_str in variable.value.elts:
#                testfiletaglist.append(tag_str.s)

#    camelcasedfilename = underscore_to_camelcase(os.path.splitext(os.path.basename(shorttestfilename))[0].replace("test_", ""))
#    classnamefromfilename =  camelcasedfilename[0].upper() + camelcasedfilename[1:] + "TestCase"

#    if classnamefromfilename != classobj.name:
#        print "Class name %s does not match file name %s. Should be %s" % (classnamefromfilename, shorttestfilename, classnamefromfilename)
#    if os.path.splitext(os.path.basename(shorttestfilename))[0] != testfunc.name:
#        print "Function name %s does not match file name %s." % (testfunc.name, shorttestfilename)

#    if not os.path.exists("%s/../../configball/%s.sql.gz" % (CURRENTFOLDER, configballname)):
#        print "Missing configball %s on test %s!" % (configballname, testfilename)

#    # Add test to configball dict
#    if configballname in configballs:
#        configballs[configballname].append(shorttestfilename)
#    else:
#        configballs[configballname] = [shorttestfilename]

#    # Add test to tagname dict for all tagnames the test has
#    for tagname in testfiletaglist:
#        if tagname in tags:
#            tags[tagname].append(shorttestfilename)
#        else:
#            tags[tagname] = [shorttestfilename]


#with open("report.html", "w") as reporthandler:
#    outputlist = []

#    for row in csvfeatures:
#        if row[0] in tags:
#            testcount = len(tags[row[0]])
#        else:
#            testcount = 0
#        doubtscore = (float(row[1]) * float(row[2]) * float(row[3])) / (1 + float(testcount))
#        doubtscore = int(round(doubtscore))
#        outputrow = (row[0], row[1], row[2], row[3], testcount, doubtscore)
#        outputlist.append(outputrow)


#    outputlist.sort(key=lambda x: x[5], reverse=True)

#    reporthandler.write("<html><head></head><body><table><thead> <td>Feature</td> <td>TouchScore</td> <td>Complexity</td> <td>Business Value</td> <td>Number of tests</td> <td>DoubtScore</td>  </thead><tbody>\n")
#    for row in outputlist:
#        reporthandler.write("<tr> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> </tr>\n" % tuple(row))
#    reporthandler.write("</tbody></table></html>\n")

