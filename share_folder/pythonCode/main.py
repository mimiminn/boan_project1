import pymysql
import user
import admin
import hashlib

while True:
    account = input("ID: ")
    password = input("Password: ")
    password = hashlib.sha256(password.encode())
    password = password.hexdigest()

    if account == "" or password == "":
        print("입력을 완료해주세요")
        continue

    conn = pymysql.connect(host='172.18.0.2', user='root', password='qwer', db='Log', charset='utf8')
    cursor = conn.cursor()

    sql = "SELECT * FROM User WHERE id = %s"

    cursor.execute(sql, (account))
    result = cursor.fetchall()
    sql_pwd = result[0][1]

    if len(result) == 0:
        print("존재하지 않는 사용자입니다")
    elif sql_pwd != password:    # 비교시에 해시 추가 필요
        print("비밀번호가 올바르지 않습니다")
    else:
        if result[0][3] == 0:  # 관리자 객체 생성 후 선택 번호 부여
            while True:
                print("관리자 입니다")
                print("1: 로그 보기")
                print("2: 사용자 추가하기")
                print("3: 사용자 제거하기")
                print("4: 사용자 리스트 확인")
                print("5: 다른 계정으로 로그인하기")
                print("6: 창을 종료하기")
                num = int(input("원하는 목록의 번호를 선택해주세요.... "))
                if num == 5:
                    print("로그아웃되었습니다.")
                    break
                #만약 num이 다른값이라면
                if num == 6:
                    print("===EXIT===")
                    exit()
                Admin = admin.admin()
                Admin.choice(num)

        elif result[0][3] == 1:  # 사용자 객체 생성 후 선택 번호 부여
            while True :
                print("사용자 입니다")
                print("1: 로그 보기")
                print("2: 다른 계정으로 로그인하기")
                print("3: 창을 종료하기")

                num = int(input("원하는 목록의 번호를 선택해주세요.... "))
                if num == 2:
                    print("로그아웃되었습니다.")
                    break
                if num == 3:
                    print("===EXIT===")
                    exit()
                User = user.user()
                User.choice(num)

        else:
            print("올바른 사용자가 아닙니다.")
            continue

    conn.commit()
    conn.close()
