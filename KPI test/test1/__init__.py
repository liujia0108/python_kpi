#encoding:utf-8
import os,sys
import re
import time
import subprocess
import smtplib
from pychartdir import *
import xlrd
import xlwt
from xlutils.copy import copy


def addNewLine(filename,content):
    f = open(filename,'a')
    f.write(content+'\n')
    f.close()
    
def draw_pic():
    traceID = []
    f = open(searchresult,'r')
    lines = f.readlines()
    for line in lines:
        single = line.split(',')
        #debug print
        print "single value is %s"%single
        occurence_time = single[0]
        used_time_list = single[2]
        trace = single[1]
        if trace not in traceID:
            traceID.append(trace)
    traceID_num = len(traceID)
    f.close()
    #debug print 
    print "traceId list is %s"%traceID
    print "trace num is %s"%traceID_num
    for i in range(0,traceID_num-1):
        file = open(searchresult,'r')
        file_lines = file.readlines()
        abscissa_list = []
        ordinate_list = []
        sum = 0
        for line in file_lines:
            #debug print
            print "get in draw loop!"
            data = line.split(',')
            data_time = data[0]
            data_trace = data[1]
            data_usedtime = data[2]
            if data_trace == traceID[i]:
                #debug print
                print "now will draw the traceID is:%s"%traceID[i]
                abscissa_list.append(data_time)
                ordinate_list.append(data_usedtime)
        #debug print
        print "abscissa_list is :%s"%abscissa_list
        print "ordinate_list is :%s"%ordinate_list
        sum_num = len(ordinate_list)
        for j in range(0,sum_num -1):
            sum = sum + float(ordinate_list[j])
        average = round(sum/sum_num,2)
        print "now the %s average is %f"%(traceID[i],average)
        
        file.close()
        c = XYChart(1400,600)
        c.addTitle("%s Occurence Time"%traceID[i])
        c.setPlotArea(50,55,1300,500)
        #c.yAxis().setLabelFormat("{value}")
        layer = c.addLineLayer(ordinate_list)
        layer.addDataSet(ordinate_list).setDataSymbol(SquareSymbol,7)#add symbol for each value
        layer.setDataLabelFormat("{value}")
        c.xAxis().setLabels(abscissa_list)
        c.xAxis().setLabelStep(len(abscissa_list)-1)
        c.makeChart("D:\\work\\KPI\\%s.png"%traceID[i])
        
        #write into excel
        excel_path = xlrd.open_workbook(r'D:\\work\\KPI\\performance\\funrom performace1010_new (2).xls')
        table = excel_path.sheet_by_name('Sheet1')
        print "nrows is %s"%table.nrows
        print "ncols is %s"%table.ncols
        cols_value = table.col_values(2)
        print cols_value#debug print
        cols_value_num = len(cols_value)
        print "the total cols value are:%s"%cols_value_num
        for z in range(0,cols_value_num -1):
            if cols_value[z] == traceID[i]:
                wb = copy(excel_path)
                ws = wb.get_sheet(0)
                ws.write(z,10,average)
                #wb.save()
            else:
                pass
        wb.save('D:\\work\\KPI\\performance\\funrom performace1010_new (2).xls')#save must add save path in (),if not add,such as wb.save(),will report error
        

#def add_value_excel():
              
#def change_excel_style():
                
            
    
    
folder = "D:\\work\\KPI"
searchresult = "D:\\work\\KPI\\searchresult.txt"
if not os.path.exists(searchresult):
    f = open(searchresult,'w')
    f.close()

log_all = subprocess.Popen('adb logcat -v time',shell = True,stdout = subprocess.PIPE)
while log_all.poll() ==None:
    log = log_all.stdout.readline()
    line_funperformance = re.compile(r'.*FUNPERFORMANCE.*')
    line_fpstart = re.compile(r'(?P<log_time1>.+)\:.+FUNPERFORMANCE.+FPSTART\|(?P<traceId1>\w+\_\d+)\|(?P<uuid1>.+)\|(?P<start_time>\d+).*',re.DOTALL)
    line_fpstop = re.compile(r'(?P<log_time2>.+)\:.+FUNPERFORMANCE.+FPSTOP\|(?P<traceId2>\w+\_\d+)\|(?P<uuid2>.+)\|(?P<stop_time>\d+).*',re.DOTALL)
    line_duration = re.compile(r'(?P<log_time3>.+)\:.+FUNPERFORMANCE.+FPDURATION\|(?P<traceId3>\w+\_\d+)\|(?P<duration_time>\d+).*',re.DOTALL)
    search_result1 = line_funperformance.search(log)
#debug print
    print search_result1
    if search_result1:
        #debug print
        print "has searched the funperformance!"
        search_result2 = line_fpstart.search(log)
        search_result3 = line_fpstop.search(log)
        search_result4 = line_duration.search(log)
        if search_result2:
            #debug print
            print "has searched the start line!"
            logTime1 = search_result2.group('log_time1')
            traceid1 = search_result2.group('traceId1')
            uuid1 = search_result2.group('uuid1')
            start_time = search_result2.group('start_time')
            
        elif search_result3:
                #debug print
            print "has searched the stop line!"
            logTime2 = search_result3.group('log_time2')
            traceid2 = search_result3.group('traceId2')
            uuid2 = search_result3.group('uuid2')
            stop_time = search_result3.group('stop_time')
            if traceid1 == traceid2 and uuid1 == uuid2:
                start_time_f = float(start_time)
                print "start_time is %f"%start_time_f
                stop_time_f = float(stop_time)
                print "stop_time is %f"%stop_time_f
                used_time = round(stop_time_f - start_time_f,2)
                used_time_str = str(used_time)
                print "used_time is %f"%used_time
                addNewLine(searchresult,logTime2+','+traceid2+','+used_time_str+',')
            else:
                pass
        elif search_result4:
                #debug print
            print "has searched the duration line!"
            print "duration search result:%s"%search_result4
            logTime3 = search_result4.group('log_time3')
            duration_time = search_result4.group('duration_time')
            traceid3 = search_result4.group('traceId3')
            addNewLine(searchresult,logTime3+','+traceid3+','+duration_time+',')
        else:
            pass
    else:
        pass
    
    draw_pic()
            
            
            
                
    