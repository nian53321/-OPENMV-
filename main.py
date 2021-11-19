import sensor, image, time,struct,pyb
led = pyb.LED(1)
def init_sensor():
	led.on()
	sensor.reset()
	sensor.set_pixformat(sensor.GRAYSCALE)
	sensor.set_framesize(sensor.QQVGA)
	sensor.skip_frames(time = 10)
	sensor.set_auto_gain(False)
	sensor.set_auto_whitebal(False)
	sensor.set_colorbar(False)
	sensor.set_auto_exposure(False)
	led.off()
init_sensor()
uart = pyb.UART(3, 115200)
uart.init(115200, bits=8, parity=None, stop=1)
clock = time.clock()
led = pyb.LED(2)
isangle = 0
angle = 0
lines = []
for i in range(1,11):
	lines.append(15+10*i)
flag = [0b00000000000]*10
flag_result = 0
Mid_Zuobiao_cha1 = [0]*10
Mid_Zuobiao_final1 = 0
Mid_Zuobiao_final2 = 0
Deep = 0
K = 2.82
jishu2 = 1
jishu3 = 0
Xiangsu_color = 0
cha = 0
def send_data_packet(Angle,X1,X2,Y,Z,isangle):
	temp = struct.pack("<bbffffiibb",
				   0x0D,
				   0x0A,
				   float(Angle),
				   float(X1),
				   float(X2),
				   float(Y),
				   int(Z),
				   int(isangle),
				   0x0A,
				   0X0D)
	uart.write(temp)
while(True):
	clock.tick()
	isreset = uart.read()
	if not(isreset == None):
		init_sensor()
	thresh = sensor.snapshot().binary([(120,255)])
	thresh.lens_corr(1.7,1)
	flag = [0b00000000000]*10
	flag_result = 0
	cha = 0
	Xiangsu_Zuobiao_sum = [0]*10
	Xiangsu_Shuliang_sum = [1]*10
	x_min = [0]*10
	x_l = [0]*10
	x_r = [0]*10
	Mid_Zuobiao_jizhi = [0]*10
	Mid_Zuobiao_avg = [0]*10
	jishu1 = 1
	jishu3 = 0
	jishu4 = 0
	angle1 = 0
	angle2 = 0
	angle3 = 0
	angle4 = 0
	angle5 = 0
	angle = 0
	Sum_1 = 0
	sum1 = 0
	sum2 = 0
	sum3 = 0
	for i in range(0,10):
		for j in range(0,160,1):
			Xiangsu_color = (thresh.get_pixel(j, lines[i]) == 255)
			if Xiangsu_color:
				Xiangsu_Zuobiao_sum[i] +=  j
				Xiangsu_Shuliang_sum[i] += 1
			if x_min[i] == 0:
				if Xiangsu_color:
					x_l[i] = j
					x_min[i] = 1
			else:
				if Xiangsu_color:
					x_r[i] = j
	for i in range(0,10):
		Mid_Zuobiao_jizhi[i] = ((x_l[i] + x_r[i]) / 2)
		Mid_Zuobiao_avg[i] = Xiangsu_Zuobiao_sum[i] / Xiangsu_Shuliang_sum[i]
		if (Mid_Zuobiao_avg[i] > 0) and (Mid_Zuobiao_avg[i] < 159) and (Xiangsu_Shuliang_sum[i]>12):
			flag[i] =  pow(2,i)
			flag_result += flag[i]
	for i in range(5,10):
		if not (flag[i] == 0):
			Mid_Zuobiao_final1 += Mid_Zuobiao_jizhi[i]
			Mid_Zuobiao_final2 += Mid_Zuobiao_avg[i]
			jishu4 = jishu4 + 1
	x1 = Mid_Zuobiao_final2/5
	if not (jishu4==0):
		Mid_Zuobiao_final1 = (Mid_Zuobiao_final1/jishu4/2)-40
		Mid_Zuobiao_final2 = (Mid_Zuobiao_final2/jishu4/2)-40
	for i in range(3,9,1):
		if Xiangsu_Shuliang_sum[i] > 30:
			jishu1 = jishu1 + 1
			Sum_1 = Sum_1 +Xiangsu_Shuliang_sum[i]
	Mid_Zuobiao_Deep_Sum = Sum_1 / jishu1
	if not Mid_Zuobiao_Deep_Sum == 0:
		Deep = (160 / Mid_Zuobiao_Deep_Sum) * K
	if (thresh.get_pixel(1, 50) == 255) or (thresh.get_pixel(159, 50) == 255):
		Deep = -1
	if (thresh.get_pixel(1, 70) == 255) or (thresh.get_pixel(159, 70) == 255):
		Deep = -1
	if (thresh.get_pixel(1, 90) == 255) or (thresh.get_pixel(159, 90) == 255):
		Deep = -1
	if (thresh.get_pixel(1, 50) == 255) and (thresh.get_pixel(159, 50) == 255):
		Deep = 1
	if (thresh.get_pixel(1, 70) == 255) and (thresh.get_pixel(159, 70) == 255):
		Deep = 1
	if (thresh.get_pixel(1, 90) == 255) and (thresh.get_pixel(159, 90) == 255):
		Deep = 1
	for i in range(0,9):
		Mid_Zuobiao_cha1[i] = Mid_Zuobiao_avg[i] - Mid_Zuobiao_avg[i+1]
		if not flag[i]==0:
			cha += Mid_Zuobiao_cha1[i]
	if (Xiangsu_Shuliang_sum[2] - Xiangsu_Shuliang_sum[3] > 20)and(flag_result > 1007):
		if (Mid_Zuobiao_cha1[2] > 10):
			isangle = 1
	if (isangle) == 1:
		jishu2 = jishu2 + 1
	if(jishu2) > 70:
		jishu2 = 1
		isangle = 0
	if not(Mid_Zuobiao_avg[6] > Mid_Zuobiao_avg[9]) and (Mid_Zuobiao_avg[6] > 50) and (flag[5] == 0):
		if (flag[6] == 64) and (flag[9] == 512) and (Xiangsu_Zuobiao_sum[6] > 20) and (Xiangsu_Zuobiao_sum[9] > 20):
			angle1 = Mid_Zuobiao_avg[6]-Mid_Zuobiao_avg[9]
			jishu3 += 1
	if not (Mid_Zuobiao_avg[6] > Mid_Zuobiao_avg[8]) and (Mid_Zuobiao_avg[6] > 50) and (flag[5] == 0):
		if (flag[6] == 64) and (flag[8] == 256) and (Xiangsu_Zuobiao_sum[6] > 20) and (Xiangsu_Zuobiao_sum[8] > 25):
			angle2 = Mid_Zuobiao_avg[6]-Mid_Zuobiao_avg[8]
			jishu3 += 1
	if not (Mid_Zuobiao_avg[6] > Mid_Zuobiao_avg[7]) and (Mid_Zuobiao_avg[6] > 50) and (flag[5] == 0):
		if (flag[6] == 64) and (flag[7] == 128) and (Xiangsu_Zuobiao_sum[6] > 20) and (Xiangsu_Zuobiao_sum[7] > 20):
			angle3 = Mid_Zuobiao_avg[6]-Mid_Zuobiao_avg[9]
			jishu3 += 1
	if (flag[7] == 128) and (flag[9] == 512) and (Xiangsu_Zuobiao_sum[7] > 20) and (Xiangsu_Zuobiao_sum[9] > 20):
		angle4 = Mid_Zuobiao_avg[7]-Mid_Zuobiao_avg[9]
		jishu3 +=1
	if (flag[8] == 128) and (flag[9] == 512) and (Xiangsu_Zuobiao_sum[8] > 20) and (Xiangsu_Zuobiao_sum[9] > 20):
		angle5 = Mid_Zuobiao_avg[7]-Mid_Zuobiao_avg[9]
		jishu3 +=1
	if not (jishu3) == 0:
		angle = (angle1 + angle2 + angle3 + angle4 + angle5) / jishu3
	if angle>60 or angle<-60:
	   angle = 0
	send_data_packet(angle,Mid_Zuobiao_final1,Mid_Zuobiao_final2,Deep,flag_result,isangle)
