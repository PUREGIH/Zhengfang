import requests
from lxml import etree

import os

import joblib
from ProcessingImage import *


def get_captcha(n=200):
    s = requests.session()
    # 循环执行200次
    for i in range(n):
        # 访问网页，获取页面源代码
        url = "http://119.6.108.206:777/default2.aspx"
        response = s.get(url)
        selector = etree.HTML(response.content)

        # 获取SafeKey
        SafeKey = selector.xpath("//div[@class='jympic']/img/@src")[0]

        # 验证码url
        captcha_url = "http://119.6.108.206:777" + SafeKey

        captcha = s.get(captcha_url, stream=True).content
        # 保存验证码图片
        filename = f"./images/download/captcha_{i + 1}.jpg"
        try:
            with open(filename, "wb") as jpg:
                jpg.write(captcha)
        except IOError:
            print("IO Error\n")


def loadModel(filename):
    return joblib.load(filename)


# def evaluate_captcha(folder_path, rename=False):
#     model = loadModel('./model/clf1.model')  # 导入模型
#
#     correct_count = 0  # 记录正确预测的数量
#     total_count = 0  # 记录总的预测数量
#
#     for root, dirs, files in os.walk(folder_path):
#         for file in files:
#             name = file[:-4]
#             # 模型预测验证码
#             result_pred = []
#             captcha = Image.open(root + file)
#             new_img = SplitImage(GrayscaleAndBinarization(captcha))
#             for item in new_img:
#                 tmp = []
#                 img_after_split = item.resize((14, 27))
#                 tmp.append(featuretransfer(img_after_split))
#                 result_pred.append(model.predict(tmp)[0])
#             captcha_pred = ''.join(result_pred)
#             print('此次预测结果为：{}  '.format(captcha_pred), '  正确结果：{}'.format(name), sep='|')
#             total_count += 1
#             if captcha_pred == name:
#                 correct_count += 1
#
#     accuracy = correct_count / total_count
#     print('预测准确率为：{:.2%}'.format(accuracy))
#     return accuracy


# 加载模型
model = loadModel('./model/clf1.model')


def evaluate_captcha(folder_path, rename=False):
    correct_count = 0  # 记录正确预测的数量
    total_count = 0  # 记录总的预测数量

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            name = file[0:4]
            # 模型预测验证码
            result_pred = []
            captcha = Image.open(root + file)
            new_img = SplitImage(GrayscaleAndBinarization(captcha))
            for item in new_img:
                tmp = []
                img_after_split = item.resize((14, 27))
                tmp.append(featuretransfer(img_after_split))
                result_pred.append(model.predict(tmp)[0])
            captcha_pred = ''.join(result_pred)

            if rename:
                # 重命名文件
                new_file_name = captcha_pred + '.jpg'
                os.rename(os.path.join(root, file), os.path.join(root, new_file_name))

            else:
                total_count += 1
                if captcha_pred == name:
                    correct_count += 1
                print('此次预测结果为：{}  '.format(captcha_pred), '  正确结果：{}'.format(name), sep='|')

    if not rename:
        accuracy = correct_count / total_count
        print('预测准确率为：{:.2%}'.format(accuracy))
        return accuracy


if __name__ == '__main__':
    # get_captcha(500)
    evaluate_captcha('./images/test/')
    # 参数2：是否将预测验证码结果命名为新文件名，为假仅预测准确率。
