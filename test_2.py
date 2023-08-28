import os
import threading
import time

def main_menu():
    while True:
        os.system('cls')
        print("1. 菜单1")
        print("2. 菜单2")
        choice = input("请选择菜单（按q键退出）：")
        if choice == "q":
            break
        elif choice == "1":
            while True:
                os.system('cls')
                print("1. 子选项1")
                print("0. 返回主菜单")
                choice = input("请选择子选项：")
                if choice == "1":
                    t = threading.Thread(target=get_time)
                    t.start()
                    try:
                        while True:
                            time.sleep(1)
                    except KeyboardInterrupt:
                        print("程序被强制结束，退出程序")
                elif choice == "0":
                    break
                else:
                    try:
                        raise ValueError("无效选项，请重新输入！")
                    except ValueError as e:
                        print(e)
                        time.sleep(2)
        elif choice == "2":
            while True:
                os.system('cls')
                print("1. 子选项1")
                print("0. 返回主菜单")
                choice = input("请选择子选项：")
                if choice == "1":
                    # 子选项1的代码
                    pass
                elif choice == "0":
                    break
                else:
                    try:
                        raise ValueError("无效选项，请重新输入！")
                    except ValueError as e:
                        print(e)
                        time.sleep(2)
        else:
            try:
                raise ValueError("无效选项，请重新输入！")
            except ValueError as e:
                print(e)
                time.sleep(2)
            continue


def get_time():
    for i in range(10):
        print("北京时间：", time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        time.sleep(1)

if __name__ == "__main__":
    os.system('cls')
    main_menu()
