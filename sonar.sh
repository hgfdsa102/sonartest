if [[ $DRONE_PULL_REQUEST_TITLE == *"SONAR"* ]]
then
    echo "Start Scanning"
else
    echo "Pass scanning"
fi