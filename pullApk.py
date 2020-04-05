import os

outPath = input(str("请输入导出地址(若不填则导出到该脚本文件夹下)："))

#默认root版本
root_status = 0
count = 0

def readPackList():
	#读取包名文件，输出列表
	with open('package.txt',"r") as f:
		packList = f.readlines()
		return(packList)

def checkRoot():
	#执行adb指令查询root情况
	res = os.system("adb shell su")
	#rootStatu = res.read()
	if res == 127:
		print("非root版本，部分分区的apk无法pull出来")
		return 1
	else:
		return 0
		
def checkPath(list:list,apkPath:str):
	#筛选需要root权限的分区
	for i in list:
		if i in apkPath:
			return 1
	return 0	

def changeApkName(apkName,packName,outPath):
	#重命名
	cmd = "ren "+outPath+"\\"+apkName+" "+packName+".apk"
	print(cmd)
	os.system(cmd)
	
def pullApk(package,count,outPath):
	outPath = outPath
	apkPath = ""
	apkName = ""
	pathArr = []
	path_limit = 0
	root_limit = ["/vendor","/product","/oppo_product"]
	path = os.popen("adb shell pm path"+ " " + package).readlines()
	if path == []:
		print("手机中无此包名的Apk")
		with open('fail.txt','a') as f:
			f.write(package+"——手机中无此应用\r\n")
	else:
		pathArr = path[0].split(":")
		arrLen = len(pathArr)
		apkPath = pathArr[arrLen-1].strip()
		apkName = apkPath.split("/")[-1].strip()
		#print(apkName)
		path_limit = checkPath(root_limit,apkPath)
		#print(root_status,path_limit)
		
		if root_status == 1 & path_limit == 1:
			print(package+"需要root权限导出")
			with open('fail.txt','a') as f:
				f.write(package+"——需要root权限\r\n")
		else:
			
			command = "adb pull "+apkPath+" "+outPath
			#print(command)
			os.system(command)
			changeApkName(apkName,package,outPath)
			with open('sucess.txt','a') as f:
				f.write(package+"\r\n")
			count = count+1
	return count
root_status = checkRoot()

packList = readPackList()
for packName in packList:
	package = packName.strip()
	if package:
		print("开始导出"+package)
		count = pullApk(package,count,outPath)
print('共输出'+str(count)+"个应用")
