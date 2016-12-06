## 数据库服务器

首先，我们在测试用的云服务器上安装 sysbench 和 mysql-client：

```
apt-get install sysbench mysql-client
```

这里安装的 sysbench 版本为 0.4.12 。然后登陆到购买的数据库实例，并创建测试数据库 dbtest。

```
mysql -h [云数据库IP] -P [云数据库端口号] -uroot -p[云数据库密码]
```

云数据库内网 IP 或访问地址，可从厂商的云数据库实例管理界面获取。如没有数据库服务器，请在腾讯云、阿里云等厂商以按量计费模式新建实例。

实例创建后，需要手动在控制台点击“初始化”来初始化实例，在此过程中会弹出窗口要求设置 root 用户的密码。阿里云 RDS 则需要在数据库登陆管理界面新建一个用户，指定用户名和密码；同时将 测试 ECS 的内网 IP 地址添加到服务器服务器的白名单中。具体操作参见管理页面。

登陆至云数据库服务器后，我们创建用户测试的数据库 dbtest。

```
create database dbtest;
```

然后，使用 sysbench 的 prepare 语句在指定数据中生成用于执行测试的表。

```
sysbench --test=oltp --oltp-table-size=1000000 --mysql-db=dbtest --mysql-host=[云数据库访问IP/地址] --mysql-user=[云数据库用户名] --mysql-password=[云数据库密码] prepare
```

该命令将新建一个名为 sbtest 的表，其中包含一百万行数据。在实际测试过程中，发现**阿里云 RDS 在创建测试数据时用的时间明显较长**。

你可以登陆数据库检查是否创建成功：

```
mysql> use dbtest;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A
 
Database changed
mysql> show tables;
+------------------+
| Tables_in_dbtest |
+------------------+
| sbtest           |
+------------------+
1 row in set (0.00 sec)
 
mysql> SELECT COUNT(*) FROM sbtest;
+----------+
| COUNT(*) |
+----------+
|  1000000 |
+----------+
1 row in set (0.12 sec)
```

接下来，就可以使用 sysbench 命令进行针对 MySQL 的 OLTP 基准测试了。先执行一个数据库只读测试（oltp-read-only=on）：

```
sysbench --test=oltp --oltp-table-size=1000000 --oltp-test-mode=complex --oltp-read-only=on --num-threads=6 --max-time=60 --max-requests=0 --mysql-db=dbtest --mysql-host=[云数据库访问IP/地址] --mysql-user=[云数据库用户名] --mysql-password=[云数据库密码] run
```

如果要执行读写测试，只需要将 oltp-read-only 的值设置为 off 即可。