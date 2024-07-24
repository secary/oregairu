# -*- codeing = utf-8 -*-
# @Time : 2020/11/19 13:58
# @Author : secary
# @File : Yuudachi[ads calculator].py
# @Software : PyCharm

'''
This is a calculator which is for to sum several ad set costs and installs,
then calculate the cpi.
'''


while 1:
    try:
        name = input("ads set name:")
        if name != 'q':
            num =int(input("number:"))
            cost = []
            install = []
            adset = []
            total_cost = 0
            total_install = 0
            for i in range(0, num):
                cost_i = float(input("cost %s:" % str(i+1)))
                install_i = int(input("install %s:" % str(i+1)))
                cost.append(cost_i)
                install.append(install_i)
                adset.append([cost_i, install_i])
                total_cost += cost_i
                total_install += install_i
                if total_install != 0:
                    cpi = total_cost / total_install
                else:
                    cpi = "#N/A"
                    i += 1
            print("%s's total cost: %s" % (name,total_cost))
            print("total install: %s" % total_install)
            print("CPI:%s" % cpi)
            print('-'*50)
            for cost_install in adset:
                print(cost_install)
            print('=' * 50)
        else:
            break
    except Exception as result:
        print("ERROR:%s" % result)
        print('=' * 50)