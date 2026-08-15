---
title: Flutter 3.47 更新要点：Material 正式分家，老项目先别急着更新
date: 2026-08-15
tags:
  - Flutter
  - 版本更新
  - 跨平台开发
  - Impeller
description: Flutter 3.47正式发布：material_ui独立包1.0、Impeller桌面端全量默认、iOS最低版本升到15、UIScene强制迁移。老刘带你拆解哪些变化必须现在处理，哪些可以再等等。
---

**大家好，我是老刘**

Flutter 3.47发布了。

每次大版本出来，评论区问得最多的都是：有啥新功能？性能提升多少？

这次老刘想提醒你换个角度看。3.47里的好几项变化，压根不算新功能，更像一场搬家。Material搬家、渲染引擎换岗、iOS生命周期换规则。

新功能决定你想不想升级，搬家决定你不得不升级。

今天老刘就带大家把Flutter 3.47里真正影响干活的要点盘点一遍，哪些必须现在动手，哪些可以再等等，一次说清楚。

***

## 一、核心要点速览

官方Flutter 3.47博客： <https://flutter.dev/blog/whats-new-in-flutter-3-47>

- **`material_ui` 和 `cupertino_ui` 独立包发布 1.0**：设计系统与核心 SDK 正式解耦
- **Impeller 桌面端默认启用**：macOS、Windows、Linux 全面切换到新一代渲染引擎
- **为 Xcode 27 / iOS 27 / macOS 27 做准备**：最低系统版本要求提升
- **Flutter Widget Previews 转正**：组件预览功能进入稳定版
- **Wasm 默认化持续推进**：Web 应用向 WebAssembly 迁移

***

## 一、Material、Cupertino正式分家

3.44的时候老刘就说过，官方要把Material和Cupertino从核心SDK里抽出来。当时还只是冻结代码，这次是真搬出去了：`material_ui`和`cupertino_ui`两个独立包在pub.dev上发布了1.0版本。

![](https://flutter.dev/assets/decoupling_localization.8c2083ef8687b4dbcc10aeb5745ee054.png)

**分家图什么**

以前设计组件捆在SDK里，改个按钮都得等Flutter发版。现在独立成包之后：

- 组件可以单独更新，不用拖着整个SDK一起走
- 社区贡献和修复能更快落地，官方计划每周发版
- 也为将来做一个风格中立的核心组件库铺了路

**怎么迁移**

官方给了一键迁移命令：

```bash
dart fix --apply --code=migrate_design_widgets
```

它会自动把`package:flutter/material.dart`和`package:flutter/cupertino.dart`的导入换成新的独立包。

这里有个坑要提一下：迁移工具早期有个bug，可能更新`pubspec.yaml`失败。真遇上了也别慌，手动执行`flutter pub add material_ui`（以及`cupertino_ui`），再跑一遍`dart fix --apply`就行。

**依赖没跟上怎么办**

官方也想到了半迁移状态的问题，提供了`MaterialUiCompatibilityBridge`。就算你的某些依赖还在用旧的核心SDK导入，应用也能先切到独立包：

```dart
import 'package:material_ui/material_ui.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF6750A4)),
      ),
      builder: (BuildContext context, Widget? child) {
        return MaterialUiCompatibilityBridge(child: child!);
      },
      home: const HomeScreen(),
    );
  }
}
```

**本地化也跟着拆了**

`flutter_localizations`也被拆分，Material和Cupertino的本地化委托分别移进了对应的包。

迁移前：

```dart
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:flutter/material.dart';

localizationsDelegates: const <LocalizationsDelegate<dynamic>>[
  GlobalCupertinoLocalizations.delegate,
  GlobalMaterialLocalizations.delegate,
  GlobalWidgetsLocalizations.delegate,
],
```

迁移后：

```dart
import 'package:material_ui/material_ui.dart';

localizationsDelegates: GlobalMaterialLocalizations.delegates,
```

一行顶三行，`GlobalMaterialLocalizations.delegates`会自动带上Cupertino和Widgets的委托，反而更省事了。

**时间节点要记牢**

核心SDK里的旧设计库，计划在11月的秋季稳定版正式弃用。如果你在维护生态插件，请把这次迁移当成major release级别的变更来对待，别等用户来催。

**老刘的看法**

3.44那会儿我担心过碎片化，怕重演Android组件库分家后的乱象。这次看下来，官方至少把功课做在前面了。

上次我说迁移工具到时候都会配齐，现在这话兑现了。真到动手那天，AI加官方工具一起上，手工修改这种费力不讨好的情况 基本就不存在了。

***

## 二、Impeller桌面端全量默认

这是本次更新里对桌面开发者影响最大的一项：macOS、Windows、Linux三个桌面平台，默认渲染引擎全部换成Impeller。

**Impeller是什么来头**

它是Flutter的下一代渲染引擎，用来替代Skia。最大的卖点是把着色器编译挪到了构建期，固定的着色器集提前编译好，首次播动画时那种莫名其妙的掉帧（shader compilation jank）直接从根上消灭了。

平台后端上，macOS走Metal，Windows和Linux走Vulkan。

另外Impeller在桌面端用SDF（Signed Distance Function）渲染文字，桌面文字和矢量曲线会比之前更清晰，做桌面工具类应用的同学应该能直观感受到。

**想临时退回去也行**

万一你的项目在Impeller下出了问题，三个平台都留了后门：

- **macOS**
`Info.plist`里把`FLTEnableImpeller`设成`false`
- **Windows**
`main.cpp`里加`project.set_impeller_switch(flutter::ImpellerSwitch::Disabled)`
- **Linux**
`my_application.cc`里调用`fl_dart_project_set_enable_impeller(project, FALSE)`

注意，这些回退选项未来会被移除。如果你的项目必须退回Skia才能跑，请一定去给官方提bug，这是你唯一的发声窗口。

**老刘的看法**

Impeller本质上是一套自渲染引擎，直接指挥GPU画图。这条路的好处是界面在每个平台上完全一致，没有中间桥接的性能损耗。

原先我们说Flutter自带渲染引擎，更多的是指flutter的framework，但它并非真正的渲染层，而是一个UI图形框架。真正的渲染这一步仍然是交给各个平台自己的渲染引擎，比如skia。不同平台的底层还是会有差异。

现在终于在这个层面也统一了。

之前Impeller一直在移动端打磨，这次敢在桌面三个平台全量默认，说明官方对质量心里有底了。做桌面端的同学，这个版本值得你认真实测一轮，尤其是文字渲染和动画流畅度。

***

## 三、Apple平台：最低版本提升，UIScene成必答题

这一节是iOS开发者的重点，也是全文最没有商量余地的一节。

**最低系统版本提升**

| 平台 | 旧最低版本 | 新最低版本（Flutter 3.47+） |
|------|-----------|---------------------------|
| iOS | 13 | **15** |
| macOS | 10.15 | **12** |

iOS 13到14的用户这下真覆盖不到了，发版前记得评估一下自己的用户分布。

**UIScene生命周期强制迁移**

iOS 27 SDK强制所有UIKit应用采用`UIScene`生命周期。用Xcode 27构建、又没适配`UIScene`的应用，直接无法启动。

好消息是，大多数应用由Flutter CLI在构建时自动完成迁移。

坏消息是，如果你的`AppDelegate`里写过自定义原生代码，或者用了依赖旧生命周期的插件，这部分得手动处理。

这事老刘从7月就开始念叨了，当时叫它9月大限。现在3.47把工具链准备好了，事情反而简单了：只要你还要往App Store发版，这道题就没有绕过去的选项，只剩早做晚做的区别。

***

## 四、Intel Mac退场，SwiftPM冲刺收尾

**Intel Mac进入淘汰倒计时**

官方已经停止在Intel硬件上跑自动化测试了。在Intel主机上构建，或者构建双架构包，CLI会打印警告。未来某个版本，警告会升级成错误。

还在用Intel Mac当主力机的同学，换机计划可以提上日程了。

话说这是一个向老板要新电脑的绝佳理由。

**SwiftPM迁移进度92/100**

前100个iOS插件里，已经有92个完成了Swift Package Manager迁移。CocoaPods正式进入维护模式，没迁移的插件最终会无法工作。

另外社区贡献者@lukemmtt优化了构建管线，提前过滤掉不必要的SwiftPM scheme，构建速度有实打实的提升。

**老刘的看法**

之前老刘反复提醒过：老项目别急着上AGP 9和SPM，等生态跟上再说。

现在情况开始变化了。Top 100插件的适配率到了92%，CocoaPods进了维护模式，方向已经定死，剩下的只是时间问题。

我的建议也跟着调整：新项目直接上SwiftPM；老项目现在就可以把插件清单拉出来过一遍，看看哪些还没适配，提前给作者提issue。真等到CocoaPods支持被移除那天再动手，就被动了。

***

## 五、Wasm继续推进，Widget Previews转正

**Wasm默认化**

Flutter正在推动Web应用默认启用WebAssembly

有个坑要提前说：Wasm不支持旧的`dart:html`库，得迁移到新的JS interop包（`package:web`）。好消息是，升级项目依赖通常就能自动解决大部分遗留的interop问题。

主渠道还上了一个实验性能力：Wasm延迟加载。把Wasm应用拆成更小的懒加载模块，优化首屏加载时间。

做Web端的同学，这个值得盯住，首屏速度对web应用来说非常重要。

**Widget Previews转正**

Flutter Widget Preview正式进入稳定版。不用构建和启动整个应用，就能即时渲染、检查。单个UI组件。

稳定版带来三个改进：

- **启动更快**
本地项目缓存（`.widget_preview/`文件夹），消除重复设置的开销
- **测试更灵活**
抽象出`PreviewThemeData` API，支持顺序主题分层，复杂矩阵测试也好搞了
- **Web资源自动同步**
预览Web组件时自动复制宿主项目的`web/`资源，自定义主题和`index.html`都能自动应用

这个功能对组件库作者和UI密集型企业项目是真福利，改一个按钮再也不用等全量构建了。

顺带提一句，GenUI包也更新到了0.10.0，新增`a2ui_core`包集中管理协议相关类，还支持了A2UI客户端函数，让agent可以指示客户端执行验证、派生值这类小任务，省掉往返通信。AI生成UI这条线，官方一直在悄悄加码。

***

## 六、平台细节打磨，快速过一遍

这部分不展开，挑重点列一下，哪条戳中你的痛点，你自己去翻changelog。

**Android**

- 修复了虚拟键盘修饰键（比如Shift）卡住的问题
- 依赖版本矩阵
Java最低17，Kotlin Gradle Plugin 2.4.0，Android Gradle Plugin 9.1.0，Gradle 9.3.1
- 标准API级别默认值
`flutter.compileSdkVersion`和`flutter.targetSdkVersion`都是API 36，`flutter.minSdkVersion`是API 24

**iOS / macOS**

- 代码签名更透明，CLI选证书时会同时显示Team ID和Team Name
- 签名失败时，provisioning profile的错误信息更清晰了

**桌面**

- 修复Windows韩文输入时的光标定位问题
- Windows插件可通过`FlutterEngine::PostPlatformThreadTask`把耗时任务移出平台线程
- Linux新增触控笔旋转和压力报告

**框架打磨**

- Android的高对比度和颜色反转设置现在能自动检测（`MediaQueryData.highContrast`、`MediaQueryData.invertColors`）
- 移动端文本选择手柄在轻微滚动时保持稳定，手柄不再遮挡屏幕顶部的上下文菜单
- 修复`SelectableRegion`在空滚动容器中开始选择时的崩溃
- 改进嵌入平台视图的原生iOS视图手势传播
- `ImageIcon`支持`useOriginalColors: true`保留原始颜色
- `AnimatedCrossFade`支持指定裁剪行为

***

## 总结一下

Flutter 3.47并非一个功能上重大更新的版本，而是主要把之前的规划变成正式的路线。

设计系统解耦、渲染引擎换代、Apple平台规则跟进，这三件事单独拿出来都是大工程，官方选择在一个版本里一起端上来。

**老刘的升级建议**

咱们的策略一直都没有改变，新版本先观察两个月，等核心功能稳定、第三方的生态跟上，再开始升级。

与其把时间花在给新版本填坑，不如去关注你的业务逻辑。

这次Flutter 3.47的更新，你最关注哪一项？Material分家你打算什么时候迁？

欢迎在评论区留言，咱们聊聊。

***

> 🤝 如果看到这里的同学对客户端开发或者Flutter开发感兴趣，欢迎联系老刘，我们互相学习。
>
> 🎁 点击免费领老刘整理的《Flutter开发手册》，覆盖90%应用开发场景。
>
> 🚀 [覆盖90%开发场景的《Flutter开发手册》](https://mp.weixin.qq.com/s/6FeO9IoHbEuM-vhISitUxw)

> 📂 老刘也把自己历史文章整理在GitHub仓库里，方便大家查阅。
> 
> 🔗 <https://github.com/lzt-code/blog>
