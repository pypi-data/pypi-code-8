def combination(result_list,str,prev_str):
    if len(str)==0:
        result_list.append(prev_str)
    else:
        for i in range(len(str)):
            new_str=str[:i]+str[i+1:]
            combination(result_list,new_str,str[i]+prev_str)
            
if __name__=="__main__":
    result_list=[]
    combination(result_list,"abc","")
    print(result_list)            