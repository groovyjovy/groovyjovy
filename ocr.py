from os import name
import pyocr
import pyocr.builders
import cv2
import numpy as np
import re
from PIL import Image
import sys
 
#テキストファイルから名前を取得して、リストに入れる
path = r'C:\Users\01082\python_programs\namelist.txt'
#分割される文字をリストに格納（"佐々木遥人"）等
prename_list = [] 
#("佐","々","木","遥","人")のように分割された文字列がリストに格納されていく
name_list = []
def namelist_get(filepath):
    with open(filepath, 'r',encoding="utf-8_sig") as fileread:
        for i in fileread:
            prename_list.append(i)
            for j in range(len(prename_list[-1]) - 1):
                apst = prename_list[-1][j:j + 1]
                name_list.append(apst)
                
    return name_list

name_list = namelist_get(path)
print(name_list)

#利用可能なOCRツールを取得
pyocr.tesseract.TESSERACT_CMD = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
tools = pyocr.get_available_tools()
 
if len(tools) == 0:
    print("OCRツールが見つかりませんでした。")
    sys.exit(1)
 
#利用可能なOCRツールはtesseractしか導入していないため、0番目のツールを利用
tool = tools[0]
 
#画像から文字列を取得
res = tool.image_to_string(Image.open(r"C:\Users\01082\python_programs\PdfToImage\image_file\seikei_01.jpg"),lang="jpn",builder=pyocr.builders.WordBoxBuilder(tesseract_layout=4))
 
#取得した文字列を表示
#print(res)



#以下は画像のどの部分を検出し、どう認識したかを分析
out = cv2.imread(r"C:\Users\01082\python_programs\PdfToImage\image_file\seikei_01.jpg")
#height = out.shape[0]
#width = out.shape[1]

aaaa = "a"
return_list = []

#リストに含まれていない値に対して任意のデフォルト値を返す
def my_index(l, x, default=False):
    if x in l:
        return l.index(x)
    else:
        return default

#print(type(res))
for d in res:
    print(d.content) #どの文字として認識したか
    print(d.position) #どの位置を検出したか
    #print(type(d.position))
    if re.search(r'(...-....-....)',d.content):
        cv2.rectangle(out, d.position[0], d.position[1], (0, 0, 255), -1) #検出した箇所を赤枠で囲む
    if re.search(r'(...-...-....)',d.content):
        cv2.rectangle(out, d.position[0], d.position[1], (0, 0, 255), -1)
    if re.search(r'(..-....-....)',d.content):
        cv2.rectangle(out, d.position[0], d.position[1], (0, 0, 255), -1)
    if re.search(r'(....-..-....)',d.content):
        cv2.rectangle(out, d.position[0], d.position[1], (0, 0, 255), -1) 
    if re.search(r'(...-...-...)',d.content):
        cv2.rectangle(out, d.position[0], d.position[1], (0, 0, 255), -1)   

    for i in name_list:
        result = i in d.content
        return_list.append(result)
        #print(any(return_list))  
        if True in return_list:
            nametrue_position = my_index(return_list,True)
            #print(name_list[nametrue_position - 1] + name_list[nametrue_position])
            #print(aaaa + d.content +"A")
            if name_list[nametrue_position]  + name_list[nametrue_position + 1] == d.content:
                    #print(name_list[nametrue_position ] + name_list[nametrue_position + 1])
                    #print(d.content +"〇")
                    cv2.rectangle(out , d.position[0], d.position[1], (0, 0, 255), -1)
                    #print("=====================================================================")

            if name_list[nametrue_position - 1]  + name_list[nametrue_position] in aaaa + d.content:
                cv2.rectangle(out , bbbb[0], d.position[1], (0, 0, 255), -1)
                #print("=====================================================================")  

            if name_list[nametrue_position ]  + name_list[nametrue_position + 1] in aaaa + d.content:
                cv2.rectangle(out , d.position[0], d.position[1], (0, 0, 255), -1)   

            #for j in prename_list:
                #if any(k in aaaa + d.content for k in j):
                    #print('================================================')
                    #cv2.rectangle(out , d.position[0] , d.position[1], (0, 0, 255), -1)


    #print(type(aaaa))
    return_list.clear() 
    #print((aaaa))
    aaaa = d.content
    bbbb = d.position 

#検出結果の画像を表示

#resized_out = cv2.resize(out,(width/2, height/2))
cv2.imwrite(r"c:\Users\01082\siryo\kuronuri.jpg", out)
#cv2.imshow("img",out)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
