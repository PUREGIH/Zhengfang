import joblib
import requests
from config import Config
from zf_handle import zf_login, zf_pj, zf_cj

# 初始化会话
config = Config()
xh = str(config.getRaw('config', '学号'))
password = str(config.getRaw('config', '密码'))

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


def save_session(session, filename):
    with open(filename, 'wb') as f:
        joblib.dump(session, f)


def load_session(filename):
    try:
        with open(filename, 'rb') as f:
            return joblib.load(f)
    except FileNotFoundError:
        return None


def main():
    # 尝试从保存的文件中加载登录信息
    session_filename = 'session.pkl'
    saved_session = load_session(session_filename)

    saved_student_name = load_login_info()

    if saved_session:
        print('Using saved session.')
        s = saved_session
    else:
        s = requests.session()
        saved_student_name = zf_login(s, xh, password, model)
        save_login_info(saved_student_name)

    zf_cj(s, xh, saved_student_name)
    zf_pj(s, xh, saved_student_name)

    save_session(s, session_filename)


if __name__ == "__main__":
    main()
