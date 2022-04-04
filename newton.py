import numpy as np
import pylab as pl


# ---------列出函數式---------
def ShowFunction( myList ):
    # 從最高次項數回去
    for index in range(len(myList)-1,-1,-1) :
        if(myList[index]!=0):
            if(myList[index]>0 and index!=len(myList)-1):
                print("+", end="")
            if(index==0):
                print(str(myList[index]), end="")
            else :
                print(str(myList[index])+"x^"+str(index), end="")
    print("\n")


# ---------存取係數---------
def MakeCoefficient(original, deg):    
    # find()  找不到會回傳-1
    coefficient=[]
    for i in range(deg+1):
        coefficient.append(0)

    for i in original :
        target = i.find('x')
        if(target!=-1):
            coefficient.pop(int(i[target+2:]))
            coefficient.insert(int(i[target+2:]), int(i[:target]))
        else:
            coefficient.pop(0)
            coefficient.insert(0, int(i))

    return coefficient



# ---------進行微分---------
def Differential(coefficient, deg):
    difCoefficient=[]
    for i in range(deg):
        difCoefficient.append(0)
    # 略過常數項，因為微分=0
    for i in range(1, len(coefficient)):
        if(coefficient[i]!=0):
            difCoefficient.pop(i-1)
            difCoefficient.insert(i-1, coefficient[i]*i)
    return difCoefficient


# ---------主函式開始---------
# 讀入方程式，依照'+'分開存到original，new為暫時存取 用以修復負號
f1 = input("請輸入函數： ")
deg = int(input("函數的最高次數為： "))
length = len(f1)
new = ""
start = 0
for i in range(1, length):
    if(f1[i]=='-'): # 將負號改為'+-'，方便於做字串拆分
        new = new + f1[start:i] + "+-"
        start=i+1   # start為'-'的下一個數
new = new + f1[start:i+1]

original = new.split('+')       # 以項次進行字串拆分
print(original)

coefficient = MakeCoefficient(original, deg)    # 把所有係數存到 coefficient
print(coefficient)

difCoefficient = Differential(coefficient, deg) # 把 coefficient 中的係數做微分，存在 difCoefficient 內
print(difCoefficient)

ShowFunction(difCoefficient)    # 輸出微分後的方程式


# ---------為畫圖的 (x, y) 做準備---------
coefficient_y = 0
coefficient_dify = 0


# ---------輸入各項繪圖參數---------
start_paint_form = float(input("輸入繪製圖形的 x 軸左端點："))
start_paint_to   = float(input("輸入繪製圖形的 x 軸右端點："))
x = np.linspace(start_paint_form, start_paint_to, 500)


# ---------建立 f(x) 及 f'(x) 兩多項式函數---------
for i in range(len(coefficient)):       # coefficient_y 即為 f(x)
    if(coefficient[i]!=0):
        coefficient_y += coefficient[i]*x**i

for i in range(len(difCoefficient)):    # coefficient_dify 即為 f'(x)
    if(difCoefficient[i]!=0):
        coefficient_dify += difCoefficient[i]*x**i


# ---------建立 f(x) 函數回傳值---------
def Value_coefficient_y( input_x ):
    value_of_y = 0.0
    for i in range(len(coefficient)):     
        if(coefficient[i]!=0):
            value_of_y += coefficient[i]*input_x**i
    return value_of_y


# ---------建立 f'(x) 函數回傳值---------
def Value_coefficient_dify( input_x ):
    value_of_dify = 0.0
    for i in range(len(difCoefficient)):   
        if(difCoefficient[i]!=0):
            value_of_dify += difCoefficient[i]*input_x**i
    return value_of_dify


# ---------輸入初始值 Xn ---------
Xn = float(input("輸入初始近似值Xn："))         # 通常以勘根或觀察選出

while(True):

    pl.vlines(Xn, 0, Value_coefficient_y(Xn), colors='green', label = "x = Xn")     # 畫從 y=0 到 y=f(Xn) 的鉛直線
    counter = 500
    while(counter):

        Xn1 = Xn - Value_coefficient_y(Xn)/Value_coefficient_dify(Xn)               # 用公式找到 Xn1 (更接近根的近似值)
        print("Value X", 501-counter, "=", Xn1)

        difx = np.linspace(Xn1, Xn, 500)                # 給定 difx 為從 Xn1 到 Xn 
        dify = (Value_coefficient_dify(Xn))*(difx-Xn)+Value_coefficient_y(Xn)       # 由點斜式找到 dify (從切線方程式回推 dify )

        pl.plot(difx, dify, color = "blue")        # 畫 f(x) 在 x=Xn 處的切線Tangent

        pl.vlines(Xn1, 0, Value_coefficient_y(Xn1), colors='green')           # 畫從 y=0 到 y=f(Xn1) 的鉛直線
        counter -= 1

        if(abs(Xn-Xn1) < 10**-7):          # 與前次數值差異小於 10^-7
            break 

        Xn = Xn1

    print("迭代共進行", 500-counter, "次")

    # ---------最後畫的在最上面---------
    pl.axhline(y = 0, color = "black", label = "X-axis")    # 畫 X 軸
    pl.plot(x, coefficient_y, color = "red", label = "Function")        # 畫 f(x) 圖形

    pl.legend()     # 印出有給定 label 標籤的線段
    pl.show()       # show 出圖片

    Xn = float(input("試試其他初始值Xn："))

# 23x^3-56x^2-964x^1+3049  
# -5~10     |   -2
# -10~700   |   -3

# 123x^8-89x^6-13x^5+4x^2-789

# -1x^3+3x^2+2x^1+3

# 1x^3-27

# 公式：Xn+1 = Xn - f(Xn)/f'(Xn)
