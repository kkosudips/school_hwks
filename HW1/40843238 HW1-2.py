# 2.(50%) 請參照投影片(unit4,p10)資料,將浮水印圖(nfuwm.jpeg）以取代
# 法將它嵌入在 elaine image，個別嵌入在(1) 7th,(2) 3rd bit 內.根據
# 下列 
#  (a) 重複嵌入 3 個浮水印圖至 elaine image,計算嵌入前後之 PSNR 
# value 
#  (b) 不重複,僅將 1 個 watermark 嵌入至 elaine image, 計算嵌入前後
# 之 PSNR value
#  （同學亦可自行試驗取代其他位元內，感受不同位元被取代後的結果） 
#
# --------------import, function -------------------------------
import cv2
import math

def MSE_calc(height,width,img,img_origin):
    sum = 0
    for i in range(0,height):
        for j in range(0,width):
           # 轉成 int 才能避免報 overflow 錯誤 
           diff = int(img_origin[i][j])-int(img[i][j])
           sum= sum+ diff*diff
    return sum/(width*height)

def PSNR_calc(img_new,img):
    height,width = img.shape
    MSE = MSE_calc(height,width,img_new,img)
    PSNR = 10*math.log((255**2/MSE),10)
    return PSNR

def get_wm_bin_seq(h,w,img_wm):
    # 將 watermark 轉成 0,1 序列 seq
        # 黑: 0b0 => 0
        # 白: 0b11111111 => 1
    # python 內建 binary轉換 bin()，轉出格式為 "0b0"
    seq = []
    for i in range(0,h):
        for j in range(0,w):
            if(bin(img_wm[i][j])=="0b0"):seq.append("0")
            elif(bin(img_wm[i][j])=="0b11111111"):seq.append("1")
    return seq

def substitute(img_host,img_wm,bit,repeat):
    # 替代法，將浮水印嵌入原圖，可指定要替代原圖 pixel 的第幾個 bit，以及浮水印要重複幾次。
    result = img_host.copy()

    # base x,base y 用來提供每次嵌入原圖的浮水印之起始位置
    base_y=0
    base_x=0

    # 浮水印跟原圖的高度、寬度
    wm_h,wm_w = img_wm.shape
    host_h,host_w = img_host.shape

    # 產生浮水印的 bitstream
    seq = get_wm_bin_seq(wm_h,wm_w,img_wm)
    seq_index = 0

    # 嵌入 n 次浮水印
    for n in range (0,repeat):
        for i in range (0,wm_h):
            for j in range (0,wm_w):
                # 先將原圖pixel取出(base_y+i,base_x+j) 
                #   -> 使用python轉bin，格式為 0x10101010，使用[2:]取0x後面的字元
                #       -> 使用zfill(8)將2進制強制用8個位元顯示
                # 將原圖 bin_pixel 以 wm binary 序列代替
                #   -> 原圖 bin_pixel 要先從 string 轉成 list 才能代替(python不允許字串中的某個字元直接被替換)
                #       -> 代替要用 7- 替代位元 (因為最右邊為 0)
                # 代替完後轉回 string再轉回10進位，替換host的pixel

                host_bin = (bin(result[base_y+i][base_x+j])[2:]).zfill(8)
                host_bin = list(host_bin) 
                
                host_bin[7-int(bit)] = seq[seq_index]
                host_bin = ''.join(host_bin)
                result[base_y+i][base_x+j] = int(host_bin,2)

                seq_index+=1
                if(seq_index>=wm_h*wm_w):seq_index=0

        # 修改下一次浮水印要添加在原圖的起始位置
            # 如果寬度會超出邊界就從下一排的最左邊(x=0)開始擺
            # 如果高度會超出邊界就從最上面(y=0)開始擺
        base_x+=wm_w
        if(base_x+wm_w>=host_w):base_x=0;base_y+=wm_h
        if(base_y+wm_h>=host_h):base_x=0;base_y=0
        seq_index=0
    

    return result


# ---------------- Main section -------------------------------


elaine = cv2.imread('elaine_512x512.bmp',cv2.IMREAD_GRAYSCALE)
nfuwm = cv2.imread('nfuwm_68x68.jpg',cv2.IMREAD_GRAYSCALE)
cv2.imshow('Host image',elaine)


# (1) 7th bit (a) 重複嵌入 3 個浮水印圖至 elaine image,計算嵌入前後之 PSNR 
wmted_img = substitute(elaine,nfuwm,7,3)
cv2.imshow('7 bit, repeat 3 times',wmted_img)
PSNR = PSNR_calc(elaine,wmted_img)
print(f'PSNR of 7bit repeat 3 times: {PSNR}')

# (1) 7th bit (b) 不重複,僅將 1 個 watermark 嵌入至 elaine image, 計算嵌入前後之 PSNR value
wmted_img = substitute(elaine,nfuwm,7,1)
cv2.imshow('7 bit, repeat 1 times',wmted_img)
PSNR = PSNR_calc(elaine,wmted_img)
print(f'PSNR of 7bit repeat 1 times: {PSNR}')

# (2) 3rd bit (a) 重複嵌入 3 個浮水印圖至 elaine image,計算嵌入前後之 PSNR 
wmted_img = substitute(elaine,nfuwm,3,3)
cv2.imshow('3 bit, repeat 3 times',wmted_img)
PSNR = PSNR_calc(elaine,wmted_img)
print(f'PSNR of 3bit repeat 3 times: {PSNR}')

# (2) 3rd bit (a) 不重複,僅將 1 個 watermark 嵌入至 elaine image, 計算嵌入前後之 PSNR value
wmted_img = substitute(elaine,nfuwm,3,1)
cv2.imshow('3 bit, repeat 1 times',wmted_img)
PSNR = PSNR_calc(elaine,wmted_img)
print(f'PSNR of 3bit repeat 1 times: {PSNR}')

# ------------------------------------------------------------
cv2.waitKey(0)
cv2.destroyAllWindows()