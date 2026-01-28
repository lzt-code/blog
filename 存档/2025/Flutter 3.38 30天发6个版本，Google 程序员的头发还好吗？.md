**大家好，我是老刘**

最近如果你盯着 Flutter 的 release 页面会发现，从 11月12日 到 12月11日，短短 30 天内，Flutter 官方竟然一口气更新了 6 个版本！

平均 5 天一个版本，最夸张的时候，两个补丁版本的间隔甚至不到 24 小时。比我提交代码到 dev 分支还要勤快。

![](https://files.mdnice.com/user/142171/bd52fb8c-3fa6-4531-90dc-55ba20b8f015.png)

看着 3.38.x 的版本号一路狂飙，真心想问问：Google 程序员的头发还好吗？

## 这些版本到底修了啥？

下面整理了 Flutter 3.38 各个小版本的更新内容 


### Flutter 3.38.5
**发布日期** ：2025年12月13日   
**修复内容** ：
- flutter/179700 ：将 Dart SDK 更新至 3.10.4 版本。

### Flutter 3.38.4
**发布日期** ：2025年12月5日  
**修复内容** ：
- flutter/178547 ：修复 Linux 桌面端使用 Skia 渲染器时的渲染问题。
- flutter/178529 ：修复运行 debug web 时 AppLocalizations 被意外删除的问题。
- flutter/178660 ：修复当 .dart_tool 目录结构不完整时， flutter widget-preview start 崩溃的问题。
- flutter/175227 ：修复 Flutter Web 应用在 Chrome 中启动时显示 --no-sandbox 警告的问题。
- flutter/179155 ：修复项目外部 pubspec.yaml 变动导致 Widget Previewer 崩溃的问题。
- flutter/156692 ：修复目标应用意外断开连接导致 flutter attach 崩溃的问题。
- flutter/179008 ：修复 macOS 上根项目运行 pub get 后，外部 pubspec.yaml 变动导致重复 spawn pub get 的问题。
- flutter/178715 ：修复 Linux/macOS 上缺少桌面工具时，对 Android 项目运行 flutter test 失败的问题。

### Flutter 3.38.3
**发布日期** ：2025年11月22日   
**修复内容** ：
- flutter/178772 ：修复 Flutter Engine 报告的版本号与 Framework 版本不一致的问题。
- flutter/178804 ：将 Dart SDK 更新至 3.10.1 版本。

### Flutter 3.38.2
**发布日期** ：2025年11月19日   
**修复内容** ：
- flutter/178472 ：修复分析 Dart 文件变更过程中退出 Widget Previewer 导致崩溃的问题。
- flutter/178452 ：修复 add-to-app 场景下 iOS 构建报错 "Improperly formatted define flag" 的问题。
- flutter/178486 ：修复禁用 Web 支持时启动 Widget Previewer 抛出异常的问题。
- flutter/178317 ：修复插件依赖变更时运行 flutter pub get 导致 Widget Previewer 崩溃的问题。
- flutter/178318 ：修复单一进程崩溃提交多个崩溃报告的问题。
- flutter/176399 ：修复编译 Windows 桌面应用时不支持 Visual Studio 2026 的问题。
- flutter/175058 ：修复目标项目未运行 pub get 时 Widget Previewer 启动失败的问题。
- flutter/178421 ：修复 IDE 调试物理 iOS 26 设备时应用启动卡白屏的问题。

### Flutter 3.38.1
**发布日期** ：2025年11月14日   
**修复内容** ：
- flutter/178400 ：正式添加对 Dart 3.10 stable 版本的支持。

### Flutter 3.38.0
**发布日期** ：2025年11月13日   
- 初始稳定版本发布 ：包含该周期的所有新特性（如对 iOS 26 的支持、Dart 3.10 新语法支持、Widget Previewer 改进等）。

**总结一下**

这一个月，Flutter 团队基本上就是在**修 Widget Previewer -> 升 Dart -> 修各平台兼容性**这个循环里狂奔。

---

## Flutter 3.38还处于观察期

老刘之前在很多场合都反复强调过一个“防坑指南”：**一个新的 Flutter 版本发布后，至少要观察两个月，等它基本稳定了，没有什么大问题了，再考虑升级。**

看看 3.38 这一个月的表现，完全验证了老刘的这个观点。30 天 6 个版本，这频率虽然感人，但也意味着这个版本目前还非常不稳定。尤其是这次更新涉及到了Dart SDK 的升级，很容易牵一发而动全身。

对于我们在公司里维护的商业项目，**稳定永远是第一位的**。你抢先升级，大概率会遇到各种编译失败、工具崩溃（比如上面提到的 Previewer 各种崩）、甚至运行时的诡异 Bug。到时候为了修这些非业务逻辑的 Bug，加班掉头发的可是你自己。

所以，老刘真心建议：**先别动**。让 3.38 再“飞”一会儿。等它发到 3.38.8 甚至出了 3.39，社区里的坑都被填得差不多了，才是我们入场的最佳时机。现在，就静静地看着 Google 的大佬们表演（修 Bug）就好。

---

## 总结：别慌，这是好事（大概）

看到这里，可能很多同学心里会犯嘀咕：Google 这么着急发版，是不是 Flutter 要凉或者质量不行？

其实大可不必惊慌。老刘觉得，这反而是好事。

熟悉 Flutter 的老朋友都知道，这属于“传统保留节目”了。

几乎每一个大版本发布后，都会紧跟着一串小补丁，这恰恰说明 Google 依然在重兵投入 Flutter，发现问题解决问题的速度极快。

![3.16出了9个小版本](https://files.mdnice.com/user/142171/b5e5581e-d36f-49d6-b8ff-753f6b96498f.png)


毕竟，只有亲儿子才会得到如此细致（虽然有点急躁）的照料，没人会给弃子这么勤快地修 Bug。

所以，看着版本号飙升，我们应该感到欣慰。

这每一个版本号背后，都是 Google 工程师奋斗的里程碑（和献祭的头发）。

只要 Flutter 还在变好，还在快速迭代，这点头发掉了就掉了罢——反正掉的是他们的，我们坐享其成，挺好。


> 如果看到这里的同学对客户端开发或者Flutter开发感兴趣，欢迎联系老刘，我们互相学习。
>
> 点击免费领老刘整理的《Flutter开发手册》，覆盖90%应用开发场景。
>
> 可以作为Flutter学习的知识地图。
>
> [覆盖90%开发场景的《Flutter开发手册》](https://mp.weixin.qq.com/s?__biz=MzkxMDMzNTM0Mw==&mid=2247483665&idx=1&sn=56aec9504da3ffad5797e703c12c51f6&chksm=c12c4d11f65bc40767956e534bd4b6fa71cbc2b8f8980294b6db7582672809c966e13cbbed25#rd)
