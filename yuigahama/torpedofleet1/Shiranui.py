# -*- codeing = utf-8 -*-
# @Time : 2020/11/19 13:58
# @Author : secary
# @File : Shiranui.py
# @Software : PyCharm

'''
This is a calculator for exchange CNY to USD.
'''

Currency1 = input("Original Currency:")
Currency2 = input("Currency to Exchange:")
Exchange_rate = float(input("today's currency of %s to %s:"%(Currency1,Currency2)))
def Exchange(Currency_1):
    Currency_2 = float(Currency_1)/Exchange_rate
    print("%s:%s"%(Currency2,Currency_2))
print('-'*10,'%s To %s ,press Q to quit'%(Currency1,Currency2),'-'*10)
while 1:
    Currency_1 = input("%s:"%Currency1)
    if Currency_1 != 'q':
        Exchange(Currency_1)
        print('='*50)
    else:
        break
