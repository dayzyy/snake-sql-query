MYSQL_PWD=$MYSQL_ROOT_PASSWORD

mysqladmin ping -h 127.0.0.1
exit $?
