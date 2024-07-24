# -*- codeing = utf-8 -*-
# @Time : 2020/11/23 18:36
# @Author : secary
# @File : Shimushu.py
# @Software : PyCharm
try:
    f = open('poet.txt','w')
    f.write('君不见，黄河之水天上来，奔流到海不复回。\n'
            '君不见，高堂明镜悲白发，朝如青丝暮成雪。\n'
            '人生得意须尽欢，莫使金樽空对月。\n'
            '天生我材必有用，千金散尽还复来。\n'
            '烹羊宰牛且为乐，会须一饮三百杯。\n'
            '岑夫子，丹丘生，将进酒，杯莫停.\n'
            '与君歌一曲，请君为我倾耳听。\n'
            '钟鼓馔玉不足贵，但愿长醉不复醒。\n'
            '古来圣贤皆寂寞，惟有饮者留其名。\n'
            '陈王昔时宴平乐，斗酒十千恣欢谑。\n'
            '主人何为言少钱，径须沽取对君酌。\n'
            '五花马，千金裘，呼儿将出换美酒，与尔同销万古愁。\n')
    f.close()

    def reading():
        f = open('poet.txt','r')
        text = f.readlines()
        return  text
        f.close()

    def writing():
        g = open('copy.txt','w')
        i = 0
        for i in range(len(reading())):
            g.write(reading()[i])
            i += 1
        g.close()
        g = open('copy.txt','r')
        copy = g.readlines()
        print('Copy Complete')
        return copy
        g.close()

except Exception as result:
    print("ERROR:%s"%result)
print(writing())
