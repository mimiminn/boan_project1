import pymysql
import datetime

conn = pymysql.connect(host='172.18.0.2', user='root', password='qwer', db='Log', charset='utf8')
cursor = conn.cursor()

class auto:
    def accesslogload(self):
        testFile = open('/var/lib/python/log/access.log','r')
        #파일 읽어옴
        while True:
            readFile = testFile.readline() #access file log readline으로 읽어오기
            if not readFile:
                break
            readFile_list=readFile.split()
            readFile_list_03=str(readFile_list[3])
            readFile_list_03=readFile_list_03[1:]
            format = '%d/%b/%Y:%H:%M:%S'
            time_accesslog = datetime.datetime.strptime(readFile_list_03, format)
            sql_a = "INSERT Into AccessLog (ip_addr, access_point, time, httpcode) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql_a,(readFile_list[0], readFile_list[21], readFile_list_03, readFile_list[8]))
        conn.commit()
        testFile.close()
        #테스트파일닫음




        #에러 로그 파일 읽어옴
        Errorlogfile = open('/var/lib/python/log/error.log','r')
        while True:
            readErrorFile = Errorlogfile.readline() #error log file readline으로 읽어옴
            if not readErrorFile:
                break
            readErrorFile_list = readErrorFile.split()
            #에러로그 시간
            errortime = str(readErrorFile_list[0]+" "+readErrorFile_list[1])
            format = '%Y/%m/%d %H:%M:%S'
            time_errorlog = datetime.datetime.strptime(errortime, format)
            time_errlog_final = time_errorlog.strftime('%Y-%m-%d %H:%M:%S')
            #에러로그 ip
            client=""
            for i in range(len(readErrorFile_list)):
                if readErrorFile_list[i] == 'client:':
                    client = readErrorFile_list[i+1]
            client = client[:-1]
            #http에러코드
            httpercd=""
            for i in range(len(readErrorFile_list)):
                if '(' in readErrorFile_list[i] and len(readErrorFile_list[i])<6:
                    httpercd = str(readErrorFile_list[i])
                    httpercd = httpercd[1:-1]
            sql_e = "INSERT Into ErrorLog (ip_addr, error_code, time) VALUES (%s, %s, %s)"
            cursor.execute(sql_e,(client, time_errlog_final, httpercd))
        conn.commit()
        Errorlogfile.close()
