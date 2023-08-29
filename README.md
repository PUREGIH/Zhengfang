![仅适用新版方正教务管理后台](https://github.com/PUREGIH/Zhengfang/blob/main/images/UI.jpeg?raw=true)
# **新版正方教务系统API**

## 简介
本项目使用了一个基于深度学习的模型来自动识别正方教务系统的验证码。该模型是用Python的sklearn库中的MLPClassifier类来构建和训练的。模型的输入是一个由验证码图片经过预处理后得到的一维向量，输出是一个四位数的字符串，表示验证码的内容。模型使用了1W张图片验证码作为训练集，其中90%用于训练，10%用于验证。模型的准确率在测试集上达到了95.7%。为了使用该模型，您需要先下载clf1.model文件，并放置在/model目录下

- 其他说明：这个项目还在开发中，可能存在一些bug和不完善的地方。欢迎提出建议和反馈。

## 已实现

> ✅ 自动识别验证码登录
> 
> ✅ 导出所有历史成绩到Excel表格文件

## 待实现
> ⬛ 一键评教
> 
> ⬛ 课表通知

## 安装
`pip install requirements.txt`

## 使用
要使用这个项目，您需要先[点击此处](https://ali.ma.softrib.xyz/d/%E6%9C%AC%E5%9C%B0/fangzheng_model/clf1.model?sign=L_y9IykXQ6An8Q8577czD3E7sbnChDlP_pQNGcwRIic=:0)下载模型文件`clf1.model`最后放到`/model`目录下，然后修改`config.ini`文件，填写您的学号、密码、学校等信息。然后，您可以运行`main.py`来启动程序。

## 贡献
如果您对这个项目感兴趣，欢迎您参与贡献。您可以通过以下方式来贡献

- 提交问题或建议
- 修复bug或增加新功能
- 改进文档或注释
