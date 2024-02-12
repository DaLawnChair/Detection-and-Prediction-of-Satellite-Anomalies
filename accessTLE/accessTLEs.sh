#!/bin/bash

# TO USE THIS SCRIPT, 
# (1) Give this script read and execute permissions with "chmod u=rx accessTLEs.sh"
# (2) Change the log in credentials below
# (3) Change the parameters if desired
# (4) In the terminal, run the script "./accessTLEs.sh"


#(REQUIRED) User specific credentials for space-track.org
user=""
password=""

#cookies
cookies="cookies.txt"

#User set parameters for the range of satellites accessed
#Note using this method will lead to a bad if the difference between the start and end satellite ids is greater than ~400. 
#Use with disgression.
startSatelliteId=0
endSatelliteId=300
minLines=$(( 3650*2 )) #A mimimum of 10 years worth of data if the satellite produces 1 TLE per day
dateStart="1957-01-01"
dateEnd="2024-01-01"

#combined output of the data from the satellites.
combinedData="combinedData.txt"
sateliteInfo="satelliteAddedInfo.txt"
rawDataHolderDir="rawDataHolder"

#mkdir "$rawDataHolderDir"

#Log in to space-track.org
curl -c $cookies -b $cookies https://www.space-track.org/ajaxauth/login -d "identity=${user}&password=${password}"

#Access all satellites within the given range.
for(( satelliteNumber=${startSatelliteId}; satelliteNumber<=${endSatelliteId}; satelliteNumber++ ))
do
  if (( numOfLines == 68 )); then
    curl -c $cookies -b $cookies https://www.space-track.org/ajaxauth/login -d "identity=${user}&password=${password}"
    sleep 60
  fi

  #Access the TLE data for the satellite given the date range.
  curl --cookie $cookies --limit-rate 100K https://www.space-track.org/basicspacedata/query/class/gp_history/NORAD_CAT_ID/${satelliteNumber}/orderby/TLE_LINE1%20ASC/EPOCH/${dateStart}--${dateEnd}/format/tle --output ${satelliteNumber}.txt
  
  numOfLines=$(wc -l < ${satelliteNumber}.txt) 
  addedToCombinedData="No"
  #Remove the file if the amount of TLE lines does not meet the minimum.
  if [[ $numOfLines -lt ${minLines} ]]; then
    rm ${satelliteNumber}.txt
  #Concatonate the data to the combinedText file.
  else
    cat ${satelliteNumber}.txt >> ${combinedData}
    addedToCombinedData="Yes"
    mv ${satelliteNumber}.txt "$rawDataHolderDir"
  fi

  # Store information on the satellites entered
  echo "$satelliteNumber    $numOfLines   $addedToCombinedData" >> "$sateliteInfo"
done


