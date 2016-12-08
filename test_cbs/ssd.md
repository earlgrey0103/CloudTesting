# 阿里云：你的 SSD 云盘虽好，但也别这么坑我啊

本文是[《20天持续压测，告诉你云存储性能哪家更强？》](http://www.codingpy.com/article/cloud-block-storage-performance-testing/)的续篇。上篇中，我们介绍了云存储性能测试的大致背景，并先对国内两大云厂商阿里云与腾讯云的高效云盘的测试结果进行了分析。本文将接着对比 SSD 云盘的性能。由于已经在上篇中介绍了此次测试的诸多背景，因此本文的篇幅相对来说会比较精简。

SSD 是固态硬盘的英文简称，最突出的特点就是读写速度快，能够在低于 1ms 的时间内对任意位置存储单元完成 I/O (输入/输出)操作，适用于 I/O 密集型业务。阿里云在 2015 年 7 月推出了 SSD 云盘，号称可以达到最高 20000 IOPS。约一年后 ，腾讯云也发布了自家的 SSD 云盘，IOPS 的最高性能超过阿里云 4000。

SSD 的 IOPS 性能虽高，但是其整体性能还受吞吐量和访问时延的影响。而且价格不低，每 GB 一个月要 100 元左右。因此，在购买之前，尤为需要进行全面的压力测试。

在笔者之前，虽然肯定有其他人对两家厂商的 SSD 云盘产品做过性能测试，但从初步的百度搜索结果来看，大多只是执行几次 fio 命令得出的数据。笔者或许是第一个根据 SNIA PTS 规范（见上一篇中的说明）对云盘做测试的，而且测试次数也足够充分，可以看出产品性能的稳定性。

## 测试数据下载

测试数据大约 190MB（解压后），下载地址为：[https://pan.baidu.com/s/1i5BJZCD](https://pan.baidu.com/s/1i5BJZCD)，提取码：e2xd。

其中，文件夹的命名规律为：`厂商_云盘类型_容量`。除了 `aliyun_ssd_500x` 和 `aliyun_ssd_250x` 外，每个文件夹下均有一个 `report.pdf` 文件，为测试程序自动生成，里面包含了测试结果、数据和图表。

![](http://ww2.sinaimg.cn/large/006tNc79gw1fahgz7diayj30bk0ak0ui.jpg)

另外，笔者用 Highcharts 制作了一些可交互图表，可用来查看汇总后的各项数据。地址如下：[http://codingpy.com/specials/cbs_test/](http://codingpy.com/specials/cbs_test/)。

将数据包解压后，你会发现其中阿里云 SSD 云盘有 4 个相关的文件夹，其中两个带有 `x` 字样。这是因为其中的数据并不是笔者一开始希望得到的。那为什么出现了这些数据？

原因大致是这样的：

笔者曾经因为账号内余额不足等多种原因，多次重新启动过对阿里云 SSD 云盘的性能测试。经过漫长的等待，最终快要完成性能对比文章时，又**发现阿里云的数据只达到了预期性能的一半**。这些数据显然是真实的数据，但却又让人无法相信。

最终在同事的指点下，才找到了背后真正的原因：**测试用的服务器不是 I/O 优化实例**。

没错，`aliyun_ssd_250x` 和 `aliyun_ssd_250x` 文件夹下就是以非 I/O 优化实例测试得出的 SSD 性能数据。

最终，为了能够尽快给出 SSD 云盘的对比结果，笔者选择了取消对 PTS 中 WSAT、HIR 两项测试（见[上篇](http://www.codingpy.com/article/cloud-block-storage-performance-testing/)中的说明）。

## 预期性能对比

在介绍测试结果之前，我们先回顾一下两家云盘的预期性能（SSD 云盘为下图右侧部分）。

<a href="http://ww1.sinaimg.cn/large/006tNc79gw1fah1xdjyjyj31400lgwig.jpg"><img src="http://ww1.sinaimg.cn/large/006tNc79gw1fah1xdjyjyj31400lgwig.jpg" alt="两大产生云硬盘预期性能对比"></a>

上图显示，**阿里云的 SSD 云盘在 IOPS 和 Throughput（吞吐量）指标上有一定的性能优势，只有在容量 1TB 以上时才性能略低于腾讯云**。

笔者之前就说过，预期性能不等于实际性能，二者之间很可能存在差异。那么两家厂商在 SSD 云盘上的真实差距到底有多大？

我们下面用数据说话。

## 性能测试结果

先看一遍两个容量级别下的性能对比图：

首先是 250GB 容量的 IOPS、Throughput、Latency 三项指标的数据（可点击图片查看大图，或查看[交互式图表](http://www.codingpy.com/specials/cbs_test/)）：

![](http://ww4.sinaimg.cn/large/006tNc79gw1fahhll18ugj30xc0m877a.jpg)
![](http://ww2.sinaimg.cn/large/006tNc79gw1fahhm6812bj30xc0m8mz8.jpg)
![](http://ww3.sinaimg.cn/large/006tNc79gw1fahhmmdpouj30xc0m8mza.jpg)

<table>
  <tr>
    <td style='width:50%;padding: 8px;'><a href="http://ww4.sinaimg.cn/large/006tNc79gw1fahhll18ugj30xc0m877a.jpg"><img src="http://ww4.sinaimg.cn/large/006tNc79gw1fahhll18ugj30xc0m877a.jpg" alt="SSD IOPS测试"></a></td>
    <td style='width:50%;padding: 8px;'><a href="http://ww2.sinaimg.cn/large/006tNc79gw1fahhm6812bj30xc0m8mz8.jpg"><img src="http://ww2.sinaimg.cn/large/006tNc79gw1fahhm6812bj30xc0m8mz8.jpg" alt=""></a></td>
  </tr>
  <tr>
      <td style='width:50%;padding: 8px;'><a href="http://ww3.sinaimg.cn/large/006tNc79gw1fahhmmdpouj30xc0m8mza.jpg"><img src="http://ww3.sinaimg.cn/large/006tNc79gw1fahhmmdpouj30xc0m8mza.jpg" alt=""></a></td>
    </tr>
</table>

500GB 容量的性能对比（可点击图片查看大图，或查看[交互式图表](http://www.codingpy.com/specials/cbs_test/)）：

![](http://ww3.sinaimg.cn/large/006tNc79gw1fahhn43a0sj30xc0m8goo.jpg)
![](http://ww3.sinaimg.cn/large/006tNc79gw1fahhnjahjsj30xc0m80us.jpg)
![](http://ww3.sinaimg.cn/large/006tNc79gw1fahho0rmjbj30xc0m8mzd.jpg)

<table>
  <tr>
    <td style='width:50%;padding: 8px;'><a href="http://ww3.sinaimg.cn/large/006tNc79gw1fahhn43a0sj30xc0m8goo.jpg"><img src="http://ww3.sinaimg.cn/large/006tNc79gw1fahhn43a0sj30xc0m8goo.jpg" alt=""></a></td>
    <td style='width:50%;padding: 8px;'><a href="http://ww3.sinaimg.cn/large/006tNc79gw1fahhnjahjsj30xc0m80us.jpg"><img src="http://ww3.sinaimg.cn/large/006tNc79gw1fahhnjahjsj30xc0m80us.jpg" alt=""></a></td>
  </tr>
  <tr>
      <td style='width:50%;padding: 8px;'><a href="http://ww3.sinaimg.cn/large/006tNc79gw1fahho0rmjbj30xc0m8mzd.jpg"><img src="http://ww3.sinaimg.cn/large/006tNc79gw1fahho0rmjbj30xc0m8mzd.jpg" alt=""></a></td>
    </tr>
</table>


<small>图注：RW Ratio 指的是 I/O 操作中的读写比例，0/100 表示顺序写, 100/0 表示顺序读。</small>

> > 如果觉得看起来不方便，可以访问用 Highcharts 制作的交互式图表：[http://codingpy.com/specials/cbs_test/](http://codingpy.com/specials/cbs_test/)。

IOPS 的数据稍微有点特殊，我们最后来介绍。先看吞吐量和访问时延。

吞吐量指标上，

- 阿里云和腾讯云在 128k 数据块下的数据较为接近，而且绝对差值随着云盘容量增加而扩大；
- 1024k 数据块下，阿里云的吞吐量是腾讯云的约 2 倍，而且倍数随着云盘容量增加会逐步扩大。

访问时延指标上，

- 阿里云和腾讯云的时延范围均在 0.7~0.9ms 之间；
- 二者均为容量大的云盘，访问时延更低；
- 同一容量下，阿里云的时延均低于腾讯云，约有平均 0.1 ms 的优势。

最后回到 IOPS 性能。出乎意料地是，和高效云盘一样，腾讯云 SSD 云盘的 IOPS 峰值也高于阿里云，这与官方预期的性能不符。但是如果你看了[前一篇文章](http://www.codingpy.com/article/cloud-block-storage-performance-testing/)，会发现这并不是数据错误，而是因为：

> [产品文档](https://www.qcloud.com/document/product/362/5145?utm_source=Zhihu&utm_medium=Community&utm_campaign=Community))中承诺的IO性能，如1TB的SSD云硬盘，随机IOPS能达到24000IOPS。含义是读写可同时达到24000IOPS，4KB/8KB的 IO都可做到，16KB的IO大小，则无法做到24000（由于吞吐已经达到了260MB/s的限制）。

即测试数据中的峰值可以看成读+写IOPS，而且读写都能同时达到官方预期的性能峰值。这是与阿里云 SSD 云盘的一个较大不同。

### 测试性能与预期性能的差异

![](http://ww3.sinaimg.cn/large/65e4f1e6gw1fajttnoykrj21520fs77q.jpg)

![](http://ww2.sinaimg.cn/large/65e4f1e6gw1fajturll7lj215006ewfp.jpg)

### I/O 优化与非 I/O 优化对比

由于笔者手头上已经有了阿里云 SSD 云盘在 I/O 优化实例和非 I/O 优化实例下的性能数据，不利用一下简单可耻。虽说这样的对比可能意义不大，但至少可以让大家直观地感受到二者之间的差距具体有多少。为了缩减篇幅，仅以 500GB SSD 云盘为例说明。

先来看 IOPS。

在 16KB 以下大小的数据块下，I/O 优化实例的 IOPS 都非常接近峰值，获得了最大性能。而非 I/O 优化实例只取得了 3500 左右的性能，只有前者的 1/5。不过 ，随着测试数据块的增大，二者的 IOPS 值逐渐趋同，在数据块为 1M 的情况下，两者的 IOPS 几乎没有差别。

![IOPS](http://ww2.sinaimg.cn/large/65e4f1e6gw1fajseckolnj21ew0ywtdo.jpg)

吞吐量和访问时延方面的差距也十分明显。

![](http://ww2.sinaimg.cn/large/65e4f1e6gw1fajson30ohj21ao0xy41t.jpg)

![](http://ww4.sinaimg.cn/large/65e4f1e6gw1fajt3dj1wqj21aq0ygwi5.jpg)


## 价格对比



## 结语

• Locate your storage system as close as possible to the applications. This helps keep latency to an absolute minimum. That is, if you are connecting to remote storage, use ioping to determine the lowest latency. This will give you the best performance. Within AWS, you can specify which availability zone which usually translates into different data center locations.
• Match your architecture to your storage solution. Make sure you have the correct amount of cache, the right storage node processor capabilities, and the right ratio of SSD storage.

## 评价

腾讯云：

新增数据盘不支持按量计费、容量范围较小

阿里云：容量范围大、灵活性高

价格：

## 测试后记

犯的错误：

开多了虚拟机，阿里云只需要一台VM，挂载多个磁盘即可。

没有以后台运行，导致断网后Terminal与VM连接中断，测试中断。

双磁盘与单磁盘测试数据输出没弄明白，导致重复测试。

按量付费充值余额不足，导致实例过期，测试中断。

VM 未设置 SSH 登陆，导致重复输入密码。