豆瓣验证码识别

感觉关键在于图像预处理，处理得好，正确率就高，处理不好就低
最关键的是要根据豆瓣的图片特征来调整图像处理的各个参数,至于参数为什么那么设置,只能靠经验和试验了
目前正确率大概20%左右吧，将就用了 

加上百度OCR, 可以提高正确率，但是每天有调用限制

主程序在:
DouBanCaptcha.py