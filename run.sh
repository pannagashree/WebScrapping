#!/bin/sh
Indian_papers='DH IE HT POI ET DNA TGI TOI TI'	
Foreign_papers='CNN USToday BB DAWN CNBC TG rediff'

python3 copy1.py --src /home/pannaga/work/extraction/extraction --dest Indian --folder_list $Indian_papers
python3 copy1.py --src /home/pannaga/work/extraction/extraction --dest Foreign --folder_list $Foreign_papers

today=`date +"%Y%m%d"`
file_list=`ls ./extracted/Indian/$today/`
for i in $file_list;do
	python3 data_cleaner_Acoustic.py "Indian" $i &
	python3 data_cleaner_language.py "Indian" $i &
done
wait
file_list=`ls ./extracted/Foreign/$today/`
for i in $file_list;do
	python3 data_cleaner_Acoustic.py "Foreign" $i &
	python3 data_cleaner_language.py "Foreign" $i &
done
wait