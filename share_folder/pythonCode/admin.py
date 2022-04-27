import pymysql
import auto
import hashlib

conn = pymysql.connect(host='172.18.0.2', user='root', password='qwer', db='Log', charset='utf8')
cursor = conn.cursor()
curDict = conn.cursor(pymysql.cursors.DictCursor)

class admin:
    def choice(self, num):
        if num == 1:
            self.showLog()
            return
        elif num == 2:
            self.createUser()
            return
        elif num == 3:
            self.deleteUser()
            return
        elif num == 4:
            self.showUser()
            return

    # 1,2,3,4 선택 후 결과값을 보여주고 이후 특정 버튼 / 숫자 등을 누르면 선택지가 있는 곳으로 이동 -> back 활용
    def showLog(self):  # 로그 보여주기 -> /var/lib/python/log 에 있는 파일불러오고 가공
        print("로그를 불러옵니다.")
        while True:
            Auto = auto.auto()
            Auto.accesslogload()
            sql_loadLog = "SELECT DISTINCT access.ip_addr, access.time, access.access_point, access.httpcode, error.error_code FROM AccessLog access LEFT JOIN ErrorLog error ON (access.ip_addr = error.ip_addr) AND (access.time = error.time);"
            curDict.execute(sql_loadLog)
            joinL = curDict.fetchall()
            print("||",str("NO").center(4),"|",str("IP").center(20),"|",str("Access Time").center(24),"|",str("Access Point").center(30),"|",str("HTTP Code").center(12),"|",str("Error Code").center(12),"||")
            print("")
            joNo = 1
            for log in joinL :
                print("||",str(joNo).center(4),"|",str(log['ip_addr']).center(20),"|",str(log['time']).center(24),"|",str(log['access_point']).center(30),"|",str(log['httpcode']).center(12),"|",str(log['error_code']).center(12),"||")
                joNo += 1
            print("\n로그 분석을 완료하였습니다.")
            do = self.back()

            if do == 0 :
                return


    def createUser(self):  # sql문, Insert로 사용자 생성
        while True:
            print("사용자 생성을 위해 아래의 내용을 입력해주세요.")
            addID = str(input("ID : "))
            addPW = str(input("Password : "))
            addNA = str(input("Name : "))
            addPRI = str(input("UserLevel('0' - admin | '1' - user) : "))
            if addID == None or addPW == None or addNA == None:
                print("잘못된 입력입니다. 처음부터 다시 입력해주세요.")
                continue
            #id중복확인
            real = self.findUser(addID)
            if len(real) != 0:
                print("이미 사용중인 아이디입니다. 다른 아이디를 입력해주세요.")
                continue
            if addPRI == "0":
                sql_insertAdmin = "INSERT INTO User (id,pwd,name,privilege) VALUES (%s,%s,%s,0)"
                password = addPW
                password=hashlib.sha256(password.encode())
                password = password.hexdigest()
                cursor.execute(sql_insertAdmin,(addID,password,addNA))
                conn.commit()
                print("관리자 \"",addID,"\"가 등록되었습니다.")
                self.back()
                return  
            if addPRI == "1":
                sql_insertUser = "INSERT INTO User (id,pwd,name) VALUES (%s,%s,%s)"
                password = addPW
                password=hashlib.sha256(password.encode())
                password = password.hexdigest()
                cursor.execute(sql_insertUser,(addID,password,addNA))
                conn.commit()
                print("사용자 \"",addID,"\"가 등록되었습니다.")
                self.back()
                return  
            print("잘못된 입력입니다. 처음부터 다시 입력해주세요.")


    def deleteUser(self):  # sql문, Delete로 사용자 제거성
        print("삭제를 원하시는 사용자의 ID를 입력해주세요.")
        delID = str(input("ID : "))
        #if 만약 계정의 id와 불러온 fetchall의 결과값과 일치한다면 근데 fetchall 괜찮은건가...;;
        #맞는 계정이라면
        ansRm = str(input("정말로 이 계정을 삭제하시겠습니까? [ Y / N ] "))
        while True:
            if ansRm == "Y" or ansRm == "y" :
                sql_deleteUser = "DELETE FROM User WHERE id = %s"
                cursor.execute(sql_deleteUser,(delID))
                conn.commit()
                print("사용자 \"",delID,"\"가 제거되었습니다.")
                self.back()
                return
            elif ansRm == "N" or ansRm == "n" :
                print("메인화면으로 이동합니다.")
                return
            else:
                ansRm = str(input("잘못된 입력입니다. 정말로 삭제하시겠습니까? [ Y / N ] "))
                continue
        #맞지않는 계정이라면 따라서 없는 계정이라면ㅑ
        #없는 계정입니다 print하고 어디로 돌아갈지 고민해보기


    def showUser(self):  # sql문, Select로 사용자 보여주기
        print("현재 등록되어있는 사용자 목록을 출력합니다.")
        sql_selectUser = "SELECT id, name FROM User"
        curDict.execute(sql_selectUser)
        list = curDict.fetchall()
        print("||",str("NO").center(4),"|",str("ID").center(30),"|",str("NAME").center(30),"||")
        print("")
        inNo = 1
        for data in list :
            print("||",str(inNo).center(4),"|",str(data['id']).center(30),"|",str(data['name']).center(30),"||")
            inNo += 1
        print("")
        self.back()
        return
        #만약 넣을 수 있다면
        #SELECT id, name FROM User id ASC / DESC (오름차순 / 내림차순정렬)
        #SELECT id, name FROM User WHERE privilege = 0 / 1 (관리자계정만 추출 / 사용자계정만 추출)


    def back(self):  # 선택지 나오는 부분으로 이동
        backChoice = input("이전 화면으로 돌아가시려면 아무 글자를 눌러주세요...")
        if backChoice != "" :
            print("화면을 이동합니다.")
            return 0
        else:
            return 1

    
    def findUser(self,addID):
        sql_findUser = "SELECT id FROM User WHERE id = %s"
        cursor.execute(sql_findUser, (addID))
        found = cursor.fetchall()
        return found
