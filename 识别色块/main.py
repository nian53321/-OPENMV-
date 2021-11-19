import sensor, image, time,struct,pyb

blue_threshold = (0, 100, 25, -128, -102, -12)
red_threshold = (30, 80, 127, 26, -45, 127)
PI = 3.14159
sensor.reset()
#sensor.set_vflip(True)
#sensor.set_hmirror(True)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA) # 160x120 (4,800 pixels) - O(N^2) max = 2,3040,000.
#sensor.set_windowing([0,20,80,40])
sensor.skip_frames(time = 2000)     # WARNING: If you use QQVGA it may take seconds
#clock = time.clock()                # to process a frame sometimes.
sensor.set_auto_gain(False)#自动增益
sensor.set_auto_whitebal(False)#关白平衡
sensor.set_colorbar(False)#关闭彩色模式
sensor.set_auto_exposure(False)#关闭自动曝光

S = 0
roi = (10,10,300,220)


while(True):
    c = 0
    img = sensor.snapshot()#    .binary([blue_threshold])
    blobs1 = img.find_blobs([blue_threshold],roi=roi)
    if blobs1:
        for b in blobs1:
            if(b[4]>1000 and b[4]<5000):
                S = b[2] * b[3]
                for c in img.find_circles(roi,threshold = 3000, x_margin = 10, y_margin = 10, r_margin = 10,r_min = 20, r_max = 100, r_step = 2):
                    if c:
                        img.draw_circle(c.x(), c.y(), c.r(), color = (255, 0, 0))
                        print('blue_cir')
                        break

                if b[4]<(0.7)*S:
                    img.draw_cross(b[5],b[6])
                    print('blue_tri')
                    break
                if not c:
                    img.draw_rectangle(b[0:4]) # rect
                    #用矩形标记出目标颜色区域
                    print('blue_rect')
            else:
                blobs2 = img.find_blobs([red_threshold],roi=roi)
                if blobs2:
                    for b in blobs2:
                        if(b[4]>1000 and b[4]<5000):
                            S = b[2] * b[3]
                            for c in img.find_circles(roi,threshold = 3500, x_margin = 10, y_margin = 10, r_margin = 10,r_min = 20, r_max = 100, r_step = 2):
                                if c:
                                    img.draw_circle(c.x(), c.y(), c.r(), color = (255, 0, 0))
                                    print('red_cir')
                                    break

                            if b[4]<(0.7)*S:
                                img.draw_cross(b[5],b[6])
                                print('red_tri')
                                break
                            if not c:
                                img.draw_rectangle(b[0:4]) # rect
                                #用矩形标记出目标颜色区域
                                print('red_rect')
