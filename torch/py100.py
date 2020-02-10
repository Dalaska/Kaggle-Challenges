# learn python 
#  https://github.com/jackfrued/Python-100-Days/blob/master/Day01-15/01.%E5%88%9D%E8%AF%86Python.md

# math
a = 10
b = 3
if a and b:
    print(a//b)

print('%d + %d = %d'% (1,1,2))

# zen
a = [1,2,3,4]
print(a.pop())
print(a.remove(2))
print(a)

# 善于使用in运算符
x = 3
if x in a: 
    print('hi')

for x in a: # 迭代
    print(x)

# 用序列构建字符串
chars = ['m', 'e']
name = ''.join(chars)
print(name)  # jackfrued


chicks = ['xinyi', 'lihong', 'wenwen']
for index, name in enumerate(chicks):
	print(index, ':', name)

# gen list
dat = [3,4,5]
new_dat = [num*2 for num in dat if num<4.5]
print(new_dat)

# func
def factorial(num = 1):
    result = 1
    for n in range(1,num+1):
        result *= n
    return result

print(factorial(3))

# string
str1 = 'hola el mundo'
print(len(str1))
print(str1.upper())

# set
a = {1}
b ={1,3,4}
print(b-a)

# dict
items2 = dict(zip(['a', 'b', 'c'], '123'))

# doc
f = open('README.md','r',encoding = 'utf-8')
print(f.read())
f.close()

# input
a = float(input('a = '))
b = float(input('b = '))
c = float(input('c = '))
if a + b > c and a + c > b and b + c > a:
    print('周长: %f' % (a + b + c))

# 1 draw turtle
import turtle
turtle.pensize(4)
turtle.pencolor('red')
turtle.forward(100)
turtle.right(90)

