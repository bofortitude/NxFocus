#!/bin/bash





############################Custom variable############################


runmode=ipv4


#Default Radius-attribute

deacctType=start
desecret=fortinet
deusername=user10
depassword=pass10
denasPort=100
denasIP=10.0.10.10
deframedIP=192.168.1.110
denasType=Ethernet
decalledID=00-04-5f-00-0f-d1
decallingID=00-01-24-80-b3-9c
deacctID=00000100

############################Custom variable############################





cathelp()
{


cat << EOF


How to:
./shrad.sh destination_IP radtype [options]

Note:
1. "destination_IP" and "radtype" is a must.
2. "radtype" means Radius request type, you have two choice, "auth", "acct".

Options:
  -h  [help]                  Show help.
  -t  [acct_type]             If the radtype is "acct", this parameter can be used, three choice: "start", "update", "stop", default is "start".
  -u  [username]              Default username is $deusername .
  -p  [password]              Default password is $depassword .
  -s  [secret]                Default secret is $desecret .
  -i  [acct_ID]               Default acct_ID is $deacctID .
  
  -A  [run_mode]              If this parameter is used, run mode will be IPv6, default is IPv4.
  -B  [nas_port]              Default is $denasPort .
  -C  [nas_IP]                Default is $denasIP .
  -D  [framed_IP]             Default is $deframedIP .
  -E  [nas_type]              Default is $denasType .
  -F  [called_ID]             Default is $decalledID .
  -G  [calling_ID]            Default is $decallingID .
  

Run like:
./shrad.sh  10.76.2.110 auth  
./shrad.sh  10.76.2.110 acct -t update
./shrad.sh  10.76.2.110 acct -u user100 -p pass100 -D 172.22.1.1


EOF


exit



}






if [[ $* == "" || $1 == "-h" ]]; then

    cathelp

fi

dst_IP=$1

if [[ $2 == "auth" ]]; then
    radtype=auth

elif [[ $2 == "acct" ]]; then
    radtype=acct

else

    cathelp


fi



shift $(($OPTIND + 1 ))



while getopts "ht:u:p:s:i:AB:C:D:E:F:G:" opt
do

    case $opt in
            
         h) cathelp ;;
         t) deacctType=$OPTARG ;;
         u) deusername=$OPTARG ;;
         p) depassword=$OPTARG ;;
         s) desecret=$OPTARG ;;
         i) deacctID=$OPTARG ;;
         A) runmode=ipv6 ;;
         B) denasPort=$OPTARG ;;
         C) denasIP=$OPTARG ;;
         D) deframedIP=$OPTARG    ;;
         E) denasType=$OPTARG    ;;
         F) decalledID=$OPTARG ;;
         G) decallingID=$OPTARG    ;;


         ?) cathelp ;;

    esac

done


if [[ $runmode == ipv4 ]]; then

    mode46="-4"

elif [[ $runmode == ipv6 ]]; then

    mode46="-6"

fi


if [[ $radtype == auth ]]; then

    

    radresult=`echo "User-Name=$deusername,User-Password=$depassword,NAS-IP-Address=$denasIP,NAS-Port=$denasPort,Framed-IP-Address=$deframedIP,NAS-Port-Type=$denasType,Called-Station-Id=$decalledID,Calling-Station-Id=$decallingID" | radclient $mode46 $dst_IP $radtype $desecret`



    firstline=`echo "$radresult" | grep Received`
    if [[ $firstline ]]; then
        echo ""
        secondline=`echo "$radresult" | grep Reply-Message | awk '{print substr($3,1)}'`
        echo "$firstline ==> Reply from $secondline"
        echo ""
    fi

elif [[ $radtype == acct ]]; then
    if [[ $deacctType == update ]]; then

        deacctType="Interim-Update"

    fi

    radresult=`echo "User-Name=$deusername,User-Password=$depassword,NAS-IP-Address=$denasIP,NAS-Port=$denasPort,Framed-IP-Address=$deframedIP,NAS-Port-Type=$denasType,Acct-Status-Type=$deacctType,Acct-Session-Id=$deacctID" | radclient $mode46 $dst_IP $radtype $desecret`



    firstline=`echo "$radresult" | grep Received`
    if [[ $firstline ]]; then
        echo ""
        secondline=`echo "$radresult" | grep Reply-Message | awk '{print substr($3,1)}'`
        echo "$firstline ==> Reply from $secondline"
        echo ""

    fi



fi













