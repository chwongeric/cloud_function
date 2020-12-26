#auto generate test and spray messages - uncommment 1st line of generate if json  - uncommment 1st line if json.gz already generated
#!/bin/sh
echo $0 $1 $2
if [ ! -z "$2" ]
  then
    echo "generating test $2 records in INVENTORY.json..."
    /usr/bin/python3 generate.py -r $2
    /bin/gunzip INVENTORY.json.gz
fi
echo "spraying pubsub messages..."
step=10
for (( i=0 ; i<1 ; i++ ))
do
  offset=`expr $i \* $step`
  echo $offset
  /usr/bin/python3 spray.py -s 10000 -c 10 -o $offset -p $1 >& test-10K-$i.log &
done
