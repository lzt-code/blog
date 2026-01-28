# Flutter 3.38 版本更新：客户端开发者需要关注这三点？



![](https://files.mdnice.com/user/142171/a7d61a33-bcdf-44ff-b806-d972b92cfed4.jpg)

---

**哈喽，我是老刘**

作为一个以Flutter为主要技术栈的开发者，其实我对Flutter版本更新的关注程度比很多人想象中要底很多。

本质上是因为在我的团队里对Flutter版本更新这件事会采用非常谨慎的策略。

我们的产品功能极少依赖最新版本的某个新组件，同时除非有非常严重的bug要解决，也不会急于升级到新版本。

但是Flutter 3.38版本我觉得各位开发者还是有必要关注一下的。

从Flutter本身的功能来看没有特别重大的更新，但是对于Android和iOS原生系统的要求来说，这个版本还是非常重要的。



## 官方链接
- Release Notes（3.38.0）： https://docs.flutter.dev/release/release-notes/release-notes-3.38.0 （官方版本更新内容与变更说明）［来源：Flutter Docs］
- Breaking Changes & Migration： https://docs.flutter.dev/release/breaking-changes （所有破坏性变更与迁移指南索引）［来源：Flutter Docs］
- UIScene 生命周期迁移（iOS 必读）： https://docs.flutter.dev/release/breaking-changes/uiscenedelegate （苹果要求采用 UIScene 生命周期，需按此迁移）［来源：Flutter Docs］
- What's New（文档站新增内容）： https://docs.flutter.dev/release/whats-new （该页明确本次版本重点并指向相关指南）［来源：Flutter Docs］
- 官方技术博客（3.38 总览）： https://blog.flutter.dev/whats-new-in-flutter-3-38-3f7b258f7228 （本次版本的特性、工具链要求与已知问题）［来源：Flutter Blog］

## 要点解读
### Dart 语言更新：Dot shorthands 默认开启
Dot shorthands 是 Dart 3.6 中引入的“点速记”语法，允许在枚举或静态常量上下文中省略前缀，仅写 `.xxx`，编译器自动补全类型。  
- 适用场景：枚举值、静态常量（如 `MainAxisAlignment.start` → `.start`）。  
- 开启条件：Flutter 3.38 默认启用，无需额外配置。  

'''dart
// With shorthands
Column(
  mainAxisAlignment: .start,
  crossAxisAlignment: .center,
  children: [ /* ... */ ],
),

// Without shorthands
Column(
  mainAxisAlignment: MainAxisAlignment.start,
  crossAxisAlignment: CrossAxisAlignment.center,
  children: [ /* … */ ],
),
'''

最主要的作用是减少样板代码，提升可读性。

### Web 开发增强
- web_dev_config.yaml 配置开发服务器：
    - 可设置 host/port/HTTPS 证书/headers，以及代理规则（将指定路径转发到后端）
- Web 热重载增强：
    - -d web-server 模式下默认开启 Web 热重载，并支持多个浏览器同时连接
    - 可用 --no-web-experimental-hot-reload 暂时禁用（后续版本会移除该禁用选项）

Flutter最近几个小版本更新都在持续优化Web开发的部分，可见近期团队的重点一部分放在这里。

不过Flutter的web和常规的web开发两者应用场景还是有区别的，开发者做技术选型时一定要根据实际场景考虑。

### Framework优化
#### OverlayPortal 新能力
可将子 Widget 渲染到任意 Overlay（如 root overlay），并通过 overlayChildLayoutBuilder 精细控制位置。

感觉适合弹窗、气泡、提示、对话框等复杂浮层的灵活布局。

#### Windows 桌面增强
可访问已连接显示器列表（PlatformDispatcher.displays），查询分辨率、刷新率、设备像素比、物理尺寸等属性。

这次的桌面增强也属于是完善桌面的功能完备性的一个组成部分。

Flutter的桌面端多窗口还没有完整的实现，但是能看到各个细节在不停的补充进来。

对桌面端有需要的开发者目前仍然建议优先选择其它技术栈，但是可以持续关注Flutter的桌面端多窗口功能的进展。

### 其它更新

Flutter 3.38 修复了 issue #173770：在 Android 端退出 Activity 销毁时出现的严重内存泄漏。该缺陷自 3.29.0 引入，影响所有 Flutter 应用。


## 升级提示

Flutter 3.38 从功能上看没有特别重大的更新，但是对Android和iOS原生来说都有比较重要的 影响。

- Android：默认 NDK 版本升级为 r28，满足Google Play 16 KB 页面大小兼容性要求。  
- iOS：提供了对 UIScene 生命周期的支持。
    老刘在文章开始的官方链接部分也有给出UIScene 生命周期的官方迁移指南。

因此，虽然从功能上看没有升级的必要，但是从原生的角度来说，确实是建议升级的。

根据我们一贯的升级核心原则：**2~3个月观察期，别当小白鼠**

新版本发布后的前两三个月是“真人实验期”，严重问题通常在这段时间集中暴露。

等社区反馈、官方 issue 修复进度、第三方插件兼容性稳定后，再将其提升为主力版本。

老刘也会在每个月发布的《Flutter版本选择指南》中更新 Flutter 3.38 版本的最新情况。

历史链接：

- [Flutter版本选择指南：避坑3.27，3.35基本稳定 | 2025年10月](https://mp.weixin.qq.com/s/DsP4g_9HKAkOlfcyTGKmCw)
- [Flutter版本选择指南：避坑3.27 | 2025年9月](https://mp.weixin.qq.com/s/9JHDVD2wSVtXkv8UxUr-qg)



## 总结

Flutter 3.38 从功能本身来说并非“重大升级”，更像是常规迭代与体验优化（Web 开发流程、桌面细节、语法易用性）。

但是不管是Android端的16k页面大小兼容还是iOS端的UIScene生命周期迁移，都对Flutter的开发有比较重要的影响。

因此建议将 3.38 设为候选版本，等待2–3 个月观察窗口。没有重大问题后再提升为日常主力版本。

