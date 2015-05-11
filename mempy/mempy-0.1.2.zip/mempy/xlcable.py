# *-* coding: UTF-8 -*-
#==============================================================================
"""
[xlcable.py] - Mempire Excel-Python Link module

이 모듈은 Microsoft Excel과 Python 연결 기능을 구현한 모듈입니다.

"""
__author__ = 'Herokims'
__ver__ = '150511'
__since__ = '2015-05-11'
__copyright__ = 'Copyright (c) TreeInsight.org'
__engine__ = 'Python 3.4.1'
#==============================================================================


import numpy as np
import pandas as pd
#xlwings모듈의 Workbook, Range객체는 Excel데이터 입출력에 있어 매우 편리하나, 
#파일로 저장된 바 있는 Workbook을 열어 데이터를 입출력할 때, 
#파일경로에서 파일을 찾을 수 없다는 에러가 발생하는 문제가 있으므로,
#엑셀->파이썬은 win32com, 파이썬->엑셀은 xlwings 모듈사용
from win32com.client import dynamic
from xlwings import Workbook,Sheet,Range


def xl2py(workbookname, sheetname, range_address=None, page_size=30000):
    '''
기    능 : 지정하는 Excel 워크북의 지정하는 워크시트에서 data를 가져온다.
입    력 : wbname은 열려있는 워크북이름(또는 워크북파일 경로), sheetname은 워크시트이름
           range_address는 데이터를 가져올 범위주소(비어있으면 A1셀부터 UsedRange까지),
           page_size는 데이터블록 전송시 블록의 크기
출    력 : 성공하면 pandas DataFrame객체, 실패하면 None객체를 반환한다.
주    의 : 1. range_address는 (좌측상단셀행,좌측상단셀열,우측하단셀행,우측하단셀열)의 튜플
           2. range_address를 지정하지 않으면 A1셀부터 UsedRange까지를 반환한다.
    '''
    
    
    try:
        #win32com모듈 사용
        #-----------------------------------------------------
        xl = dynamic.Dispatch("Excel.Application")
        ws = xl.Workbooks(workbookname).Worksheets(sheetname)
        #-----------------------------------------------------
    except:
        print("\n지정하는 워크북 또는 그 워크시트를 찾을 수 없습니다!")
        return None
    
    #range_address가 지정되지 않은 경우는 대상 시트의 UsedRange 사용
    #(아무런 내용이 없는 경우에도 range_rowend와 range_colend는 각각 1로 반환)
    if range_address is None:
        try:
            range_rowstart = 1
            range_rowend = ws.UsedRange.Row + ws.UsedRange.Rows.Count - 1
            range_colstart = 1            
            range_colend = ws.UsedRange.Column + ws.UsedRange.Columns.Count - 1
        except:
            print("\n지정하는 워크시트의 UsedRange를 찾을 수 없습니다!")
            return None 
    else:
        try:
            range_rowstart = int(range_address[0])
            range_colstart = int(range_address[1])
            range_rowend = int(range_address[2])
            range_colend = int(range_address[3])   
        except:
            print("\nrange_address가 올바른 형식이 아닙니다!")
            return None
    
    if range_rowstart < 1 or range_colstart < 1 or \
       range_rowend < 1 or range_colend < 1 or \
       range_rowend < range_rowstart or range_colend < range_colstart or \
       range_rowend > 1048576 or range_colend > 16384:
           print("\nrange_address가 올바른 형식이 아니거나, Excel의 범위를 벗어났습니다!")
           return None        
           
    try:
        #win32com모듈 사용
        #---------------------------------------------------------------- 
        xldata_raw = ws.Range(ws.Cells(range_rowstart,range_colstart),\
                              ws.Cells(range_rowend,range_colend)).Value
        xldata = np.array(xldata_raw)
        #----------------------------------------------------------------

        #데이터에 따라, index과 label을 따로 가지고 있지 않을 수도 있으므로 디폴트 변환한다.
        df = pd.DataFrame(xldata)
        
        print("\n데이터 수신이 성공했습니다.\n") 
        return df
    
    #이 부분에서는 Memory용량 때문에 오류났을 가능성이 높음
    except:
     
        if ws is None:
            ws = xl.Workbooks(workbookname).Worksheets(sheetname)
        
        #대상 시트의 A1셀에만 데이터가 있는 경우에는 데이터를 List로 만들어 입력해야만
        #DataFrame을 만들 수 있음('ValueError(Must pass 2-d input)'에러 발생)         
        if range_rowstart == range_rowend == \
           range_colstart == range_colend == 1:
               
            df = pd.DataFrame(np.array([ws.Range("A1").Value,]))  
             
            print("\n데이터 수신이 성공했습니다.\n") 
            return df
            
        try:
            
            print("\n데이터블록으로 나누어 받습니다..\n")
            
            pagenum,tmp  = divmod(range_rowend,page_size)                
            pagenum += 1    #최종 pagenum은 남은 부분을 담을 페이지까지 포함해서 결정
            
            #page_size만큼 page로 나누어 로딩하고(1번째 ~ pagenum-1번째),        
            for p_index in range(pagenum-2):
    
                xldata_raw = None
                xldata_raw = ws.Range(ws.Cells(p_index * page_size+1,1),\
                                  ws.Cells((p_index+1)*page_size,range_colend)).Value
                
                xldata = np.array(xldata_raw)
                
                df_part = None
                df_part = pd.DataFrame(xldata)    
                
                if p_index == 0:
                    df = df_part
                else:
                    df = df.append(df_part,ignore_index=True)   
                    
                print("%2d/%d 데이터블록 받음" % (p_index+1,pagenum))
    
            #남은 부분을 로딩한다(pagenum번째).
            xldata_raw = None
            xldata_raw = ws.Range(ws.Cells((pagenum-1)*page_size + 1,1),\
                                  ws.Cells(range_rowend,range_colend)).Value
            
            xldata = np.array(xldata_raw)
            
            df_part = None
            df_part = pd.DataFrame(xldata)
            
            df = df.append(df_part,ignore_index=True)
            
            print("%2d/%d 데이터블록 받음" % (pagenum,pagenum))
            
            print("\n데이터블록 수신이 성공했습니다.\n")
            return df
            
        except Exception as e:
            
            print(e.args)
            print("\n알 수 없는 에러가 발생하여 df를 만들지 못했습니다!\n" + \
                  "(page_size가 너무 컸을 수도 있습니다)")
            return None
    

def py2xl(data, workbookname=None, sheetname=None, page_size=30000):
    '''
기    능 : data를 지정하는 Excel 워크북(미입력시 새 워크북)으로 전송한다.
입    력 : data는 pandas DataFrame객체, 
           workbookname은 데이터를 전송하고자 하는 워크북(미입력시 새 워크북),
           sheetname은 데이터를 전송하고자 하는 워크시트(미입력시 새 시트),
           page_size는 데이터블록전송시 블록크기(미입력시 30000)
출    력 : 성공하면 1, 실패하면 0
주    의 : 대상 워크시트의 A1셀을 기준으로 데이터가 입력된다.
    '''
#개발자주의사항 : 1. xlwings모듈은 좌측상단의 셀주소만 알면 Range 전체를 입력가능하므로,
#                  win32com 대신 xlwings모듈을 사용한다.
    
    
    if data is None:
        print("data변수가 비어있습니다!")
        return 0
    else:
        
        #xlwings모듈과 win32com모듈을 혼합사용
        #(xlwings모듈은 파일로 저장된 바 있는 Workbook을 열어 데이터를 입출력할 때,
        #파일경로에서 파일을 찾을 수 없다는 에러가 발생하는 문제가 있음)
        #---------------------------------------------------
        xl = dynamic.Dispatch("Excel.Application")
        
        if workbookname is None:
            wb_new = Workbook()
            sheetname = "Sheet1"
        else:
            #workbookname이 경로명을 포함한 경우
            #(아직 열리지 않은 엑셀파일을 열고자 하는 경우)
            if "\\" in workbookname:
                try:
                    wb_new = Workbook(workbookname)
                except:
                    wb_new = Workbook()
                    sheetname = "Sheet1"
            
            #파일명인 경우
            else:
                try:
                    
                    wbpath = str(xl.Workbooks(workbookname).Path)
                    
                    #workbookname은 존재하나, Unsaved Workbook
                    if len(wbpath) == 0:   
                        wb_new = Workbook(workbookname)
                        
                    #workbookname은 존재하나, Saved Workbook    
                    else:
                        wbpath = wbpath + "\\" + workbookname                          
                        wb_new = Workbook(wbpath)
                        
                except:
                    wb_new = Workbook()
                    sheetname = "Sheet1"

        if sheetname is None:
            sheetindex = Sheet.add().index
        else:
            try:
                sheetindex = Sheet(sheetname).index
            except:
                sheetindex = Sheet.add().index
        #--------------------------------------------------- 
        
        try:
            #효율적인 전송을 위해 데이터블록 전송방식으로 바로 넘어감
            raise Exception
            
            #----------------------------------------------------------------
            #이 부분은 데이터를 통째로 전송하기 위한 부분으로 사실상 사용하지 않음
            Range(sheetindex,"A1").table.value = data.values.tolist()
            #----------------------------------------------------------------
            
            print("\n데이터 전송이 성공했습니다.\n") 
            return 1
            
        except:
                            
            try:
        
                range_rowend = data.values.shape[0]
                range_colend = data.values.shape[1]

                print("\n'" + wb_new.name + "'에 데이터블록으로 나누어 보냅니다..\n")
                
                pagenum,tmp  = divmod(range_rowend,page_size)                
                pagenum += 1    #최종 pagenum은 남은 부분을 담을 페이지까지 포함해서 결정
                
                #page_size만큼 page로 나누어 로딩하고(1번째 ~ pagenum-1번째),        
                for p_index in range(pagenum-1):
        
                    data_part = None
                    data_part = data[p_index*page_size:(p_index+1)*page_size]
                    Range(sheetindex,(p_index*page_size+1,1)).value = data_part.values.tolist()
                        
                    print("%2d/%d 데이터블록 보냄" % (p_index+1,pagenum))
                        
                #남은 부분을 로딩한다(pagenum번째).
                data_part = None
                data_part = data[(pagenum-1)*page_size:]
                
                Range(sheetindex,((pagenum-1)*page_size+1,1)).value = data_part.values.tolist()
                
                print("%2d/%d 데이터블록 보냄" % (pagenum,pagenum))   
                print("\n데이터블록 전송이 성공했습니다.\n")
                return 1                
                
            except Exception as e:
                
                print(e.args)
                print("Excel 데이터블록 전송과정에서 에러가 발생했습니다!\n" + \
                      "(page_size가 너무 컸을 수도 있습니다)")
                return 0 
        

if __name__ == "__main__":
    pass
