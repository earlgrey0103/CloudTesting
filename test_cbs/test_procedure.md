## 块存储性能测试

### PTS 测试步骤

根据 PTS 规范，SSD 性能测试需要经过以下四个步骤：

1. 净化：通过擦除数据，将 SSD 置于接近 FOB 状态。
2. 事先准备工作负载：写入规定的数据到整个 SSD，帮助其达到稳态。
3. 正式测试之前的准备工作：循环运行测试，直到 SSD 进入稳态。
4. 测试：当 SSD 进入稳态时开始测试。

> * 一块新的SSD被称为FOB，即为“Fresh Out of The Box(新鲜出炉)”的缩写。
> * SSD 初次使用后，进入到下一个阶段，SNIA 称之为“Steady State(稳态)”。此时，SSD 性能水平相对稳定，可以准确测量。

### 评测步骤

1. 创建虚拟机

VM 规格相同，选择相同规格、相同容量的云盘。

2. 挂载云硬盘（格式化）

```sh
sudo fdisk -l
mkfs.ext4 /dev/xvdb
mkfs.ext4 /dev/xvdc
```

3. 安装依赖包

```sh
sudo apt-get -y update
sudo apt-get -y install gnuplot php5-cli util-linux zip make autoconf libtool gettext libgconf2-dev libncurses5-dev python-dev libaio-dev libaio1 build-essential git autoconf libtool gettext libgconf2-dev libncurses5-dev python-dev

sudo apt-get -y install fio

sudo apt-get -y install autopoint
sudo apt-get -y install xvfb

cd util-linux/
./autogen.sh
./configure --disable-libblkid
make
sudo mv blkdiscard /usr/bin/
sudo blkdiscard --verbose -o 0 -l `expr $(lsblk -n -o size -b /dev/xvdb) - 512` /dev/xvdb
sudo blkdiscard --verbose -o 0 -l `expr $(lsblk -n -o size -b /dev/xvdc) - 512` /dev/xvdc

cd
wget http://download.gna.org/wkhtmltopdf/0.12/0.12.1/wkhtmltox-0.12.1_linux-wheezy-amd64.deb
sudo dpkg -i wkhtmltox-0.12.1_linux-wheezy-amd64.deb

# get cloudharmony block storage benchmark
cd
git clone git://github.com/cloudharmony/block-storage.git


```

4. 执行自动测试程序

示例：腾讯云 高效云盘 50G
磁盘名称：/dev/vdb
测试命令：

nohup sudo ~/block-storage/run.sh --meta_compute_service "Qcloud CVM" --meta_drive_type Hybrid --meta_instance_id test_cbs --meta_provider Qcloud --meta_region guangzhou-3 --meta_storage_config "Hyrbid" --meta_storage_vol_info 50GB --meta_test_id "Qcloud Hybrid 50GB" --oio_per_thread 64  --target /dev/vdb --test iops --test throughput --test latency --test wsat --test hir --threads 8 --verbose &

5. 收集测试数据
