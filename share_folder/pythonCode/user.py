import pymysql
import auto

conn = pymysql.connect(host='172.18.0.2', user='root', password='qwer', db='Log', charset='utf8')
curDict = conn.cursor(pymysql.cursors.DictCursor)

class user:
    def choice(self, num):
        if num == 1:  # 선택지가 1번일 때
            self.showLog()
            return

    def showLog(self):  # db에서 파일 읽어오기
        print("로그를 불러옵니다.")
        while True:
            Auto = auto.auto()
            Auto.accesslogload()
            sql_loadLog = "SELECT DISTINCT access.ip_addr, access.time, access.access_point, access.httpcode, error.error_code FROM AccessLog access LEFT JOIN ErrorLog error ON (access.ip_addr = error.ip_addr) AND (access.time = error.time);"
            curDict.execute(sql_loadLog)
            joinL = curDict.fetchall()
            print("||",str("NO").center(4),"|",str("IP").center(20),"|",str("Access Time").center(24),"|",str("Access Point").center(30),"|",str("HTTP Code").center(12),"|",str("Error Code").center(12),"||")
            joNo = 1
            for log in joinL :
                print("||",str(joNo).center(4),"|",str(log['ip_addr']).center(20),"|",str(log['time']).center(24),"|",str(log['access_point']).center(30),"|",str(log['httpcode']).center(12),"|",str(log['error_code']).center(12),"||")
                joNo += 1
            print("\n로그 분석을 완료하였습니다.")
            do = self.back()

            if do == 0 :
                return

    def back(self):
        backChoice = input("이전 화면으로 돌아가시려면 아무 글자를 눌러주세요...")
        if backChoice != "":
            print("화면을 이동합니다.")
            return 0
        else:
            return 1
