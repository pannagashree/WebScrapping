import glob, os,sys
import tarfile,argparse
import concurrent.futures
import datetime
import time
global counter

def parse_args():
	parser=argparse.ArgumentParser(description="Tarring of data files")
	parser.add_argument('--src',type=str)
	parser.add_argument('--dest',type=str)
	parser.add_argument('--folder_list',nargs="+")
	return parser.parse_args()

def copy(folder):
	counter=0
	global destination,source
	name=os.path.join(destination,folder+".tar")
	tFile = tarfile.open(name, 'w')
	print ("above",tFile)
	os.chdir(os.path.join(source,folder))
	#print(os.getcwd())
	file_list=glob.glob("*.text")
	print(file_list,folder)
	for i in file_list:
		#print(i,folder)
		tFile.add(i)
		counter+=1
		print(counter,folder)
		os.remove(i)
	tFile.close()


if __name__=='__main__':
	destination="/home/pannaga/work/extraction/extraction/extracted/"
	parsed=parse_args()
	print(parsed.folder_list)
	folder_list=parsed.folder_list
	destination=destination+parsed.dest
	source=parsed.src
	today=time.strftime('%Y%m%d')
	if not os.path.exists(os.path.join(destination,str(today))):
		os.mkdir(os.path.join(destination,str(today)))
	destination=os.path.join(destination,str(today))
	with concurrent.futures.ProcessPoolExecutor() as executor:
		executor.map(copy,folder_list)
	
		
		
		
		