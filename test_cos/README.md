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
