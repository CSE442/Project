import cv2
import time
import math
import thread
import channel

colors = {}
colors['red'] = {
                    'name':'red',
                    'up_h':0,
                    'up_s':0,
                    'up_v':0,
                    'lo_h':0,
                    'lo_s':0,
                    'lo_v':0,
                    'bgr':(0,0,255),
                    'X':0,
                    'Y':0,
                    'num':0,
                    'exists':False
                }

colors['grey'] = {
                    'name': 'grey',
                    'up_h':0,
                    'up_s':0,
                    'up_v':0,
                    'lo_h':0,
                    'lo_s':0,
                    'lo_v':0,
                    'bgr':(0,0,0),
                    'X':0,
                    'Y':0,
                    'num':0,
                    'exists':False
                }

color_detected = {}



def isColor(hue, sat, vib, color):#looks at the HSV values and determines if it matches the HSV range of the color
    if (color.get('lo_h')<hue and hue<color.get('up_h') and\
       color.get('lo_s')<sat and sat<color.get('up_s') and\
       color.get('lo_v')<vib and sat<color.get('up_v')):
        return True
    else:
        return False

def whatColor(hue, sat, vib):#looks at the HSV values and determines which of the detected colors it is
    for item in color_detected:
        if (item['lo_h']<hue<item['up_h'] and item['lo_s']<sat<item['up_s'] and item['lo_v']<vib<item['up_v']):
            return item
    return colors['grey']#if a color was not detected in the initial frame it will not be tracked

def Tracker(send_channel):
    camera = cv2.VideoCapture(0)
    imageCounter =1
    widthOfCircle = 0
    _, initialFrame = camera.read()
    cv2.imwrite('C:\Users\Aaron\python\images\Original.png', initialFrame)
    cv2.imshow('Original Picture', initialFrame)
    width = initialFrame.shape[0]
    halfW = float(width/2)
    height = initialFrame.shape[1]
    halfH = float(height/2)
    for c in range(0,width):
        for r in range(0,height):
            color = initialFrame[c,r]
            hsv = cv2.cvtColor(initialFrame, cv2.COLOR_BGR2HSV)
            hue = hsv[c,r,0]
            sat = hsv[c,r,1]
            vib = hsv[c,r,2]
            for item in colors.itervalues():
                if(isColor(hue,sat,vib,item)):
                    if(not item['exists']):
                        color_detected[item['name']]=item
                        item['exists'] = True
                    item['X'] += c
                    item['Y'] += r
                    initialFrame[c,r] = item['bgr']
    for item in color_detected:
        avgX = item['X']/item['num']
        avgY = item['Y']/item['num']
        if avgX > 0 and avgX < width -1 and avgY > 0 and avgY < height -1:
            #determine width of the circle
            width = 0
            height = 0
            x1 = avgX
            y1 = avgY
            x2 = avgX
            y2 = avgY
            while x1<width and initialFrame[x1,avgY][0] == 255:
                initialFrame[x1,finalBlueY] = (255,255,255)
                x1 = x1+1
                blueWidth = blueWidth + 1
            while x2>0 and initialFrame[x2,avgY][0] == 255:
                initialFrame[x2,finalBlueY] = (255,255,255)
                x2 = x2-1
                blueWidth = blueWidth + 1
            while y1<height and initialFrame[avgX,y1][0] == 255:
                initialFrame[finalBlueX,y1] = (255,255,255)
                y1 = y1+1
                blueHeight = blueHeight + 1
            while y2>0 and initialFrame[avgX,y2][0] == 255:
                initialFrame[finalBlueX,y2] = (255,255,255)
                y2 = y2-1
                blueHeight = blueHeight + 1
            if(min(height, width) < step):
                step = min(height, width)
    cv2.imshow('Initialization',initialFrame)

    jCrap = 0
    emptyImg = initialFrame
    for c in range(0,width):
        for r in range(0,height):
            emptyImg[c,r] = (0,0,0)
    
    for item in color_detected:
        item['X']=0
        item['Y']=0
        item['num']=0
        item['exists']=False

    while camera.isOpened():
        start_time = time.time()
        _, frame = camera.read()
        
        width = frame.shape[0]
        height = frame.shape[1]

        if step == 0:
            step = 10
        for c in range(0,width, step/2):
            for r in range(0,height, step/3):
                color = frame[c,r]
                hsv = colorsys.rgb_to_hsv(color)
                hue = hsv[0]
                sat = hsv[1]
                vib = hsv[2]
                for item in color_detetcted:
                    if(not item['exists'] and isColor(hue,sat,vib,color)):
                        item['exists'] = True
                        tempX,rigX,lefX = c
                        tempY,topY,botY = r

                        while tempX < width and isColor(frame[tempX,r][0], frame[tempX,r][1], frame[tempX,r][2]):
                            frame[tempX, r] = item['bgr']
                            tempX = tempX + 1
                        rigX = tempX
                        tempX = c
                        
                        while tempX>1 and isColor(frame[tempX,r][0], frame[tempX,r][1], frame[tempX,r][2]):
                            frame[tempX, currentY] = item['bgr']    
                            tempX = tempX - 1
                        leftMostX = tempX
                        
                        while tempY<height and isColor(frame[c,tempY][0], frame[c,tempY][1], frame[c,tempY][2]):
                            frame[currentX, tempY] = item['bgr']
                            tempY = tempY + 1
                        botY = tempY
                        tempY = r
                        
                        while tempY>1 and isColor(frame[c,tempY][0], frame[c,tempY][1], frame[c,tempY][2]):
                            frame[c, tempY] = item['bgr']
                            tempY = tempY - 1
                        topY = tempY
                        

                        item['X'] = (lefX+rigX)/2
                        item['Y'] = (topY+botY)/2

                        for x in range(item['X']-2, item['X']+2):
                            for y in range(item['Y']-2, item['Y']+2):
                                if y>0 and y<height and x>0 and x<width:
                                    frame[x,y] = (255,255,255)
                        for x in range(item['X']-1, item['X']+1):
                            for y in range(item['Y']-1, item['Y']+1):
                                if y>0 and y<height and x>0 and x<width:
                                    frame[x,y] = item['bgr']


                outputImg = emptyImg
                for item in color_detected:
                    for x in range(item['X']-1, item['X']+1):
                        for y in range(item['Y']-1, item['Y']+1):
                            if y>0 and y<height and x>0 and x<width:
                                outputImg[x,y] = item['bgr']

                
                                
                imageCounter = imageCounter +1 
                
                if start_time != time.time(): 
                    colorDetectionList['---fps---']= 1/(time.time() - start_time)

                send_channel.send(colorDetectionList)
                cv2.imshow('Initialization',frame)
                k = cv2.waitKey(5) & 0xFF
                if k == 27:
                    thread.exit()
                    break




        
        
