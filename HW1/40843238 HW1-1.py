# 1.(50%)請利用 Random function 產生一續列不規則之 0,1 序列,將這些序
# 列數嵌入至 elaine 照片之內. 
# (a).嵌入個數為原始照片大小的 50% 個 0,1序列數目（亦是（512512）50%
# 的 0,1 序列數目） 
# a.請顯示嵌入後之影像圖 
# b.計算嵌入前,後之差異性為何 (PSNR)？ 
# (b).嵌入個數為原始照片的 2 倍,（亦是(512x512)2 的 0,1 序列數目） 
# a.請顯示嵌入後之影像圖 
# b.計算嵌入前,後之差異性為何 (PSNR)？ 
#  (設計方法：你可以自己設計或參考上課講的方法或文獻中的方法皆可)

# --------------import, function -------------------------------
# pip install opencv-python
import cv2
import random 
import math

def seq_random(img,multiple):
    #隨機產生 圖片大小個數量 的 0,1 序列
    height,width = img.shape
    seq = []
    for i in range(0,int(height*width*multiple)):
        seq.append(random.choice([0,1]))
    return seq

def img_modify(x,y,rule,multiple,seq,img):
    # x,y為起始位置, rule=0 時用 "+" 將序列嵌入原圖, multiple 為嵌入時的倍數 越高越明顯,seq為隨機序列, img為原始圖像
    height,width = img.shape

    result = img.copy()

    for i in range(0,len(seq)):
        if(x>=width or x<0):x=0;y+=1
        if(y>=height or y<0 ):y=0
                                # 該乘數調高可明顯看出嵌入位置
        if(rule==0):result[y][x]+= seq[i]*multiple
        elif (rule==1):result[y][x]-= seq[i]*multiple

        x=x+1

    return result

def MSE_calc(img_modified,img):
    #計算 Mean Error Square
    height,width = img.shape
    sum = 0
    for i in range(0,height):
        for j in range(0,width):
           # 轉成 int 才能避免報 overflow 錯誤 
           diff = int(img[i][j])-int(img_modified[i][j])
           sum= sum+ diff*diff
    return sum/(width*height)

def PSNR_calc(img_modified,img):
    #計算 PSNR 數值
    MSE = MSE_calc(img_modified,img)
    PSNR = 10*math.log((255**2/MSE),10)
    return PSNR

# ---------------- Main section -------------------------------
# 0. 使用 opencv 讀取 elaine。
    ## 因為本次圖片為灰階，因此使用 IMREAD_GRAYSCALE 參數將圖片以灰階讀入。
img = cv2.imread('elaine_512x512.bmp',cv2.IMREAD_GRAYSCALE)
cv2.imshow('img_origin',img)

# 1. 建立 原始照片大小 50% 個 0,1 序列數目 512*512*0.5=131072
# 1.(a). 嵌入個數為原始照片大小的 50% 個 0,1序列數目（亦是（512x512x50%的 0,1 序列數目） 
    # 嵌入方式: 從原始圖像 指定(x,y) 開始由 "左至右" 由 "上至下" 開始嵌入。
    # 如果隨機序列超出原始圖像大小，則從頭(0,0)重複先前規則嵌入。
    ## seq_random(圖片,倍數): 回傳 圖片*倍數 大小的0,1序列
    ## img_modify(起始x, 起始y, 嵌入方法(0加 或 1減), 替換倍數, 替換隨機序列, 原始圖像): 回傳嵌入後的圖像
seq_50_percent = seq_random(img,0.5)
img_50_percent = img_modify(256,50,0,30,seq_50_percent,img)


# 1.(a).a. 顯示嵌入後的影像圖 
cv2.imshow('50%_seq',img_50_percent)

# 1.(a).b. 計算 PSNR (灰階 255, RGB取平均)
    # PSNR = 10*log10(255*255/MSE)
    # MeanErrorSquare = (1/h*w)for(i=1;i<=h;i++)for(j=1;j<=w;j++)(原圖_ij - 比較圖_ij)^2
PSNR = PSNR_calc(img_50_percent,img)
print(f'PSNR of 50% seq img :{PSNR}')

# 1.(b).嵌入個數為原始照片的 2 倍,（亦是(512x512)2 的 0,1 序列數目）
seq_200_percent = seq_random(img,2)
img_200_percent = img_modify(0,0,0,30,seq_200_percent,img)

# 1.(b).a.請顯示嵌入後之影像圖
cv2.imshow('200%_seq',img_200_percent)


# 1.(b).b.計算嵌入前,後之差異性為何 (PSNR)？
PSNR = PSNR_calc(img_200_percent,img)
print(f'PSNR of 200% seq img : {PSNR}')



# ---------------------------------------------------------
cv2.waitKey(0)
cv2.destroyAllWindows()
