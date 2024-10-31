from flask import Flask, jsonify  # Flask와 JSON 응답을 위한 모듈 임포트
import psycopg2  # PostgreSQL 데이터베이스 연결을 위한 모듈 임포트

app = Flask(__name__)  # Flask 애플리케이션 인스턴스 생성

# 데이터베이스 연결 설정
# TODO flask-dotenv 사용하여 암호화
conn = psycopg2.connect(
    database="postgres",  # 사용할 데이터베이스 이름
    user="postgres",      # 데이터베이스 사용자 이름
    password="1234"       # 데이터베이스 사용자 비밀번호
)
cur = conn.cursor()  # 커서 객체 생성

def db(men_sql, params):
    """
    데이터베이스 쿼리를 실행하고 결과를 반환하는 함수.
    
    :param men_sql: 실행할 SQL 쿼리 문자열
    :param params: 쿼리에 전달할 매개변수 튜플
    :return: 쿼리 결과를 딕셔너리의 리스트로 반환
    """
    global cur
    cur.execute(men_sql, params)  # 쿼리 실행
    columns = [desc[0] for desc in cur.description]  # 컬럼 이름 가져오기
    results = [dict(zip(columns, row)) for row in cur.fetchall()]  # 결과를 딕셔너리로 변환
    return results



@app.route("/", methods=['POST', 'GET'])
def home():
    return "home"

@app.route("/insert", methods=['POST', 'GET'])
def insert():
    """
    /insert 경로에 대한 요청을 처리하는 함수.
    
    :return: 사용자의 정보를 JSON 형식으로 반환하거나 오류 메시지 반환
    """
    userID = "admin001"  # 조회할 사용자 ID 설정
    try:
        # 쿼리 실행 및 결과 가져오기
        result = db("SELECT * FROM team1.t_user WHERE user_id = %s;", (userID,))
        
        '''
        # 동적 쿼리 생성 및 실행
            query = sql.SQL(
                "SELECT * FROM 
                {table} 
                WHERE user_id = %s AND auth_cd = %s").format(
                table=sql.Identifier('team1', 't_user')
            )
            result = db(query, (userID, userNm))
        '''

        # 결과를 JSON 형태로 변환하여 반환
        return jsonify(result)
    except Exception as e:
        return str(e), 500  # 오류 발생 시 오류 메시지와 상태 코드 반환

if __name__ == "__main__":
    app.run(port=5001, debug=True)  # 애플리케이션을 디버그 모드로 실행, #포트번호 8000으로 설정 기본 5000
'''
추후 DB 암호화
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{os.getenv('PG_USER')}:{os.getenv('PG_PW')}@{os.getenv('PG_HOST')}:{os.getenv('PG_PORT')}/{os.getenv('PG_DBNAME')}'
db = SQLAlchemy(app)
'''

## SQLAlchemy : JPA같은 느낌
## psycopg2 : 가장 자주사용된다고함

# 1. pyenv로 Python 버전 설정
# pyenv install 3.11.9
# pyenv local 3.11.9


# cd pythonWebBasic
# pip install pipenv 
# pipenv --python 3.11 Python 3.11로 가상 환경 생성:
# pipenv shell 가상환경 '활성화'
# pipenv --venv 가상환경 경로확인 후 인터프린터 설정 ctr + shift + p
# pipenv run python 명령어로 실행
# ex) pipenv run python src/config.py

# pipenv update -- gradle 새로고침과 같은 효과
# pipenv install -- 작업공간 이동시 패키지 재설치를위함

# exit 가상환경 비활성화

# git 설치후 시스템변수 Path에 C:\App\bin\PortableGit\2.47.0\bin 등록 되어야 git 명령어 사용가능