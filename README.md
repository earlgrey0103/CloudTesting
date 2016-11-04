# 云计算产品性能测试指南

本文所有操作对应的是 Debian 系统，并且用户假设为 root 用户。根据本文所述指南，我对腾讯云和阿里云的三个云计算基础产品进行了评测，产品类别包括云服务器、云数据库和对象存储。具体对比结果请看：[国内公有云大幅降价后，首份一手云计算产品评测报告](http://www.codingpy.com/article/guide-on-testing-cloud-products/)

## 云服务器

在开始测试云服务器之前，推荐按量计费方式购买实例。同时确保用于对比的云服务器配置规格相同或具有可比性。

通过服务商提供的账户名和密码登陆云服务器之后，请先更新系统（本文所有操作均针对 Debian 系统）。

```
apt-get update
```

在云服务器的测试过程，我将先通过 UnixBench 和 GeekBench 这两个常用的基准测试工具，获得对主机的一个总体评分。然后再从 CPU、内存和磁盘 I/O 等方面进行单项测试。

#### 1. UnixBench

UnixBench 是测试类 Unix 系统性能的老牌工具，也是常用的基准测试工具。它会执行 11 个单项测试，包括字符串处理、浮点运算效率、 文件数据传输、管道吞吐等，然后将结果与一个基准系统进行比较，得到一个指数值。指数值越高，性能越好。

最终的得分比单个测试的结果根据参考价值，而且也方便对服务器进行比较。

在安装 UnixBench 之前，要先准备好相关的依赖。请执行：

```
apt-get install libx11-dev libgl1-mesa-dev libxext-dev perl perl-modules make gcc
```

下载安装包，然后按下面的提示操作。官方的源在 googlecode 上，国内访问不便，我已经将文件上传到对象存储服务。

```
wget http://codingpy-1252715393.cosgz.myqcloud.com/archive/UnixBench5.1.3.tgz
tar xvf UnixBench5.1.3.tgz
cd UnixBench
make
```

运行 make 之前，确保将 Makefile 文件中 `GRAPHICS_TEST = defined` 行被注释掉，因为我们是在服务器端进行测试，不需要做 2D/3D 图形测试。

最后，执行：

```
./Run
```

如果一切正常，应该会出现类似下面的文字：

![UnixBench 运行](http://ww4.sinaimg.cn/large/006tNc79gw1f9cjxnv8kaj313i0vc11l.jpg)

UnixBench 测试的运行时间比较长，期间可以离开去干别的事情。

除了直接在命令行输出测试结果之外（如下图），还会在 result 目录下生成一个 HTML 格式的报告，可以将其拷贝至本地。

![UnixBench 测试结果](http://ww4.sinaimg.cn/large/65e4f1e6gw1f9ck0mzvboj213i13uwxi.jpg)

一般来说，得分在 1000 以上的云服务器就算还不错的。

#### 2. GeekBench

GeekBench 是另一款知名的性能测试工具，目前的最新版本为 GeekBench 4。相较于 GeekBench 3，最新版对测试标准进行了调整，能够更好地模拟真实任务和应用。它支持测试单核和多核性能，不过由于我们选择的虚拟机只有 1 核，在测试时请忽略多核的测试得分。

还要注意的是，GeekBench 是一款商业软件，可供免费使用的只有 32 位。如果你想在 64 位服务器上使用该工具，则需先添加必备的运行时库。

```
dpkg --add-architecture i386
apt-get update
apt-get install libc6:i386 libstdc++6:i386
```

然后下载安装包：

```
wget http://codingpy-1252715393.cosgz.myqcloud.com/archive/Geekbench-4.0.0-Linux.tar.gz ~/ # 官方地址下载较慢，替换为国内源。
```

解压缩并执行测试：

```
tar -zxvf ~/Geekbench-4.0.0-Linux.tar.gz && cd ~/build.pulse/dist/Geekbench-4.0.0-Linux/
./geekbench_x86_64
```

测试结束后，GeekBench 会将结果上传到自己的网站，并返回一个访问链接。

#### 3. CPU Cyclictest

Cyclictest 是一个高精度测试程序，可用来衡量 CPU 的平均延迟，即完成一个 CPU 周期所需的时间。通过这个数据，我们可以判断物理 CPU 的超卖情况；特定时间内，有多少虚拟 CPU 在排队等候物理 CPU 进行处理。因此，这个测试的数据越低，说明 CPU 的响应越快，延迟越低。

cyclictest 是 rt-tests 包的一部分，我们按如下操作安装并运行：

```
apt-get install rt-tests
cyclictest -D 10s -q
```

我们将使用测试结果中的 `avg_lat` 值。

#### 4. 内存性能

Mbw 是一个 Linux 内存性能测试工具，可以测试内存数据拷贝操作的速度。速度越快，性能越高。在内存大小相同的情况下，该指标就显得比较重要，该指标越高越好。因为通常内存数据操作是计算的常见瓶颈之一。

按如下操作安装并运行：

```
apt-get install mbw
mbw -n 250 -t 0 200
```

我们取测试结果中 `avg_copy` 的值。

#### 5. 磁盘 I/O

磁盘 I/O 也是云服务器性能的重要指标，一般是选择读写速度快的。磁盘 I/O 性能测试主要分为两类：顺序读写和随机读写。顺序读写频繁，应该关注数据吞吐量指标；随机读写频繁，核心指标则是 IOPS，即每秒的输入输出量（或读写次数）。我们的云服务器上主要是存储一些小文件，更注重随机读写性能。

Fio 是测试磁盘 I/O 的传统基准工具。安装非常简单：

```
apt-get install fio
```

使用如下命令测试磁盘随机读性能：

```
fio --name=randread --ioengine=libaio --direct=1 --bs=4k --iodepth=64 --size=4G --rw=randread --gtod_reduce=1
```

部分选项的说明如下：

* direct=1：测试过程绕过机器自带的 buffer，使测试结果更加真实。
* rw=randread：测试随机读的 I/O
* size=4G：本次测试文件的大小为 4G
* bs=4k：单次 I/O 的块文件大小为 4KB
* iodepth=64：一次执行 64 个操作。

使用如下命令测试磁盘随机写性能：

```
fio --name=randwrite --ioengine=libaio --direct=1 --bs=4k --iodepth=64 --size=4G --rw=randwrite --gtod_reduce=1
```

IOPS 的值越高，磁盘读写性能越好。

磁盘性能的另一个指标是延迟。可以通过 IOPing 工具进行测试。IOPing 会运行指定数量的磁盘 I/O 请求，并测试响应的时间。输出结果测试使用 ping 命令测试网络延迟的输出。

操作如下提示安装 IOPing：

```
wget https://launchpad.net/ubuntu/+archive/primary/+files/ioping_0.9-2_i386.deb ~/
dpkg -i ~/ioping_0.9-2_i386.deb
```

然后通过下面的命令运行测试：

```
ioping -c 10 .
```

输出结果类似下面这样，我们取其中 avg 对应的值。

```
4 KiB from . (ext3 /dev/vda1): request=1 time=1.87 ms
4 KiB from . (ext3 /dev/vda1): request=2 time=1.57 ms
4 KiB from . (ext3 /dev/vda1): request=3 time=2.02 ms
4 KiB from . (ext3 /dev/vda1): request=4 time=1.78 ms
4 KiB from . (ext3 /dev/vda1): request=5 time=1.79 ms
4 KiB from . (ext3 /dev/vda1): request=6 time=1.56 ms
4 KiB from . (ext3 /dev/vda1): request=7 time=2.14 ms
4 KiB from . (ext3 /dev/vda1): request=8 time=1.96 ms
4 KiB from . (ext3 /dev/vda1): request=9 time=2.64 ms
4 KiB from . (ext3 /dev/vda1): request=10 time=1.69 ms

--- . (ext3 /dev/vda1) ioping statistics ---
10 requests completed in 9.02 s, 525 iops, 2.05 MiB/s
min/avg/max/mdev = 1.56 ms / 1.90 ms / 2.64 ms / 303 us
```

请求响应时间越低，说明磁盘性能越好。

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

测试输出如下图所示。

## 对象存储服务

对象存储服务性能测试的注意事项，请参考：[论云存储服务性能评测的正确姿势](http://blog.qiniu.com/archives/5010)。

推荐的测试方法：

* 使用对应厂商位于同一区域的云服务器
* 确保测试机性能不弱，CPU等资源充足
* 随机生产指定数量、大小的测试文件，如
  * 10000 个 50KB 文件
  * 1000 个 2MB 文件
  * 100 个 50MB 文件
* 通过 SDK 计算上传、下载、删除等操作的用时
* 使用同一批文件，通过 SDK 做高并发测试

测试脚本（基于 Python SDK）位于 [Github 项目](https://github.com/bingjin/CloudTesting)中的 test_cos 目录下。测试数据位于 csv 目录下。

## 参考资料

待更新。
