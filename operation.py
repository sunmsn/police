#!/usr/bin/python
#coding:utf-8
import datetime,time
import json
revel={'1':'信息','2':'警告','3':'一般严重','4':'严重','5':'灾难'}
#告警合并
def mergeproblem(originallist):
    problemlist=[]
    problemlist1=[]
    normalist=[]
    Unknown=[]
    triggerkeylist=[]
    hostlist=[]
    sorts=[]
    hostlist=[]
    alarminfo=[]
    #告警or恢复
    for origina in originallist:

        if origina['triggervalue']=='1' :            
            problemlist.append(origina)
            if origina['triggerkey'] not in triggerkeylist:
                triggerkeylist.append(origina['triggerkey'])
        else :
            Unknown.append(origina)
    print triggerkeylist
    for triggerkey in triggerkeylist:
        for problem in problemlist:
            if problem['triggerkey']==triggerkey:
                sorts.append(problem)
	if len(sorts)>=2:
	    alarminfo.append(sorts)
	else:
	    problemlist1.append(sorts)
        sorts=[]
    print problemlist1
    for problem in problemlist1:
	if problem[0]['ipaddress'] not in hostlist:
	    hostlist.append(problem[0]['ipaddress'])
    print hostlist
    for host in hostlist:
	for problem in problemlist1:
	    if problem[0]['ipaddress']==host:
		sorts.append(problem[0])
	alarminfo.append(sorts)
	sorts=[]
    print alarminfo
    return alarminfo
#恢复合并
def mergenormal(originallist):
    normallist=[]
    normallist1=[]
    Unknown=[]
    triggerkeylist=[]
    hostlist=[]
    sorts=[]
    alarminfo=[]
    #告警or恢复
    for origina in originallist:

        if origina['triggervalue']=='0' :            
            normallist.append(origina)
            if origina['triggerkey'] not in triggerkeylist:
                triggerkeylist.append(origina['triggerkey'])
        else :
            Unknown.append(origina)
    for triggerkey in triggerkeylist:
        for normal in normallist:
            if normal['triggerkey']==triggerkey:
                sorts.append(normal)
	if len(sorts)>=2:
            alarminfo.append(sorts)
	else:
	    normallist1.append(sorts)
        sorts=[]
    for normal in normallist1:
	if normal[0]['ipaddress'] not in hostlist:
	    hostlist.append(normal[0]['ipaddress'])
    for host in hostlist:
        for normal in normallist1:
            if normal[0]['ipaddress']==host:
                sorts.append(normal[0])
        alarminfo.append(sorts)
        sorts=[]    	
    #print alarminfo
    return alarminfo

#告警压缩
def compressproblem(alarminfo):
    currenttime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
    messagelist=[]
    for info in alarminfo:
        hostlist=''
        hostgroup=''
	triggernamelist=''
        infonum=len(info)
        for host in info:
            triggername=host['triggername']
	    itemvalue=host['itemvalue']
	    ipaddr=host['ipaddress']
	    triggeritems=host['triggeritems']
	    triggernseverity=host['triggernseverity']
            hostinfo=host['hostname']+':'+host['ipaddress']+'\n'
            if host['hostgroup'] not in hostgroup:
                hostgroup+=host['hostgroup']+'\n'
	    if host['hostname'] not in hostlist:
		hostlist+=host['hostname']+',    '
	    if host['triggername'] not in triggernamelist:
		triggernamelist+=host['triggername']+'\n'
            #hostlist+=hostinfo
        if infonum >= 2 and infonum <= 6:        
            message='【'+revel[str(triggernseverity)]+'】'+'\n告警数量:  '+str(infonum)+'项\n'+hostlist+'\n相关项目:  \n'+triggernamelist+'\n'+'分析时间:  '+currenttime
            messagelist.append(message)
        elif infonum > 6:
            message='【'+revel[str(triggernseverity)]+'】'+'\n当前存在大量相同告警项,可能发生网络故障!\n详情请咨询运维人员！\n'+'告警主机:  '+str(infonum)+'台\n'+'告警项目:  '+triggername+'\n'+'分析时间: '+currenttime
            messagelist.append(message)
	else:
	    message='【'+revel[str(triggernseverity)]+'】'+'\n告警主题:  '+triggername+'\n告警项目: '+ triggeritems +'\n告警主机:  '+ipaddr+'\n当前值:  '+itemvalue+'\n分析时间:  '+currenttime
	    messagelist.append(message)
    return messagelist


#恢复压缩
def compressnormal(alarminfo):
    currenttime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
    messagelist=[]
    for info in alarminfo:
        hostlist=''
        hostgroup=''
	triggernamelist=''
        infonum=len(info)
        for host in info:
            triggername=host['triggername']
	    itemvalue=host['itemvalue']
	    ipaddr=host['ipaddress']
	    triggeritems=host['triggeritems']
	    triggernseverity=host['triggernseverity']
            hostinfo=host['hostname']+':'+host['ipaddress']+'\n'
            if host['hostgroup'] not in hostgroup:
                hostgroup+=host['hostgroup']+'\n'
            if host['hostname'] not in hostlist:
		hostlist+=host['hostname']+',    '
	    if host['triggername'] not in triggernamelist:
		triggernamelist+=host['triggername']+'\n'
        if infonum >= 2 and infonum <= 6:        
            message='恢复◕‿◕\n'+'恢复告警:  '+str(infonum)+'项\n'+hostlist+'\n相关项目:  \n'+triggernamelist+'\n告警等级:  '+revel[str(triggernseverity)]+'\n'+'分析时间:  '+currenttime
            messagelist.append(message)
        elif infonum > 6:
            message='恢复◕‿◕\n'+'大量告警已经恢复!\n详情请咨询运维人员！\n'+'恢复告警: '+str(infonum)+'项\n'+'恢复项目:  '+triggername+'\n'+'分析时间:  '+currenttime
            messagelist.append(message)
	else:
	    message='恢复*^_^*\n'+'恢复主题:  '+triggername+'\n告警等级:  '+revel[str(triggernseverity)]+'\n恢复主机:  '+ipaddr+'\n当前值:  '+itemvalue+'\n分析时间:  '+currenttime
	    messagelist.append(message)
    return messagelist
