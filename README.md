# python_backend_study

1. 윈도우 운영체제를 사용하고있음. Microsoft Store에서 우분투 설치 
2.	우분투용 미니콘다 설치  
      - 미니콘다 다운  
      $ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh  
   
      - 미니콘다 설치  
      $ bash Miniconda3-latest-Linux-x86_64.sh  

3.	파이썬 가상환경 생성  
$ conda create –-name api python=3.7  
$ conda activate api  

4.	Flask(API 프레임워크) 설치  
$ pip install flask    
     - api라는 가상환경내에 설치했으므로 api환경을 비활성화 시키고 하면 실행 안됌.  
 
5.	API 코드가 위치할 디렉토리 생성! home 디렉토리 안에 Projects생성하고 그 안에 api 생성  
$ mkdir ~/Projects (~는 home 디렉토리임.)  
$ cd Projects/ (Projects 디렉토리 안으로 이동)  
$ mkdir api (api 디렉토리 생성.)  

6.	api 디렉토리 안에 app.py 파일 생성  
$ vim app.py  

7.	첫 API 개발: ping 엔드포인트 구현하기.  

    - app.py 파일내용:    
``` 
from flask import Flask (Flask 클래스 임포트)  
app=Flask(__name__) (Flask 클래스를 객체화 하여 app이라는 변수에 저장, 이 app변수가 API 애플리케이션이다.)  
@app.route(“/ping”,methods=[‘GET’]) (Flask의 route 데코레이터로 엔드포인트 등록, 고유 주소는 “ping”이며 HTTP 메소드는 GET으로 설정하여 등록함.)  
def ping():
	   return “pong”	(”pong”스트링을 리턴하는 ping 함수.)  
```  

    - 파일 저장 후 나가기: Esc , Shift+ZZ or Esc, :wq!   
    - 파일 들어가기 $ vi app.py  

8.	API 실행하기  
    - FLASK_ENV를 development로 정해놓으면 코드가 수정될때마다 FLASK가 자동으로 재실행되어 수정된 코드가 반영되도록 해줌.(=Debug mode: on)
$ FLASK_ENV=development FKAS_APP=app.py flask run  

9.	HTTP 요청보내기.  
    - httpie 툴 설치  
$ sudo apt-get update  
$ sudo apt install httpie  

    - app.py 실행시키기  
$ cd Projects/api #app.py 파일이 있는 곳에서 실행시켜야하기 때문임.  
$ FLASK_ENV=development FKAS_APP=app.py flask run  
 
	
    - API가 실행되고 있는 상태에서 다른 터미널을 열고, http 요청 보내기  
$ http -v GET localhost:5000/ping  

10.	mysql데이터베이스 설치  
$ sudo apt update  
$ sudo apt install mysql-server  

11.	mysql 접속  
$ sudo service mysql restart  
$ sudo mysql  

12.	miniter라는 데이터 베이스 생성 후 사용  
```
mysql> 	CREATE DATABASE miniter;
mysql> USE miniter
mysql> 
CREATE TABLE users(
	    id INT NOT NULL AUTO_INCREMENT,
	    name VARCHAR(255) NOT NULL,
	    email VARCHAR(255) NOT NULL,
	    hashed_password VARCHAR(255) NOT NULL,
	    profile VARCHAR(2000) NOT NULL,
	    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, 
	    updated_at TIMESTAMP NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP, 
	    PRIMARY KEY (id), 
	    UNIQUE KEY email (email)
	);
	

	CREATE TABLE users_follow_list(
	    user_id INT NOT NULL,
	    follow_user_id INT NOT NULL,
	    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, 
	    PRIMARY KEY (user_id, follow_user_id),
	    CONSTRAINT users_follow_list_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id), 
	    CONSTRAINT users_follow_list_follow_user_id_fkey FOREIGN KEY (follow_user_id) REFERENCES users(id)
	);
	

	CREATE TABLE tweets(
	    id INT NOT NULL AUTO_INCREMENT,
	    user_id INT NOT NULL,
	    tweet VARCHAR(300) NOT NULL,
	    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (id),
	    CONSTRAINT tweets_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id)
	);
```

13.	파이썬 코드와 데이터베이스를 연결시키기.  
    - SQLALCHEMY 라이브러리 설치  
$ pip install sqlalchemy  
    - mysql용 DBAPI설치 (데이터베이스를 사용하기 위한 api)  
$ pip install mysql-connector-python  
 
14.	app.py, config.py를 수정한다  
-참고: https://github.com/rampart81/python-backend-book/tree/master/chapter6  

15.	flask를 실행시키고 http 요청을 보낸다.  

에러: sqlalchemy.exc.ProgrammingError: (mysql.connector.errors.ProgrammingError) 1698 (28000): Access denied for user 'root'@'localhost'
(Background on this error at: http://sqlalche.me/e/f405)  

<해결법>  
+	root 사용자의 인증모드를 비밀번호를 사용해서 바꾼다.  
    mysql> ALTER USER ‘root’@’localhost’ IDENTIFIED WITH mysql_native_password BY ‘내가정하는비밀번호’;  
    mysql>flush privileges; #변경된 설정이 바로 반영되도록 함.  
    mysql>SELECT user,plugin,host FROM mysql.user; (root plugin이 auth_socket이 아니라 mysql_native_password로 바뀜. )  
 

+ config.py파일의 비밀번호를 root사용자에서 설정한 비밀번호로 수정한다.     
>	회원가입을 하고 터미널을 재생성하여 트윗을 보내도 데이터가 보존되어있어서 가능하다.  
 

16.	인증 엔드포인트를 구현해보자. 데이터 베이스 암호화!  
$pip install bcrypt #bcrypt 암호 알고리즘  
$pip install PyJWT #jwt(json web tokens):json데이터를 token으로 변환하는 방식  

17.	미니터API 코드  
* app.py, config.py 수정  

18.	샘플 프론트엔드 깃 클론!  
$ pip install flask-cors 명령어로 api url도메인 주소와 frontend 도메인 주소가 달라서 생기는 문제를 해결해준다. (->sign-up에서 login화면으로 넘어감.)  

- app.py 코드 수정 (create_app함수에 CORS(app)추가)  
- config.py 코드수정(JWT_SECRET_KEY=’SOME_SUPER_SECRET_KEY’ 추가)  

* 오류:  
![image](https://user-images.githubusercontent.com/44723287/72344368-64e7ae00-3714-11ea-8b13-2a7bb85f3ef8.png)
 
<해결법>  
Jwt 유효기간인 ‘exp’를   
‘exp’:datetime.now()+timedelta(seconds=60*60*24) 로 바꿔준다.   

* app.py 에서 PermissionError: [Errno 13] Permission denied: 오류가 발생했다.  
sudo권한으로만 열려서  
$ ls -al 명령어로 파일 정보를 확인하고 오류가 없는 config.py파일과 동일한 권한으로 바꾸어주었다.   
$ chmod 666 app.py (r=4,w=2, x=1 처음 -제외하고 세자리씩 끊어서 읽음)  
	

19.	테스트 피라미드!

![image](https://user-images.githubusercontent.com/44723287/72343632-ab3c0d80-3712-11ea-8e36-c69e1082157c.png)

![image](https://user-images.githubusercontent.com/44723287/72343702-d9b9e880-3712-11ea-87ff-6d655039f749.png)


20.	프론트엔드 샘플 사용하여 UI test  
-	miniter데이터베이스에 이미 가입되어있는 Lee mina !  
![image](https://user-images.githubusercontent.com/44723287/72343781-04a43c80-3713-11ea-94c8-f586d86a1e0f.png)
![image](https://user-images.githubusercontent.com/44723287/72343793-0ec63b00-3713-11ea-9d11-14c67ef4aff9.png)
![image](https://user-images.githubusercontent.com/44723287/72343823-21d90b00-3713-11ea-826c-af87e2f0e04a.png)
 
  
21.	Unit test 구현하는데 쓰는 모듈 설치  
$ pip install pytest  
-	pytest는 파일이나 함수이름 앞부분에 test_ 라고 되어있는 것만 unit test라고 인식하고 실행시킨다.  
$ pytest 명령어로 unit test를 실행할 수 있다.  
  

22.	일부 함수 unit test!  
-miniter_test 데이터베이스 만들기!(앞의 miniter데이터베이스와 완전 동일)  
-config.py파일에 test_db(db와 동일), test_config(DB URL, JWT_SECRET_KEY를 딕셔너리 형태로) 추가  
-pytest를 위한 test_endpoints.py 파일 추가. pytest.fixure 데코레이터를 만들고 test_ping, test_tweet(sign-up,login,tweet,timeline) 함수에 대해서 status_code==200으로 테스트함!  

### 참고
깔끔한 파이썬 탄탄한 백엔드    
https://github.com/rampart81/python-backend-book/   
https://github.com/Yeri-Kim/python-tutorial-frontend   
출처: https://wookkk.tistory.com/entry/우분투-미니콘다-설치 [woo격다짐]  
출처: https://conory.com/blog/19194  


