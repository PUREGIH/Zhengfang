import joblib
import requests
from zf_handle import zf_login, zf_pj, zf_cj, getInfor, HEADERS, base_url, xh, password

# 初始化会话
session_filename = 'session.pkl'

saved_student_name = ''  # 初始学生姓名

model = joblib.load('./model/clf1.model')  # 加载模型


def save_login_info(student_name):
    data = {
        'student_name': student_name
    }
    joblib.dump(data, 'login_info.pkl')


def load_login_info():
    try:
        data = joblib.load('login_info.pkl')
        return data.get('student_name')
    except FileNotFoundError:
        return None


def get_login_status(s):
    url = f'{base_url}/xs_main.aspx?xh={xh}'
    headers = HEADERS.copy()
    response = s.get(url, headers=headers)
    content = response.content.decode('utf-8')

    # 获取学生基本信息
    student = getInfor(content, '//*[@id="xhxm"]/text()')
    return student


def create_session():
    global saved_student_name
    session = requests.session()
    saved_student_name = zf_login(session, xh, password, model)
    save_login_info(saved_student_name)
    with open(session_filename, 'wb') as f:
        joblib.dump(session, f)
    return session


def get_session(session=None):
    global saved_student_name
    saved_student_name = load_login_info()
    try:
        with open(session_filename, 'rb') as f:
            session = joblib.load(f)
    except FileNotFoundError:
        session = None

    if not session or not get_login_status(session):
        session = create_session()

    return session


def main():
    # 尝试从保存的文件中加载登录信息
    session = get_session()

    zf_cj(session, xh, saved_student_name)
    zf_pj(session, xh, saved_student_name)


if __name__ == "__main__":
    main()
