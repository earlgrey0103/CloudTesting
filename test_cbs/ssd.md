# 阿里云：你的 SSD 云盘虽好，但也别这么坑我啊

本文是[]()的续篇，将接着对比国内两大云厂商阿里云与腾讯云的 SSD 云盘性能。由于已经在上篇中介绍了此次测试的诸多背景，因此本文的篇幅会比较精简。

如果你还没看过上篇关于两家高效云盘的测评，那么笔者先带你回顾一下主要结论：

1. **腾讯云高效云盘的各项基础性能指标均优于阿里云，且优势明显；**
2. **腾讯云高效云盘达到了预期的性能，而阿里云部分云盘没有达到，400GB 容量的时延过高；**
3. **阿里云大容量高效云盘的 IOPS 性能受宿主机闲置影响较明显；**
4. **包年包月模式下，腾讯云高效云盘的性价比非常高；**
5. **阿里云高效云盘不同计费模式下费用差别不大，选择的灵活性更高。**

上面每个结论都是有事实、数据支撑的，这些在[高效云盘那篇]()中已有详细交代，本文不再重复。

回到本文的主题，SSD 云盘。SSD 是固态硬盘的英文简称，最突出的特点就是读写速度快，能够在低于 1ms 的时间内对任意位置存储单元完成 I/O (输入/输出)操作，适用于 I/O 密集型业务。阿里云在 2015 年 7 月推出了 SSD 云盘，号称可以达到最高 20000 IOPS。约一年后 ，腾讯云也发布了自家的 SSD 云盘，IOPS 的最高性能超过阿里云 4000。

SSD 的 IOPS 性能虽高，但是其整体性能还受吞吐量和访问时延的影响。而且价格不低，每 GB 一个月要 100 元左右。因此，在购买之前，尤为需要对其进行全面的压力测试。

在笔者之前，虽然肯定有其他人对两家厂商各自的产品做过性能测试，但从初步的百度搜索结果来看，大多只是执行几次 fio 命令得出的数据。笔者或许是第一个根据 SNIA PTS 规范（见上一篇中的说明）对云盘做测试的，而且测试次数也足够充分，可以看出产品性能的稳定性。

## 测试数据下载

测试数据大约 190MB（解压后），下载地址为：[https://pan.baidu.com/s/1i5BJZCD](https://pan.baidu.com/s/1i5BJZCD)，提取码：e2xd。

其中，文件夹的命名规律为：`厂商_云盘类型_容量`。除了 `aliyun_ssd_500x` 和 `aliyun_ssd_250x` 外，每个文件夹下均有一个 `report.pdf` 文件，为测试程序自动生成，里面包含了测试结果、数据和图表。

![](http://ww2.sinaimg.cn/large/006tNc79gw1fahgz7diayj30bk0ak0ui.jpg)

另外，笔者用 Highcharts 制作了一些可交互图表，可用来查看汇总后的各项数据。地址如下：[http://codingpy.com/specials/cbs_test/](http://codingpy.com/specials/cbs_test/)。

将数据包解压后，你会发现其中阿里云 SSD 云盘有 4 个相关的文件夹，其中两个带有 `x` 字样。这是因为这两个文件夹中的数据并不是笔者一开始希望得到的。原因大致是这样的：

笔者曾经因为账号内余额不足等多种原因，多次重新启动过对阿里云 SSD 云盘的性能测试。经过漫长的等待，最终快要完成性能对比文章时，才发现阿里云的数据只达到了预期性能的一半。这些数据显然是真实的数据，但却又让人无法相信。

最终在同事的指点下，才找到了背后真正的原因：**测试用的服务器不是 I/O 优化实例**。

所以，`aliyun_ssd_250x` 和 `aliyun_ssd_250x` 文件夹下是以非 I/O 优化实例测试得出的 SSD 性能数据。

最终，为了能够尽快给出 SSD 云盘的对比结果，笔者选择了取消对 PTS 测试中 WSAT、HIR 两项的测试（见上篇中的说明）。

## 预期性能对比

在介绍测试结果之前，我们先来比较一下两家云盘的预期性能（SSD 云盘为下图右侧部分）。

<a href="http://ww1.sinaimg.cn/large/006tNc79gw1fah1xdjyjyj31400lgwig.jpg"><img src="http://ww1.sinaimg.cn/large/006tNc79gw1fah1xdjyjyj31400lgwig.jpg" alt="两大产生云硬盘预期性能对比"></a>

上图告诉我们，**阿里云的 SSD 云盘在 IOPS 和 吞吐量指标上有一定的性能优势，只有在容量 1TB 以上时才性能略低于腾讯云**。

笔者之前就说过，预期性能不等于实际性能，二者之间很可能存在差异。那么两家厂商在 SSD 云盘上的真实差距到底有多大？我们下面用数据说话。

## 性能测试结果

首先是 250GB 容量的 IOPS、Throughput、Latency 三项指标的数据（可点击图片查看大图）：

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

500GB 容量的性能对比（可点击图片查看大图）：

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

> > 如果觉得看起来不方便，可以访问用 Highcharts 制作的交互式图表：[http://codingpy.com/specials/cbs_test/](http://codingpy.com/specials/cbs_test/)

### I/O 优化与非 I/O 优化对比

由于笔者手头上已经有了阿里云 SSD 云盘在 I/O 优化实例和非 I/O 优化实例下的性能数据，不利用一下简单可耻。虽说这样的对比可能意义不大，但至少可以让大家直观地感受到二者之间的差距具体有多少。

（下面的图片待替换。）

<table>
  <tr>
    <td style='width:50%;padding: 8px;'><a href="http://ww3.sinaimg.cn/large/006tNc79gw1fahhn43a0sj30xc0m8goo.jpg"><img src="http://ww3.sinaimg.cn/large/006tNc79gw1fahhn43a0sj30xc0m8goo.jpg" alt=""></a></td>
    <td style='width:50%;padding: 8px;'><a href="http://ww3.sinaimg.cn/large/006tNc79gw1fahhnjahjsj30xc0m80us.jpg"><img src="http://ww3.sinaimg.cn/large/006tNc79gw1fahhnjahjsj30xc0m80us.jpg" alt=""></a></td>
  </tr>
  <tr>
      <td style='width:50%;padding: 8px;'><a href="http://ww3.sinaimg.cn/large/006tNc79gw1fahho0rmjbj30xc0m8mzd.jpg"><img src="http://ww3.sinaimg.cn/large/006tNc79gw1fahho0rmjbj30xc0m8mzd.jpg" alt=""></a></td>
    </tr>
</table>


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