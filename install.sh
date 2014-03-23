#!/bin/bash
# The Script for importing sql statements

# directories
_create_db_path="./docs/create_table.sql"
#_drop_db_path="./docs/Queries/drop_tables.sql"
_insert_test_path="./docs/testing_data.sql"
_db_name="c410" 

# mysql info
mysql_name=""
mysql_password=""

# pre-defined queries
_create_db_query="CREATE DATABASE IF NOT EXISTS $_db_name;"

# change this if you need to connect a remote server
_HOST="127.0.0.1"   #localhost

# set permission
chmod -R "700" "$_create_db_path"
#chmod -R "700" "$_drop_db_path"
#chmod -R "700" "$_insert_test_path"

echo -e "\n ===================== CMPUT410 Deployment Toolkit ===================== \n"
login(){
    while [ "$mysql_password" == "" ] || [ "$mysql_name" == "" ] ; do 
        echo -n "Enter your mysql username:"
        read mysql_name
        echo -n "Enter your mysql password:"
        read mysql_password
        echo
    done
}

drop_all(){
    # drop all tables
    mysql -u "$mysql_name" -p"$mysql_password" -h "$_HOST" "$_db_name" < "$_drop_db_path" --verbose
}

insert_all(){
    #TODO:
    echo -e "TODO:insert all the tuples into db"
    mysql -u "$mysql_name" -p"$mysql_password" -h "$_HOST" "$_db_name" < "$_insert_test_path" --verbose

}

rebuild_all(){
    # create database
    # mysql -u "$mysql_name" -p"$mysql_password" -h "$_HOST" --verbose -e "$_create_db_query"
    
    # create tables through pipe
    mysql -u "$mysql_name" -p"$mysql_password" -h "$_HOST" "$_db_name" < "$_create_db_path" --verbose
    
    mysql -u "$mysql_name" -p"$mysql_password" -h "$_HOST" "$_db_name" < "$_insert_test_path" --verbose
}

# flags
case $1 in
    "-rebuild_all") login
                    rebuild_all;;
    "-insert_test") login
                    insert_all;;
    "-drop_all")    login
                    drop_all;;
    "-backup_all")  backup_all;;
    *)              echo "Invalid flag argument"
                    exit $?;;
esac
echo -e "\n ======================================================================= \n"
exit $?





