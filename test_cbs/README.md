# 200MB测试数据告诉你云存储性能有多强？

上个月，笔者对国内两大云厂商（阿里云和腾讯云）的[云服务器、云数据库和云存储三种产品做了性能评测](http://www.codingpy.com/article/a-comparison-of-qcloud-and-aliyun-products/)，算是对两家的部分计算和存储产品（数据库也可视作一种存储形式）做了简要对比。虽然评测文章在 V2EX 等社区的反馈还不错，但确实还存在不少缺失。除了不好评测的售后服务等指标外，还缺少了对其他使用更为普遍的云存储产品。

本文将对补充对其他云存储产品的性价比对比。

## 云存储产品

云存储类别下，目前两大云产商提供了以下产品：

* 块存储（阿里云、腾讯云）
* 文件存储（阿里云）
* 对象存储（阿里云、腾讯云）
* 内容分发网络（阿里云、腾讯云）
* 表格存储（阿里云）
* 归档存储（阿里云）

可以看出，**阿里云的云存储产品类别更为丰富**，云计算先行者的优势突出。

在上述六种产品中，笔者上次已经对比过对象存储。内容分发网络（CDN）测试起来花的时间又特别长，进行有意义的比较需要的数据特别大，而且目前没找到自动化的工具，因此这次不考虑测试 CDN（欢迎推荐可以自动化测试 CDN 性能的工具）。

那么剩下的两家均提供的产品，就是块存储（Block Storage）了。块存储，简单来说就是提供了块设备存储的接口，一个硬盘就是一个块设备。在云产商提供的产品中，所谓的普通云盘、高效云盘、SSD 云盘，都是块存储设备。

[上一篇评测文章](http://www.codingpy.com/article/a-comparison-of-qcloud-and-aliyun-products/)中，其实也对普通云盘的性能进行了对比，但被包含在云服务器性能测试中。对于选择普通云盘做对比，有的读者也提出了异议。

![V2EX 读者评论](http://ww3.sinaimg.cn/large/006tNc79gw1fafsl3flr9j30pe058my1.jpg)

确实，企业用户一般不会用虚拟机自带的云盘来存储数据，因为本地磁盘的数据迁移困难，而自建 raid 磁盘阵列的数据持久性又不高，因此大多采用 SSD 云盘或高效云盘。一线云厂商比拼的也主要是分布式块存储。

为了较为完整地比较两大厂商的块存储产品，笔者近期对两家的高效云盘和 SSD 云盘进行了压测，算是对[上一篇](http://www.codingpy.com/article/a-comparison-of-qcloud-and-aliyun-products/)的补充。期间犯了不少错，多花了不少冤枉钱，不过总算最终得出了比较可信、直观的数据。

如果你对存储类型不太熟悉，建议阅读以下文章：

* [从OpenStack的角度看块存储的世界](http://www.infoq.com/cn/articles/block-storage-overview)
* [三种存储类型比较-文件、块、对象存储](http://limu713.blog.163.com/blog/static/15086904201222024847744/)
* [知乎话题：块存储、文件存储、对象存储这三者的本质差别是什么？](https://www.zhihu.com/question/21536660)

## 厂商预期的性能

在介绍测试详情之前，先来看一看厂商对自家产品的描述。

在各自的产品介绍页面（[腾讯云](https://www.qcloud.com/product/cbs.html?idx=2)、[阿里云](https://www.aliyun.com/product/disk?spm=5176.8142029.388261.46.NEXakN)），均给出了详细的性能指标及具体的计算公式。

- 阿里云：
    - 高效云盘
        * IOPS：`min(1000 + 6 * 容量, 3000)`
        * 吞吐量：`min(50 + size * 0.1, 80)`
        * 访问时延：1-3ms
    - SSD 云盘
        * IOPS：`min(30 * 容量, 20000)`
        * 吞吐量：`min(50 + size * 0.5, 256)`
        * 访问时延：1-3ms
- 腾讯云：
    - 高效云盘
        * IOPS：`min(1500 + 容量 * 8, 4500)`
        * 吞吐量：`min(75 + size * 0.147, 130)`
        * 访问时延：< 3ms
    - SSD 云盘
        * IOPS：`min(容量 * 24, 2400)`
        * 吞吐量：`min(150 + (容量 - 250) * 0.147, 260)`
        * 访问时延：< 3ms

其中：

- IOPS：每秒读写(I/O)操作的次数，数值越高越好。
- 吞吐量：一般用MBPS，每秒传输的MB字节数来衡量，下文用英文 Throughput 替代。
- 访问时延：访问时延，完成一个 I/O 请求所需的时间，下文用英文 Latency 替代。

上述三项指标中，两家只给出了 Latency 的数值范围。不过，这个可以说是最重要的性能指标。其他指标不变的情况下，Latency 为 1ms 的性能是 3ms 的 3 倍。

另外，从给出的计算公式中，无法直观地比较 IOPS、TP。因此，笔者用绘制了云盘性能与容量（volume）的关系图。

<a href="http://ww1.sinaimg.cn/large/006tNc79gw1fah1xdjyjyj31400lgwig.jpg"><img src="http://ww1.sinaimg.cn/large/006tNc79gw1fah1xdjyjyj31400lgwig.jpg" alt="两大产生云硬盘预期性能对比"></a>

上图中，**红色虚线为腾讯云云盘，蓝色实线为阿里云云盘**。

由于腾讯云的云盘最大容量为 4000GB，而阿里云为 32678GB，但是为了图片适宜比较，只绘制出了容量在 `[0, 4000]` 范围内的性能数据。另外，高效云盘在图中以 Hybrid 代称， 下文同。

从上图来看：

- **腾讯云高效云盘的预期性能遥遥领先于阿里云**，尤其是最低吞吐量都比阿里云的峰值要高；
- 但是在 SSD 云盘方面，**阿里云的预期性能优势比较大，只有在容量 1TB 以上时才低于对手**。

**不过，以上只是厂商预期的性能数据，不代表产品的真实性能就是如此**。产品实际表现如何，与预期性能差距有多大，还需要我们亲自测试、使用才可得知。

## 测试准备工作

在开始测试之前，笔者在两家产商分别购买了测试服务器及云盘。

测试所使用的虚拟机配置为：

- CPU：4核 Intel Xeon
- 内存：4GB DDR3
- 操作系统：Ubuntu 14.04 64位。

选取的测试云盘如下：

- 高效云盘：50GB、400GB
- SSD 云盘：250GB、500GB

> 测试阿里云的 500GB SSD 云盘时碰到了两个大杯具，首先是余额不足导致测试程序中断，一切重来。。第二个杯具和 SSD 云盘的性能有关，具体下文中会提到。。。

下文中，笔者不会具体介绍测试步骤，只说明执行了哪些测试及测试结果，具体步骤请看此前在 Github 上分享的项目：[CloudTesting/test_cbs](https://github.com/bingjin/CloudTesting)。

## 执行哪些测试

一般来说，块存储性能主要看 **IOPS、Throughput 和 Latency**三个指标，厂商也大多提供这三个指标的峰值作为购买参考。

[上一篇评测](http://www.codingpy.com/article/a-comparison-of-qcloud-and-aliyun-products/)中，笔者就是使用 fio 对普通云盘进行测试，对比了三个指标的差异。不过现在回过头来看，**测试的压力还不够大，使用的块大小、队列深度还不够全，虽然最终结果差异或许并不会太大**。

因此，这次针对高效云盘（HDD+SSD）和 SSD 云盘的测试，笔者将根据 SNIA 发布的[企业级SSD评测规范（Solid State Storage Performance Test Specification Enterprise v1.1）](http://snia.org/sites/default/files/SSS_PTS_Enterprise_v1.1.pdf)进行，以下简称该规范为 PTS 。

SNIA 是存储网络行业协会(Storage Networking Industry Association，SNIA)的简称，这是一个由厂商和大学成立的行业组织，致力于开发和推广存储系统标准。

除了 IOPS、Throughput 和 Latency 三项基础测试外，PTS 还包含了以下五种测试：

* Write Saturation (WSAT)：持续应用工作负载，测试性能随着时间如何变化。
* Demand Intensity Response Time Histograms (DIRTH)
* Cross Stimulus Recovery (XSR)
* Host Idle Recovery (HIR)：测试宿主机闲置时间对性能恢复的影响。
* Enterprise Composite Workload (ECW)

SNIA 官方有提供测试服务，但是收费，而且也不适用于云存储设备。

因此，笔者选择了一家云计算公司根据 PTS 规范实现的自动化测试库（代码地址：[https://github.com/cloudharmony/block-storage](https://github.com/cloudharmony/block-storage)），其中包含了 IOPS、TP、Latency、WSAT 和 HIR 五类测试，其他的没有实现。

> SSD 云盘的测试中没有 WSAT 和 HIR 两项，具体原因后面会提到。

注意，PTS 测试中所有 fio 命令的队列深度均为 64。具体测试细节请看官方提供的 [PDF](http://snia.org/sites/default/files/SSS_PTS_Enterprise_v1.1.pdf) 文件。

#### PTS 测试耗时长

根据 PTS 规范，每项 SSD 性能测试需要经过**1、净化、2、准备工作负载、3、进入稳态、4、测试等四个环节，因此整个测试过程用时非常长，而且云盘容量越大，耗时越长。

以腾讯云 500G SSD 云盘的测试时间为例说明：

<a href="http://ww4.sinaimg.cn/large/006tNc79gw1fafuzvt59sj30z208sjtj.jpg"><img src="http://ww4.sinaimg.cn/large/006tNc79gw1fafuzvt59sj30z208sjtj.jpg" alt="测试时长说明"></a>

**此次测试采用的是第三方提供的自动化测试库，整个步骤都是可重复的，对测试数据有疑问的同学可自行验证。**在这里说明下测试所需时间，是**为了提示大家启动测试程序后该干嘛就干嘛，同时保证账户中有充足的余额（尤其是后者）**。

在介绍测试结果之前，说明一下对两家厂商测试过程的差异（云盘均为直接格式化，未分区）。

- 腾讯云由于不支持单独购买按量付费的服务器，因此是开的 4 台 VM，与 VM 一起购买云盘。
- 阿里云支持单独按量购买云盘，因此只开了 2 台 VM，每台挂载 2 块云盘，测试时针对每个云盘单独启动一个测试程序。

## 性能测试数据

经过漫长的时间，上周末终于完成了对 6 块云盘的 IOPS、TP、Latency、WSAT、HIR 五项测试。

测试数据大约 190MB，下载地址为：[https://pan.baidu.com/s/1i5BJZCD](https://pan.baidu.com/s/1i5BJZCD)，提取码：e2xd。其中，文件夹的命名规律为：`厂商_云盘类型_容量`。除了 `aliyun_ssd_500x` 和 `aliyun_ssd_250x` 外，每个文件夹下均有一个 `report.pdf` 文件，为测试程序自动生成，里面包含了测试结果、数据和图表。

另外，笔者用 Highcharts 制作了一些可交互图表，可用来查看汇总后的各项数据。地址如下：[http://codingpy.com/specials/cbs_test/](http://codingpy.com/specials/cbs_test/)。

## 阿里云的一个大坑

笔者在本文撰写快要结束时，看到阿里云 SSD 云盘的性能比预期的差很多，回头去调查原因。这才猛然发现**阿里云 SSD云盘必须搭配 I/O 优化实例才能给发挥最大性能**。当时就想破口大骂。。。

踩过这个坑的朋友不知道有多少？

![阿里云 SSD云盘必须搭配 I/O 优化实例](http://ww2.sinaimg.cn/large/006tNc79gw1fag7ria7i9j30yw0citbe.jpg)

因此，之前的 SSD 云盘数据（即 `aliyun_ssd_500x` 和 `aliyun_ssd_250x` 两个文件夹下的数据）就不具备可比性了。笔者只好重开 ECS 进行测试，为了节约时间，**SSD 云盘将只测试 IOPS、Throughput、Latency 这三个基础指标**。

本文先对比高效云盘，重新测试完后，过几日再与大家分享具体的 SSD 云盘性能对比。

## 高效云盘性能对比

下面我们来看看高效云盘的测试性能，与产商预期的性能值之间是否存在差异，差异又有多大。

先来回顾一下厂商预期的性能，请看下图左边部分。

<a href="http://ww1.sinaimg.cn/large/006tNc79gw1fah1xdjyjyj31400lgwig.jpg"><img src="http://ww1.sinaimg.cn/large/006tNc79gw1fah1xdjyjyj31400lgwig.jpg" alt="两大产生云硬盘预期性能对比"></a>

上图显示，**腾讯云高效云盘的预期性能遥遥领先于阿里云**，其中最低的吞吐量都比阿里云的峰值要高。

但是真实测试数据如何？请看下面的测试结果。

### 基础指标测试

首先是 50GB 容量的 IOPS、Throughput、Latency 三项指标的数据（可点击图片查看大图）：


<table>
  <tr>
    <td style='width:50%;padding: 8px;'><a href="http://ww4.sinaimg.cn/large/006tNc79gw1fagx5ncp9nj30xc0m841a.jpg"><img src="http://ww4.sinaimg.cn/large/006tNc79gw1fagx5ncp9nj30xc0m841a.jpg" alt=""></a></td>
    <td style='width:50%;padding: 8px;'><a href="http://ww2.sinaimg.cn/large/006tNc79gw1fagx6a4pk6j30xc0m8wga.jpg"><img src="http://ww2.sinaimg.cn/large/006tNc79gw1fagx6a4pk6j30xc0m8wga.jpg" alt=""></a></td>
  </tr>
  <tr>
      <td style='width:50%;padding: 8px;'><a href="http://ww3.sinaimg.cn/large/006tNc79gw1fagx6o9qksj30xc0m8jt8.jpg"><img src="http://ww3.sinaimg.cn/large/006tNc79gw1fagx6o9qksj30xc0m8jt8.jpg" alt=""></a></td>
    </tr>
</table>

400GB 容量的性能对比（可点击图片查看大图）：

<table>
  <tr>
    <td style='width:50%;padding: 8px;'><a href="http://ww4.sinaimg.cn/large/006tNc79gw1fagx717ku9j30xc0m841e.jpg"><img src="http://ww4.sinaimg.cn/large/006tNc79gw1fagx717ku9j30xc0m841e.jpg" alt=""></a></td>
    <td style='width:50%;padding: 8px;'><a href="http://ww3.sinaimg.cn/large/006tNc79gw1fagx7c3wz6j30xc0m8abt.jpg"><img src="http://ww3.sinaimg.cn/large/006tNc79gw1fagx7c3wz6j30xc0m8abt.jpg" alt=""></a></td>
  </tr>
  <tr>
      <td style='width:50%;padding: 8px;'><a href="http://ww3.sinaimg.cn/large/006tNc79gw1fagx7rhjofj30xc0m8765.jpg"><img src="http://ww3.sinaimg.cn/large/006tNc79gw1fagx7rhjofj30xc0m8765.jpg" alt=""></a></td>
    </tr>
</table>


<small>图注：RW Ratio 指的是 I/O 操作中的读写比例，0/100 表示顺序写, 100/0 表示顺序读。</small>

从上述图表对比来看， 可以得出结论1：

**在 50GB、400GB 两个容量级别上，腾讯云高效云盘的各项性能指标表现均优于阿里云，而且优势也比较明显**。

接下来，我们比较一下测试值与预期值之间的差异。由于预期值都是理论情况下的峰值，我们从测试数据中提取出各自的峰值。

<a href="http://ww2.sinaimg.cn/large/006tNc79gw1fag01yvq5hj314y0fqq6e.jpg"><img src="http://ww2.sinaimg.cn/large/006tNc79gw1fag01yvq5hj314y0fqq6e.jpg" alt="高效云盘性能对比"></a>

看完上面的数据，你至少会有这两个疑惑：

1. **腾讯云的测试峰值怎么接近预期值的两倍？**
2. **阿里云 400GB 高效云盘的延迟怎么那么高，离预期的 1-3ms 差距很大？是不是数据有误？**

第一个疑惑，腾讯云两个容量的测试峰值均为预期值的两倍。产品首页中没有直接说明，只能去翻产品文档，最终在 [CBS 使用约束页面](https://www.qcloud.com/document/product/362/5145)中找到了一段解释：

> 产品文档中承诺的IO性能，如1TB的SSD云硬盘，随机IOPS能达到24000IOPS。含义是读写可同时达到24000IOPS，4KB/8KB的 IO都可做到，16KB的IO大小，则无法做到24000（由于吞吐已经达到了260MB/s的限制）。

简单来说，就是**腾讯云高效云盘的读写操作可同时达到预期性能峰值（数据块 16KB 以下）**。这样，腾讯云的数据就可以解释的通了。

笔者选择的测试峰值是数据块 512b、50/50 读写比例下的数据，这时读写均达到了预期的 IOPS 峰值，总 IOPS 接近预期峰值的 2 倍。而顺序读、顺序写的值都接近预期的峰值。

而**阿里云方面，读写无法同时达到预期性能峰值**。

第二个疑惑，阿里云 50GB 高效云盘的 Latency 在正常范围，怎么 400GB 的就超标了？笔者一开始还以为数据错了，为此重开了虚拟机，用 ioping 做了简单的比对。结果如下图：

<a href="http://ww4.sinaimg.cn/large/006tNc79gw1fagvbj5ihxj312q0vc7fn.jpg"><img src="http://ww4.sinaimg.cn/large/006tNc79gw1fagvbj5ihxj312q0vc7fn.jpg" alt="高效云盘Latency对比"></a>

重新测试之后，笔者确信了此前自动测试库跑出的数据应该是没问题的。**至于高时延背后的原因，可能是“邻居”比较多、IO 操作比较活跃吧。** Latency 的自动测试大概跑了 4 个多小时，重新测试时性能也没有变化，阿里云这个算不算违反了服务协议（SLA）呢？

解决上面的疑惑之后， 我们可以得出以下结论：

- **结论2：腾讯云达到了预期的性能；阿里云部分没有达到，400GB 容量的时延过高。**
- **结论3：腾讯云高效云盘的时延在 1ms 以下，IOPS、吞吐量的优势更加突出。**

### WSAT、HIR

下面来看 WSAT 和 HIR 测试的情况。上面提到，WSAT测试是指在持续应用工作负载，测试性能随着时间如何变化。

WSAT 自动测试最终得出的是一段时间内，IOPS 的平均值，结果如下：

<a href="http://ww2.sinaimg.cn/large/006tNc79gw1fag0ivl80oj30y8036aal.jpg">
<img src="http://ww2.sinaimg.cn/large/006tNc79gw1fag0ivl80oj30y8036aal.jpg" alt="WSAT 测试">
</a>

上述数据，与两家厂商预期的峰值非常接近，说明两家的高效云盘能够长时间达到 IOPS 性能峰值。但是这里看不出性能如何随时间变化，必须从生成的 PDF 中查找，笔者截图如下：

<a href="http://ww4.sinaimg.cn/large/006tNc79gw1fagw5zhogyj30xc0p0adi.jpg"><img src="http://ww4.sinaimg.cn/large/006tNc79gw1fagw5zhogyj30xc0p0adi.jpg" alt="四种云盘 WSAT 测试"></a>

从上述 4 张趋势图来看，可以得出结论4：

**两家高效云盘的 IOPS 表现均比较稳定，几乎呈一条直线，只有阿里云的 400GB 云盘有些略微波动**。

最后来比较 HIR 测试的结果。HIR 主要测试宿主机闲置时间对性能恢复的影响。

<a href="http://ww1.sinaimg.cn/large/006tNc79gw1fagw6gjipoj30xc0p00x5.jpg"><img src="http://ww1.sinaimg.cn/large/006tNc79gw1fagw6gjipoj30xc0p00x5.jpg" alt="四种云盘 HIR 测试"></a>

从上述 4 张趋势图来看，可以得出结论5：

**容量越大，似乎闲置时间对性能恢复的影响越明显；阿里云 400GB 高效云盘的性能波动受闲置时间影响较明显。**

综合上述五项测试的结果，可以认为**腾讯云高效云盘的综合性能应该是阿里云高效云盘的2倍以上**（结论6）。

### 加入价格因素

延续[上一篇](http://www.codingpy.com/article/a-comparison-of-qcloud-and-aliyun-products/)的风格，在比较完性能指标之后， 我们再加入价格因素。

<a href="http://ww4.sinaimg.cn/large/006tNc79gw1fagwlnfsvkj310w06iabb.jpg"><img src="http://ww4.sinaimg.cn/large/006tNc79gw1fagwlnfsvkj310w06iabb.jpg" alt="高效云盘价格对比"></a>

上图中，腾讯云高效云盘按量计费的价格，为根据[官方产品页面](https://www.qcloud.com/product/cbs?idx=2)给出的定价计算，包年包月价格为单独购买云盘时系统显示价格；阿里云高效云盘的价格根据[其给出的费用规则](https://www.aliyun.com/price/product?spm=5176.54360.203004.4.hoqhjj#/disk/detail)计算。这里说明一点，腾讯云在单独购买云盘时，还只有包年包月这种模式，不够灵活。

从上图对比来看：

- 结论7：腾讯云和阿里云的包年包月价格相同；
- 结论8：腾讯云的按量计费价格比阿里云贵，约为 1.8 倍；
- 结论9：阿里云按量计费与包年包月的价格相差很小。

一般来说，数据盘中存储的多为持久性数据，以按量付费方式购买的企业用户应该并不多。所以，**在包年包月模式下，腾讯云高效云盘的性价比非常高**。

不过由于阿里云两种模式之间价格差异小，使得用户在云盘使用方式上更加灵活。**在笔者看来，按量计费和包年包月的核心并不在如何收费，而在于云计算产品的使用方式。价格差会使用户倾向于以某一种方式使用产品，而不是根据有业务情况自由选择。**

## 结语

上文中，我们分别从 IOPS、Throughput、Latency、WSAT、HIR 五项测试指标，对腾讯云、阿里云的 50GB、400GB 容量的高效云盘进行了性能对比。

经过对测试数据进行分析，笔者主要得出了以下结论：

1. **腾讯云高效云盘的各项基础性能指标均优于阿里云，且优势明显；**
2. **腾讯云高效云盘达到了预期的性能，而阿里云部分云盘没有达到，400GB 容量的时延过高；**
3. **阿里云大容量高效云盘的 IOPS 性能受宿主机闲置影响较大；**
4. **包年包月模式下，腾讯云高效云盘的性价比非常高；**
5. **阿里云高效云盘不同计费模式下费用差别不大，选择时灵活性更高。**

如果你正在考虑采购这两家产商的高效云盘，希望本文对你有帮助。如果你考虑的厂商不是腾讯云或阿里云，可以参考本文中使用的自动测试库进行全面测试。不过别忘了，要想获得最大的云盘性能，则必须购买相应厂商的云服务器，否则云应用的性能反而可能下降。关于如何测试云服务器的性能，请看笔者[上一篇评测](http://www.codingpy.com/article/a-comparison-of-qcloud-and-aliyun-products/)。

下一篇笔者将对比腾讯云和阿里云 SSD 云盘的性能。

## 参考链接

* [云存储的四大优势](http://tech.hnr.cn/yjs/2015/1117/38468.html)
* [从OpenStack的角度看块存储的世界](http://www.infoq.com/cn/articles/block-storage-overview)
* [SNIA SSS Performance Test Specification (PTS) Testing Service](http://www.snia.org/forums/sssi/ptstest)
* [网络存储协会发布企业级SSD评测规范](http://storage.it168.com/a2011/0811/1231/000001231318.shtml)
* [阿里云：云盘参数和性能测试方法](https://help.aliyun.com/document_detail/25382.html)
* [阿里云：云盘的特点和应用场景](https://help.aliyun.com/document_detail/25383.html?spm=5176.doc25382.6.550.dSYhIM)
* [腾讯云：如何衡量云硬盘的性能](https://www.qcloud.com/document/product/362/6741)
* [腾讯云：CBS 应用场景](https://www.qcloud.com/document/product/362/3065)
* [腾讯云：CBS 产品分类及对比](https://www.qcloud.com/document/product/362/2353)

* [块存储测试套件](https://github.com/cloudharmony/block-storage)
* [Key storage performance metrics for virtual environments](http://www.computerweekly.com/feature/Key-storage-performance-metrics-for-virtual-environments)
* [Pro Tips For Storage Performance Testing](http://blogs.vmware.com/virtualblocks/2015/08/12/pro-tips-for-storage-performance-testing/)
* [Understanding IOPS, Latency and Storage Performance](http://louwrentius.com/understanding-iops-latency-and-storage-performance.html)



* [Amazon EBS 卷类型](http://docs.aws.amazon.com/zh_cn/AWSEC2/latest/UserGuide/EBSVolumeTypes.html)
* [AWS系列之三 使用EBS](http://www.cnblogs.com/huang0925/p/3879542.html)
* [AWS 存储测试数据](https://blog.sungardas.com/CTOLabs/2015/09/storage-performance-benchmarking-on-aws/)





