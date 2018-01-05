#!/usr/bin/env python
#coding:utf-8
import MySQLdb
import redis
import sys
import os
from dbread import *
from operation import *
from weixin import *
import datetime,time
real={"22":"Admin","13":"深圳桌面组","17":"北京桌面组","16":"厦门桌面组","12":"电话组","23":"crm运维","24":"互联网运维","14":"互联网业务组","11":"网络组","25":"coreuser","26":"大数据平台","27":"北京机房运维","29":"互联网数据库","30":"crm1.0业务","31":"crm2.0业务","32":"coreuser业务","33":"大数据业务"}
sendtime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
#accesstoken=gettoken()
def process_exists():
    p_checkresp = os.popen('ps aux |grep allpolice|grep -v grep ').readlines()
    print len(p_checkresp)
    return len(p_checkresp)
##企业微信告警
def Send_alarm(actionid,users):
    r = redis.StrictRedis(host='127.0.0.1',port=6379)
    subjectlist = r.lrange(actionid,0,-1)
    action=real[str(actionid)]
    for i in subjectlist:
        r.lrem(actionid,0,i)
    originallist=[]
    for subject in subjectlist:
        a=alerts_eventid(str(actionid),subject)
        originallist.append(a)
    problem=mergeproblem(originallist)
    normal=mergenormal(originallist)
    messagelist=compressproblem(problem)
    if len(messagelist) != 0:
        for content in messagelist:
            print sendtime
            content='"' + str(content) + '"' 
	    os.system("echo '%s\n%s %s %s' >>/data/police/report.log" % (sendtime,actionid,action,content))
            for user in users:
                os.system("/data/police/weixin.py %s %s" % (user,content))
		os.system("echo '%s\n%s %s%s' >>/data/police/wx.log" % (sendtime,actionid,user,content))

    messagelist=compressnormal(normal)
    if len(messagelist) != 0:
       for content in messagelist:
           print sendtime
           content='"' + str(content) + '"' 
	   os.system("echo '%s\n%s %s %s' >>/data/police/report.log" % (sendtime,actionid,action,content))
           for user in users:
               os.system("/data/police/weixin.py %s %s" % (user,content))    
	       os.system("echo '%s\n%s %s%s' >>/data/police/wx.log" % (sendtime,actionid,user,content))
##邮件告警
def Send_mail(actionid,users):
    r = redis.StrictRedis(host='127.0.0.1',port=6379)
    subjectlist = r.lrange(actionid,0,-1)
    action=real[str(actionid)]
    for i in subjectlist:
        r.lrem(actionid,0,i)
    originallist=[]
    for subject in subjectlist:
        a=alerts_eventid(str(actionid),subject)
        originallist.append(a)
    problem=mergeproblem(originallist)
    normal=mergenormal(originallist)
    messagelist=compressproblem(problem)
    if len(messagelist) != 0:
        for content in messagelist:
            print sendtime
	    content=content.replace('\n','<br>')
            content='"' + str(content) + '"'
	    os.system("echo '%s\n%s %s %s' >>/data/police/report.log" % (sendtime,actionid,action,content))
            for user in users:
                os.system("/usr/local/zabbix-3.2.6/share/zabbix/alertscripts/sendEmail.sh %s '告警' %s" % (user,content))
                os.system("echo '%s\n%s %s%s' >>/data/police/wx.log" % (sendtime,actionid,user,content))

    messagelist=compressnormal(normal)
    if len(messagelist) != 0:
       for content in messagelist:
           print sendtime
	   content=content.replace('\n','<br>')
           content='"' + str(content) + '"'
	   os.system("echo '%s\n%s %s %s' >>/data/police/report.log" % (sendtime,actionid,action,content))
           for user in users:
               os.system("/usr/local/zabbix-3.2.6/share/zabbix/alertscripts/sendEmail.sh %s '恢复' %s" % (user,content))
               os.system("echo '%s\n%s %s%s' >>/data/police/wx.log" % (sendtime,actionid,user,content))


if __name__ == "__main__":
    if process_exists() <= 5:
        ###############Admin###################
    	Send_alarm(22,['18681440207','18819475152'])

   	##############深圳桌面组###############
    	Send_alarm(13,['15007554919','13760190969','15012989710','18124768491','18926774713','13823103713'])

    	##############北京桌面组###############
    	Send_alarm(17,['18001349968','13466635337','13810128662'])

    	##############厦门桌面组###############
    	Send_alarm(16,['18057126775','18950080260','15606908689'])

    	##############电话组###################
    	Send_alarm(12,['15123864695','18028702203','13322996043','18682248579'])

    	##############crm_yw###################
    	Send_alarm(23,['14718090324'])

    	##############互联网运维###############
    	Send_alarm(24,['18126019951'])

	##############互联网业务组#############
    	Send_alarm(14,['13439474968','18589057798','13189788806','18664922332','15902090811','15622238753'])

    	##############网络组###################
    	Send_alarm(11,['18191148505','13163743663'])

	##############coreuser#################
	Send_mail(25,['xiaofeng.chen@zhenai.com'])

	###############大数据平台##############
	Send_alarm(26,['13825255150'])

	###############北京机房运维############
	Send_alarm(27,['18001349968','13466635337'])

	###############互联网数据库############
	Send_mail(29,["qiang.li5@zhenai.com","hualong.zheng@zhenai.com","jinbin.he@zhenai.com","wanliang.peng@zhenai.com","xin.zhang2@zhenai.com","tingyi.wan@zhenai.com"])

	###############crm1.0 业务#############
	Send_alarm(30,['13723799372','18824864771','13580541216'])
	
	##############crm2.0 业务##############
	Send_alarm(31,['18681522736'])

	##############coreuser 业务############
	Send_alarm(32,['13265881706','18201406416'])

	##############大数据业务###############
	Send_alarm(33,['15019275604','18025312386','18824116495'])

    else:
	sys.exit(0)
