---
title: 官方俩月没回复的系统Bug，我用AI几分钟破案
date: 2026-06-04
tags: [Android, Bug, AI, 调试, 小米手机, scrcpy]
description: 小米手机在使用 scrcpy 的虚拟副屏功能后，出现无法更换壁纸的诡异 Bug。官方两月无回复，老刘利用 AI (Gemini 3.5 flash) 几分钟内通过日志分析定位到 wallpaper 服务的裁剪区域 (mCropHint) 数据污染问题，并给出了一键修复方案。
---

**大家好，我是老刘**

scrcpy 3.0+引入了--new-display这一功能，允许用户在电脑上为Android手机创建一个完全独立的虚拟副屏（Virtual Display），实现类似电脑双屏协作的体验。

老刘在之前的文章中详细介绍过这种用法：

[华为小米都在布局的多屏协同，其实Android早就有了！只是你不知道...](https://mp.weixin.qq.com/s/KfDLU8TGCjqagEKXfGYRuA)

然而，老刘在自己的小米手机上发现了一个极其诡异的Bug：**当拔掉USB线或关闭scrcpy后，手机竟然无法更换壁纸了！只有重启手机才能恢复。**

老刘将问题反馈给小米官方，结果俩月过去了连个回音都没有。（难道只有买了旗舰版手机才配反馈问题？）

没办法，只能自己来定位一下这究竟是scrcpy的功能缺陷，还是小米系统的显示服务异常？

今天老刘就带大家一起看看AI在分析定位这类Bug时能起到多大的作用。

后续所有和AI的交互和对日志的分析都是基于Gemini 3.5 flash进行的。

***

## 第一阶段：直觉与推测（虚拟显示器残留？）

**【初步怀疑】**
在Android 10+架构中，创建副屏通常依赖系统的`VirtualDisplay`机制。所以直觉告诉我：是不是scrcpy断开时发生了异常，导致虚拟显示器没有被正常注销，成为了系统的残留，从而影响了某些全局显示状态？

**【验证手段】**
我问AI如何验证我的这种猜想？AI给出了如下方案：

在断开连接且壁纸卡死的状态下，通过Windows终端执行以下ADB命令，抓取系统的显示服务（`DisplayManager`）快照：

```cmd
adb shell dumpsys display
```

**【日志打脸】**
打开导出的日志，我们直接查找`Display Devices`的数量：

```text
Display Devices: size=1
  Display Id=0 (内置屏幕...)
Logical Displays: size=1
  Display 0
```

事实上没必要自己分析，直接把日志给AI就行了。

**结论**
底层的虚拟显示器实例在scrcpy关闭时已经被干净利落地销毁了。系统中并不存在残留的幻影屏幕。

***

## 第二阶段：迷雾重重（分辨率覆盖的嫌疑？）

虽然显示器被销毁了，但AI指出日志中依然有一处可疑的地方：

* 手机主屏物理规格：`1440 x 3200`（2K）
* 当前逻辑覆盖规格：`mOverrideDisplayInfo: real 1080 x 2400`

**【推测】**
AI重点怀疑这个分辨率覆盖有问题。

不过老刘有不同的意见，小米手机支持降低分辨率运行（FHD+模式恰好是1080x2400）。如果手机本身开启了FHD+，这就属于正常现象。

然后通过检查手机设置，也确认开启了FHD+模式：

![](https://gcore.jsdelivr.net/gh/lzt-code/blog-images@main/img/Screenshot_2026-06-03-17-37-45-218_com.android.settings-edit.jpg)

那么既然不是显示器残留，也不是分辨率异常，那到底是什么出问题？

***

## 第三阶段：石锤落地（捕获壁纸服务的罪证）

在AI的建议下我们直接去看小米的壁纸服务的相关信息`WallpaperManagerService`。在卡死状态下执行：

```cmd
adb shell dumpsys wallpaper
```

我大致看了一下日志没发现问题，就直接发给AI了。没想到AI敏锐的发现了问题所在：

![](https://gcore.jsdelivr.net/gh/lzt-code/blog-images@main/img/20260603174917142.png)

### 彻底错乱的裁剪区域（mCropHint）

当前的壁纸裁剪参数：

```text
Display state:
  displayId=0
  mWidth=2400  mHeight=2400
  mCropHint=Rect(0, 0 - 864, 1920) 
```

**这就是引发问题的关键证据！**

1. **什么是`mCropHint`？**
Android为了支持手机桌面左右滑动时的壁纸视差滚动，会将壁纸画布初始化为一个正方形（在1080P下为2400x2400）。而`mCropHint`则是系统指导壁纸引擎从画布中裁剪出多大区域显示在主屏上。
2. **为什么变成了864x1920？**
当你运行scrcpy --new-display 1080x2400时，由于硬件编码压力或系统缩放保护，scrcpy在底层对副屏进行了一次等比下采样（Downsample），实际创建出了一个864x1920的虚拟副屏。
3. **数据污染导致Bug爆发**
此时，**小米的壁纸组件**应该是误将虚拟的副屏分辨率参数（864x1920）错误地覆盖并缓存在了主屏的`mCropHint`变量中。

***

## 老刘猜测bug原因

小米系统因为需要支持切换不同的分辨率，因此壁纸等模块就会注册监听显示状态的变化。

比如使用类似下面的代码：

```kotlin
val displayManager = getSystemService(Context.DISPLAY_SERVICE) as DisplayManager
displayManager.registerDisplayListener(object : DisplayManager.DisplayListener {
    override fun onDisplayAdded(displayId: Int) {}
    override fun onDisplayRemoved(displayId: Int) {}
    override fun onDisplayChanged(displayId: Int) {
        // 分辨率或显示模式变化
    }
}, Handler(Looper.getMainLooper()))
```

但是当scrcpy添加了虚拟显示器后也会触发这个回调，小米壁纸的代码没有判断displayId这个参数。就会导致当虚拟副屏被创建时，壁纸组件使用虚拟副屏的参数信息来更新主屏的`mCropHint`变量。

而使用新变量裁剪的壁纸和主屏的真实分辨率不一致，就会导致壁纸无法正常显示。

***

## 一劳永逸的解决方案

既然知道了是因为小米壁纸进程（`com.miui.miwallpaper`）的bug导致的，那解决方案就非常简单了。

当你断开scrcpy发现壁纸无法更换时，保持手机连接电脑，在电脑CMD窗口中运行：

```cmd
adb shell am force-stop com.miui.miwallpaper
```

**效果**
这行命令会强制结束小米壁纸守护进程。手机屏幕会瞬间闪烁一下，随后系统会重启壁纸进程，并且使用当前最新的屏幕参数。

当然你也可以直接写一个脚本启动scrcpy，然后等个几秒后直接运行这条命令。

这样就能保证即使时直接拔掉usb线，也能正常更换壁纸了。

***

## AI定位Bug的通用思路

虽然这不是一个非常经典的bug调试场景，因为老刘自己看不到小米壁纸的源码，也没法进行debug。不过整个定位过程仍然能充分体现AI在协助定位bug过程中起到的作用。

在解决这个问题的过程中，AI扮演了至关重要的角色。但要注意，不是简单地把Bug丢给它，然后让它在消耗大量Token后给你一个似是而非的结果。

老刘总结的经验是：
1. **提出假设**
把Bug的现象和你初步的怀疑告诉AI，让它为你提供验证猜测的方案（比如抓取哪些日志）。
2. **分析日志**
把冗长的系统日志交给AI，让它去找出其中的数值异常或逻辑冲突。
这是最能体现AI价值的地方，几百k的日志你要看半小时，但是AI只需要几秒就能发现有问题的地方。
3. **闭环验证**
根据AI发现的疑点进行针对性测试，直到定位根源。

这个过程循环几次后，大概率你就能定位到任何隐晦的Bug所在。

**写在最后**

复盘这次的Bug定位过程，本质上其实是工作方式的升级。在这个AI时代，咱们程序员的核心竞争力早就不是肉眼看海量日志了，而是**提出正确问题的能力**。下次再遇到这种诡异的系统级Bug，我建议你别再一个人死磕，试试把AI当成你的结对编程搭子，让它帮你处理数据分析的脏活累活，你只负责掌控大局。

**你在开发中遇到过哪些折磨人的奇葩Bug？最后又是怎么解决的？** 欢迎在评论区和老刘吐槽交流，咱们一起避坑。

***

> 🤝 如果看到这里的同学对客户端开发或者Flutter开发感兴趣，欢迎联系老刘，我们互相学习。
>
> 🎁 点击免费领老刘整理的《Flutter开发手册》，覆盖90%应用开发场景。
>
> 🚀 [覆盖90%开发场景的《Flutter开发手册》](https://mp.weixin.qq.com/s/6FeO9IoHbEuM-vhISitUxw)

> 📂 老刘也把自己历史文章整理在GitHub仓库里，方便大家查阅。
> 
> 🔗 <https://github.com/lzt-code/blog>
