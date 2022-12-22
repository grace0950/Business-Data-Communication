#coding=utf-8
 
# 导包
import sys
import struct
from socket import *
 
# 全局变量
g_server_ip = ''
g_uploadFileName = ''
 
#运行程序格式不正确
def run_test():
	"判断运行程序传入参数是否有错"
	global g_server_ip
	global g_uploadFileName
	
	if len(sys.argv) != 3:
		print("运行程序格式不正确")
		print('-'*30)
		print("tips:")
		print("python3 tftp_upload.py 192.168.1.1 test.jpg")
		print('-'*30)
		exit()
	else:
		g_server_ip = sys.argv[1]
		g_uploadFileName = sys.argv[2]
		#print(g_server_ip, g_uploadFileName)
 
#主程序
def main():
	run_test()
 
	# 打包
	sendDataFirst = struct.pack('!H%dsb5sb'%len(g_uploadFileName), 2, g_uploadFileName.encode('gb2312'), 0, 'octet'.encode('gb2312'), 0)
 
	# 创建UDP套接字
	s = socket(AF_INET, SOCK_DGRAM)
 
	# 发送上传文件请求到指定服务器
	s.sendto(sendDataFirst, (g_server_ip, 6969)) #第一次发送, 连接tftp服务器
 
	fileNum = 0 #表示接收文件的序号
 
	# 以二进制格式打开文件
	f = open(g_uploadFileName, 'rb')
 
	# 第一次接收数据
	responseData = s.recvfrom(1024)
 
	# print(responseData)
	recvData, serverInfo = responseData
 
	#print(recvData)
	#print(serverInfo)
 
	# 解包
	packetOpt = struct.unpack("!H", recvData[:2])  #操作码
	packetNum = struct.unpack("!H", recvData[2:4]) #块编号
	
	#print(packetOpt, packetNum)
 
	if packetOpt[0] == 5:
		print("tftp服务器发生错误！")
		exit()
 
	while True:
		#　从文件中读取512字节数据
		readFileData = f.read(512)
		
		if fileNum == 65536:
			fileNum = 0

		#　打包
		sendData = struct.pack('!HH', 3, fileNum) + readFileData
		
		# 发送数据到tftp服务器
		s.sendto(sendData, serverInfo) #第二次发给服务器的随机端口
 
		# 接受服务器回传数据
		recvData, serverInfo = s.recvfrom(1024)
 
		#print(recvData)
 
		# 解包
		packetOpt = struct.unpack("!H", recvData[:2])  #操作码
		packetNum = struct.unpack("!H", recvData[2:4]) #块编号
 
		if packetOpt[0] == 5:
			print("tftp服务器发生错误！")
			exit()
 
		if len(sendData) < 516 or packetNum[0] != fileNum:
			print("%s文件上传成功！"%g_uploadFileName)
			break
		
		fileNum += 1
 
	#　关闭文件
	f.close()
 
	# 关闭套接字
	s.close()
 
 
#调用main函数
if __name__ == '__main__':
	main()

