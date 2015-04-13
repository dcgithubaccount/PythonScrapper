#!/bin/bash
export PATH=$PATH:/usr/local/bin
#echo $PATH
projectdir="/Volumes/MyData/SharesProject/FTCompanyData"
logpath="/Volumes/MyData/SharesProject/FTCompanyData/log"
inputpath="/Volumes/Mydata/SharesProject/FTCompanyData/Input"
#outputpath="/Volumes/Mydata/SharesProject/FTCompanyData/Output"

START_TIME=`date '+%d%m%y_%H%M%S'`
#echo $START_TIME
TODAY=`date '+%Y%m%d'`
#TODAY="20150109"

cd $inputpath

if [ $1 == "UK" ]; then 
     file="UK_FTSE100.txt"
     outputpath="/Volumes/Mydata/SharesProject/FTCompanyData/Output/UK"
elif [ $1 == "Italy" ]; then 
     file="Italy_FTSEMIB.txt"
     outputpath="/Volumes/Mydata/SharesProject/FTCompanyData/Output/Italy"
elif [ $1 == "France" ]; then
     file="France_CAC40.txt"
     outputpath="/Volumes/Mydata/SharesProject/FTCompanyData/Output/France"     
elif [ $1 == "India" ]; then
     file="India_NIFTY100.txt"
     outputpath="/Volumes/Mydata/SharesProject/FTCompanyData/Output/India"     
elif [ $1 == "Germany" ]; then
     file="Germany_DAX80.txt"
     outputpath="/Volumes/Mydata/SharesProject/FTCompanyData/Output/Germany"
elif [ $1 == "Holland" ]; then
     file="Holland_AEX25.txt"
     outputpath="/Volumes/Mydata/SharesProject/FTCompanyData/Output/Holland"     
elif [ $1 == "Belgium" ]; then
     file="Belgium_BEL20.txt"
     outputpath="/Volumes/Mydata/SharesProject/FTCompanyData/Output/Belgium"     
elif [ $1 == "USA100" ]; then
     file="USA_SandP100.txt"
     outputpath="/Volumes/Mydata/SharesProject/FTCompanyData/Output/USA"     
elif [ $1 == "USA200" ]; then
     file="USA_SandP200.txt"
     outputpath="/Volumes/Mydata/SharesProject/FTCompanyData/Output/USA"     
elif [ $1 == "USA300" ]; then
     file="USA_SandP300.txt"
     outputpath="/Volumes/Mydata/SharesProject/FTCompanyData/Output/USA"     
elif [ $1 == "USA400" ]; then
     file="USA_SandP400.txt"
     outputpath="/Volumes/Mydata/SharesProject/FTCompanyData/Output/USA"     
elif [ $1 == "USA500" ]; then
     file="USA_SandP500.txt"
     outputpath="/Volumes/Mydata/SharesProject/FTCompanyData/Output/USA"     
elif [ $1 == "USAADR" ]; then
     file="USA_SandPADR.txt"
     outputpath="/Volumes/Mydata/SharesProject/FTCompanyData/Output/USA"     
elif [ $1 == "Australia" ]; then
     file="Australia_ASX100.txt"
     outputpath="/Volumes/Mydata/SharesProject/FTCompanyData/Output/Australia"     
elif [ $1 == "Japan" ]; then
     file="Japan_NIKKEI225.txt"
     outputpath="/Volumes/Mydata/SharesProject/FTCompanyData/Output/Japan"     
elif [ $1 == "Swiss" ]; then
     file="Swiss_SMI20.txt"
     outputpath="/Volumes/Mydata/SharesProject/FTCompanyData/Output/Swiss"     
elif [ $1 == "Spain" ]; then
     file="Spain_IBEX35.txt"
     outputpath="/Volumes/Mydata/SharesProject/FTCompanyData/Output/Spain"     
elif [ $1 == "HongKong" ]; then
     file="HongKong_HSI50.txt"
     outputpath="/Volumes/Mydata/SharesProject/FTCompanyData/Output/HongKong"     
elif [ $1 == "Sweden" ]; then
     file="Sweden_OMXS30.txt"
     outputpath="/Volumes/Mydata/SharesProject/FTCompanyData/Output/Sweden"     
elif [ $1 == "LATAM" ]; then
     file="LATAM_LATAM40.txt"
     outputpath="/Volumes/Mydata/SharesProject/FTCompanyData/Output/LATAM"     
elif [ $1 == "Canada" ]; then
     file="Canada_TSX60.txt"
     outputpath="/Volumes/Mydata/SharesProject/FTCompanyData/Output/Canada"     
elif [ $1 == "Denmark" ]; then
     file="Denmark_OMX20.txt"
     outputpath="/Volumes/Mydata/SharesProject/FTCompanyData/Output/Denmark"     
elif [ $1 == "Finland" ]; then
     file="Finland_OMX25.txt"
     outputpath="/Volumes/Mydata/SharesProject/FTCompanyData/Output/Finland"     
elif [ $1 == "Norway" ]; then
     file="Norway_OSLOAllShare.txt"
     outputpath="/Volumes/Mydata/SharesProject/FTCompanyData/Output/Norway"     
elif [ $1 == "Korea" ]; then
     file="Korea_KOSPI100.txt"
     outputpath="/Volumes/Mydata/SharesProject/FTCompanyData/Output/Korea"     
elif [ $1 == "Singapore" ]; then
     file="Singapore_STI30.txt"
     outputpath="/Volumes/Mydata/SharesProject/FTCompanyData/Output/Singapore"     
elif [ $1 == "NewZealand" ]; then
     file="NewZealand_NZSX50.txt"
     outputpath="/Volumes/Mydata/SharesProject/FTCompanyData/Output/NewZealand"     
elif [ $1 == "Portugal" ]; then
     file="Portugal_PSI20.txt"
     outputpath="/Volumes/Mydata/SharesProject/FTCompanyData/Output/Portugal"     
elif [ $1 == "SouthAfrica" ]; then
     file="SouthAfrica_JSE40.txt"
     outputpath="/Volumes/Mydata/SharesProject/FTCompanyData/Output/SouthAfrica"     
fi	     

filename=`echo $file | awk -F'.' '{print $1}'`
touch $logpath/"$filename"_"$START_TIME".log

cd $projectdir

while IFS=: read -r line 
do 
	echo "scrapy crawl FTCompanyData -a ric=$line"
	scrapy crawl FTCompanyData -a ric=$line --set LOG_FILE=$logpath/"$filename"_"$START_TIME".log 
done <"$inputpath/$file"

END_TIME=`date '+%d%m%y_%H%M%S'`
echo $END_TIME >> $logpath/"$filename"_"$START_TIME".log
echo "Start merging files" >> $logpath/"$filename"_"$START_TIME".log
awk '{print $0}' *.csv >> $outputpath/"$TODAY"_"$filename".csv


sed -e 's/,//g' -e 's/|/|/g' $outputpath/"$TODAY"_"$filename".csv > $outputpath/tmp.csv ; mv $outputpath/tmp.csv $outputpath/"$TODAY"_"$filename".csv
echo "Removed Commas from merged csv files" >> $logpath/"$filename"_"$START_TIME".log

echo "Removing multiple csv files" >> $logpath/"$filename"_"$START_TIME".log
rm *.csv
echo "Removed all csv files" >> $logpath/"$filename"_"$START_TIME".log
if [ $1 == "USAADR" ]; then 
   cd $outputpath
   awk '{print $0}' *USA_SandP*.csv >> $outputpath/"$TODAY"_USA_NYQ_NSQ.csv
   rm *USA_SandP*.csv
   echo "Scala File Processing for USA" >> $logpath/"$filename"_"$START_TIME".log	 
   
   sh /Volumes/MyData/SharesProject/DCFTCalc/Maincaller.sh USA $TODAY
		
   echo "Removing logs files older than 21 days" >> $logpath/"$filename"_"$START_TIME".log
   find $logpath/*.log -mtime +21 -exec rm {} \;
   
   python /Volumes/MyData/SharesProject/FTCompanyData/OutputCleaner.py USA
   	

elif [ $1 == "USA100" ] || [ $1 == "USA200" ] || [ $1 == "USA300" ] || [ $1 == "USA400" ] || [ $1 == "USA500" ]; then
   echo "No Scala File Processing for these files " >> $logpath/"$filename"_"$START_TIME".log	

else 
   echo "Scala File Processing " >> $logpath/"$filename"_"$START_TIME".log
   sh /Volumes/MyData/SharesProject/DCFTCalc/Maincaller.sh $1 $TODAY	

   python /Volumes/MyData/SharesProject/FTCompanyData/OutputCleaner.py $1	

fi
echo "Exiting Scrapy Shell" >> $logpath/"$filename"_"$START_TIME".log	
echo `date '+%d%m%y_%H%M%S'` >> $logpath/"$filename"_"$START_TIME".log
