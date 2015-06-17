####most recent change 06/17/15####

import numpy as np
import sys
import os
import re 
import codecs

def name_input():
    newnames = raw_input("please list names separated by spaces: ")
    newnames_split = newnames.split()
    return newnames_split

def make_norm(date,split_names):
	cwd = os.getcwd()
	for base_name in split_names:
		address = '%s/%s/%s/' % (cwd,date,base_name)
		norms = os.listdir(address)
		namelist = [x for x in norms if bool(re.search("[1-9]+.dat",x))==True]
	
		for name in namelist:
			num = name.split('.')[0]
			if not os.path.exists("%snorm" % address):
				os.makedirs(address+'norm')

			def make_na(x):
				if x == '-':
					return 'NA'
				else:
					return float(x)

			with codecs.open(address+name, "r",encoding='utf-8', errors='ignore') as fileopen:
				reading = fileopen.readlines()
			time = (i.strip('\n').split()[0] for i in reading[13:])

			decay = (float(i.strip('\n').split()[2]) for i in reading[13:])
			max_decay = max(decay)
			decay = (i.strip('\n').split()[2] for i in reading[13:])
			decay_adj = (float(i)/float(max_decay) for i in decay)

			def skip_na(x):
				if x == 'NA':
					return 'NA'
				else:
					return float(x)/float(max_decay)

			fit = (make_na(i.strip('\n').split()[3]) for i in reading[13:])
			fit_adj = (skip_na(i) for i in fit)

			residuals = (make_na(i.strip('\n').split()[4]) for i in reading[13:])

			test = [[w,x,y,z] for w,x,y,z in zip(time,decay_adj, fit_adj, residuals)]
			with open(address+'norm/norm_'+num+'.txt', 'w') as writeto:
				header = "%s %s%s %s%s %s%s\n" % ('Time_ns','Decay_',num,'Fit_',num,'Residuals_',num)
				writeto.write(header)
				for i in test:
					for z in i:
						z = str(z)
						out = "%s " % (z)
						writeto.write(out),
					writeto.write('\n'),
            
def make_rfile(date, row_cutoff,split_names):
    cwd = os.getcwd()
    row_cutoff = int(row_cutoff)
    if row_cutoff > 32767:
        sys.exit("Row cutoff too high! Recommended is 2000.")
        
    for base_name in split_names:
        variables = ['decay','residuals','fit']
        for type_fit in variables:
            if type_fit == 'decay':
                col = 2
            elif type_fit == 'residuals':
                col = 4
            elif type_fit == 'fit':
                col = 3
            else:
                sys.exit("unrecognized type \"%s\": use \'decay\' or \'residuals\' or \'fit\'")

            norms = os.listdir('%s/%s/%s/norm/' % (cwd,date,base_name)) 
            path = '%s/%s/%s/norm/' % (cwd,date,base_name)
            trunc_path = '%s/%s/%s/' % (cwd,date,base_name)

            norms = [x for x in norms if x != '.DS_Store']
            num_norms = len(norms)

            res = {}

            for file_name in norms[0:1]:
                for line_nr, line in enumerate(open(path+file_name)):
                    res.setdefault(line_nr, []).append(line.split()[0])

            for file_name in norms[0:num_norms+1]:
                for line_nr, line in enumerate(open(path+file_name)):
                    res.setdefault(line_nr, []).append(line.split()[col-1])

            if type_fit == 'residuals':
                pass
            else:
                with open(trunc_path+base_name+'_%s_average.txt'%(type_fit),'w') as write_file_average:
                    write_file_average.write("Time_ns %s_%s\n"%(base_name,type_fit))
                    for line_nr in sorted(res)[1:row_cutoff]:
                        time = res[line_nr][0]
                        if any("NA" in s for s in res[line_nr][1:]):
                            mean = "NA"
                        else:
                            numbers = [float(x) for x in res[line_nr][1:]]
                            mean = np.mean(numbers)
                        write_file_average.write("%s %s\n" % (time,mean))

            with open(trunc_path+base_name+'_%s.txt'%(type_fit),'w') as write_file:
                for line_nr in sorted(res)[1:row_cutoff]:
                    write_file.write(' '.join(res[line_nr])+'\n')

            with open(trunc_path+base_name+'_%s_long.txt'%(type_fit),'w') as long_format_file:
                long_format_file.write("Time_ns %s_num %s\n" % (type_fit,type_fit)) 
                for num in range(1,num_norms+1):
                    for row in sorted(res)[1:row_cutoff]:
                        time = res[row][0]
                        variable = res[0][num]
                        value = res[row][num]
                        long_format_file.write("%s %s %s\n" % (time,variable,value))

def make_average_combofile(date,split_names):
    cwd = os.getcwd()
    variables = ['decay','fit']
    for type_fit in variables:
        if type_fit == 'decay':
            col = 2
        elif type_fit == 'residuals':
            col = 4
        elif type_fit == 'fit':
            col = 3
        else:
            sys.exit("unrecognized type \"%s\": use \'decay\' or \'residuals\' or \'fit\'")

        basename = '%s/%s/' % (cwd,date)
        paths = ["%s%s/%s_%s_average.txt" % (basename,x,x,type_fit) for x in split_names]

        num_names = len(split_names)

        res = {}

        for file_name in paths[0:1]:
            for line_nr, line in enumerate(open(file_name)):
                res.setdefault(line_nr, []).append(line.split()[0])

        for file_name in paths[0:num_names+1]:
            for line_nr, line in enumerate(open(file_name)):
                res.setdefault(line_nr, []).append(line.split()[1])

        with open(basename+'%s_average_combo.txt'%(type_fit),'w') as long_format_file:
            long_format_file.write("Time_ns %s_num %s\n" % (type_fit,type_fit)) 
            for num in range(1,num_names+1):
                for row in sorted(res)[1:]:
                    time = res[row][0]
                    variable = res[0][num]
                    value = res[row][num]
                    long_format_file.write("%s %s %s\n" % (time,variable,value))
                    
def pipeline(date_final,cutoff_final):
    inputs = name_input()
    make_norm(date_final,inputs)
    make_rfile(date_final,cutoff_final,inputs)
    make_average_combofile(date_final,inputs)