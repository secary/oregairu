# -*- codeing = utf-8 -*-
# @Time : 2020/11/20 10:31
# @Author : secary
# @File : Yukikaze[cost calculator].py
# @Software : PyCharm


while 1:
    try:
        name = input("adeset name:")
        if name != 'q':
            num =int(input("number:"))
            cost = []
            total_cost = 0
            for i in range (0,num):
                cost_i = float(input("cost %s:"%str(i+1)))
                cost.append(cost_i)
                total_cost += cost_i
                i += 1
            print("%s's total cost: %s"%(name,total_cost))
            print("="*50)
        else:
            break
    except Exception as result:
        print("ERROR:%s" % result)
        print("=" * 50)
