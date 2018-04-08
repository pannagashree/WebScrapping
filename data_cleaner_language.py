# -*- coding: utf-8 -*-
import os,sys
import re
import glob
import regex,time
import tarfile
from num_converter_backup import numEnglishConverter,decimal
import concurrent.futures

def strip_split(text):
    reg = r"(?<=[\s\.][^\s\.]{2,}\.|\?|\:|\;)[\s\n]"	#\s stands for whitespace character
    result= regex.sub(reg, '\\n',text)
    # print (result)
    return result.strip().splitlines()


# pattern = r'(?:[A-Z]\.)+'
word_dictionary={
	'b':'be',
	'd':'the',
	'r':'are',
	'u':'you',
	'n':'and',
	'jan':'january',
	'feb':'february',
	'mar':'march',
	'apr':'april',
	'jun':'june',
	'jul':'july',
	'aug':'august',
	'aus':'australia',
	'sept':'september',
	'oct':'october',
	'nov':'november',
	'dec':'december',
	'ft':'feet',
	'mr':'Mister',
	'ms':'Miss',
	'kg':'kilograms',
	'km':'kilometers',
	'sq ft':'square feet',
	'sq':'square feet',
	'co':'company',
	'pvt':'private',
	'ltd':'limited',
	'ads':'advertisements',
	'ad':'advertisement',
	'pte':'private',
	'ref':'referee',
	'smt':'srimathi',
	'std':'standard',
	'wid':'with',
	'wud':'would',
	'div':'division',
	'jr':'junior',
}

def data_processing_language(file):	
	global write_file2,word_dictionary
	pattern = r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))'''
	pattern1=  r'([^a-zA-Z\ \,\"\' ])'
	main_file=tar.extractfile(file)
	data= main_file.read()
	data=str(data)
	data = data.replace('U.S','United States')
	data = data.replace('M.Sc ','Master of SCience')
	data = data.replace('B.Sc ','Bachelor of Science')
	data = data.replace('et al ','et alia')
	data = data.replace('Rs.','Rupees')
	data = data.replace('Dr.','Doctor')
	data = data.replace('Mr.','Mister')
	data = data.replace('Ms.', 'Miss')
	data = data.replace('Mrs.','Misses')
	data = data.replace('Prof.','Professor')
	data = data.replace('$','Dollar')
	data = data.replace('&', 'and')
	data = data.replace('+', 'plus')
	data = data.replace('i.e','that is')
	data = data.replace('*', ' ')
	data = data.replace('#', ' ')
	data = data.replace('\\', ' ')
	
	line_num = 0
	# lines=re.split('[.|?|;]',data)
	lines = strip_split(data)
	lines=list(set(lines))
	for line in lines :
		if(line !=''):
			match=re.findall(pattern,line)
			if(match):
				continue
			else:
				line=line.replace('“',' ')
				line=line.replace('""','" ')
				line=line.replace('\'"','\'')
				line=line.replace('\\',' ')
				line=line.replace('/',' ')
				line=line.replace('”',' ')
				line=line.replace('"',' ')
				rgx = re.compile(r"(?<!\w)\'|\'(?!\w)")
				line=rgx.sub('', line)
				line=line.strip()
				line=line.replace('.',' ')
				line=line.replace('?',' ')
				line=line.replace(';',' ')
				line=line.replace(':',' ')
				line=line.replace(',',' ')
				reg=r'[A-Z][a-z]+'
				line=regex.sub(reg,lambda m: m.group().lower(), line)
				line=' '.join([l.replace(l,word_dictionary[l]) if l in word_dictionary else l for l in line.split()])
				match=re.findall(pattern1,line)
				
				if(match):	
					continue
				else:	
					words = re.split('(\d+)',line)
					for w in words:
						if(w.isdigit()==True):
							words[words.index(w)]=numEnglishConverter(w)+' '
					line=''.join(words)
            
					
					line_num= line_num+1
					line = line.replace('  ',' ')
					line = line.replace('  ',' ')
					print(str(line_num))
					write_file2.write(line.upper())
					write_file2.write('\n')	 
	print(write_file2.tell())

if __name__=="__main__":
	folder=sys.argv[1]
	f=sys.argv[2]
	today=time.strftime('%Y%m%d')
	dest_path="/home/pannaga/work/extraction/extraction/Sentences/"
	path = "/home/pannaga/work/extraction/extraction/extracted/"+folder+"/"+today+"/"+f
	tar=tarfile.open(path)
	files=tar.getmembers()
	path2 = dest_path+'Language/'+folder+'/'
	print(path,path2)
	file_num = len(files)
	if(os.path.isdir(path2)):
	    print('Path Exists adding files to it')
	else:
		os.mkdir(path2)
	write_file2=open(path2+'Sentences_full_test_'+f.split('.')[0]+'.txt','a')
	start_time=time.time()
	with concurrent.futures.ProcessPoolExecutor() as executor:
		executor.map(data_processing_language,files)
	write_file2.close()		
	print("--- %s seconds ---" % (time.time() - start_time))

