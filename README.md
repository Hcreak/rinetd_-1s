# rinetd_-1s
一键rinetd转发至随机端口 用于复活被墙端口

## 灵感 ##

[https://www.hostloc.com/thread-543705-1-1.html](https://www.hostloc.com/thread-543705-1-1.html)
 > HiHiHi 
 > ---
 > 推荐你个办法。mtproxy开固定端口，然后rinetd开起来转发1000-3000的端口，连不上就换一个，反正2000多个端口，最少能用好几个月。

 感谢这位名叫`HiHiHi`的大佬给我的灵感 希望墙内有这个论坛账号的朋友替我向他表示感谢

 ## 部署 ##

 * 因 github 仓库名不能有 `+` 号 请注意修改目录名称
 * 自行安装 [`rinetd`](https://github.com/boutell/rinetd) 和 `python-flask` 
 * 没有考虑认证机制 建议至少需要加 `HTTP basic auth`