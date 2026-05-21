---
title: Flutter 3.44 有哪些变化？（官方blog完整翻译）
date: 2026-05-21
tags:
  - Flutter
  - Google I/O 2026
  - Android
  - iOS
  - AI
  - 翻译
description: 别只盯着版本号看，Flutter 3.44 这次是真的“动了筋骨”。老刘连夜把官方万字博文翻译成了中文，带你看懂未来一年的技术风向。
---

**大家好，我是老刘**

Flutter 3.44 真的发布了不少东西，之前每次大版本发布老刘都只是点评其中我认为比较重要的内容，然后把官方的博文链接分享出来。

What’s new in Flutter 3.44： https://blog.flutter.dev/whats-new-in-flutter-3-44-b0cc1ad3c527

但是有不少朋友反馈官方链接打不开，所以这次老刘先把官方内容翻译成中文分享出来。

后续还会单独写篇文章聊聊我觉得这个大版本有哪些内容值得我们开发者关注的。

由于原文章中有很多 gif 图片太大公众号无法上传，所以老刘只保留了 png 图片（这里吐槽一下公众号的傲慢）。

好了下面就是译文的内容：

***

# Flutter 3.44 有哪些新变化
**在 Google I/O 2026 上赋能开发者**

Flutter 3.44 正式发布，这是一个非常重磅的版本！本版本迎来了 Flutter 发展史上的多个里程碑：Android 端的 Hybrid Composition++、成为 iOS/macOS 新默认配置的 Swift Package Manager，以及针对 Impeller 改进的 Vulkan 支持。我们还与新晋桌面端主导维护者 Canonical 合作，带来了多窗口桌面支持的预览，并开启了一项重大的架构演进——将 Material 和 Cupertino 库从核心框架中解耦。我们正在通过 GenUI 重新定义智能体（agentic）用户体验的交互，并通过 Agentic Hot Reload、Dart & Flutter Agent Skills 重塑开发者的开发体验。从 2026 款丰田 RAV4 的多媒体系统到即将推出的 LG webOS SDK，Flutter 正在为下一代“无处不在”的应用赋能。我们非常高兴能与大家分享所有的新闻与更新，欢迎来到 Flutter 3.44！

*Flutter 3.44：扩展至更多设备上的更多用户！*

今年 Google I/O 的 Flutter 主题是：**Flutter 无处不在，服务日常，人人共建，人人共享。**

“**无处不在，服务日常**”源于我周二使用手机应用时的一个感悟：Flutter 应用已经融入了我生活的方方面面，从在旧金山湾区记录饮食到在日本旅行时购物。数据也印证了这一点：pub.dev 生态系统比以往任何时候都更受欢迎，仅在过去 30 天内，包下载量就超过了 **13 亿次**。Flutter 现已成为两大主流应用商店中**第二受欢迎的移动开发 SDK**，月活跃开发者已超过 **150 万名**，仅一年内就增长了 50%。

“**人人共建，人人共享**”反映了我与 Google I/O 联合主持人 Kate Lovett 之间关于全球社区乐趣的对话。我们 **1,700 多名** 尽职尽责且充满热情的贡献者是推动这一进展的引擎，他们在过去的一年中向核心仓库提交了 **5,800 项变更**。仅在本次发布周期中，我们就合并了来自 **178 位独立贡献者**（包括 **61 位首次提交贡献的新成员**）的 **972 次提交**。我们的社区依然是 Flutter 的生命线，确保它真正做到人人共建，人人共享。非常感谢大家！

关于更多的变更信息，您可能还想查看 Dart 3.12 版本的更新公告：https://dart.dev/blog/announcing-dart-3-12。

***

***
## 开发者体验

我们希望让使用 Flutter 构建应用的体验尽可能高效，无论您是手动编写代码，还是与您喜爱的 AI 编程助手共同迭代。在此版本中，我们改进了现有的开发者工具套件，并引入了全新的工具来增强您的开发工作流。

### DevTools 性能提升
我们引入了细粒度的分析以提高效率，并针对包含大量文件或目录的项目提升了分析性能。

我们还对 Flutter DevTools 进行了多项稳定性和性能改进，包括**默认使用 WASM**，这使得 DevTools 的响应更加敏捷、迅速。

* **了解更多**
DevTools 2.55.0：https://docs.flutter.dev/tools/devtools/release-notes/release-notes-2.55.0 和 2.57.0：https://docs.flutter.dev/tools/devtools/release-notes/release-notes-2.57.0 版本的发布说明。

### 组件预览（实验性）
此版本为 Widget Preview 环境带来了进一步的性能改进和新特性：

* **预览检测重写**
检测逻辑现在利用了 Dart Analysis Server，显著降低了 flutter 命令行工具的内存占用。对于 IDE 用户，整体内存占用最高可降低 50%。
* **预览过滤**
现在可以按组、名称以及脚本和包的 URI 过滤预览，从而更容易在拥有大量预览的项目中进行开发。特别感谢社区成员 NamanGoyalK：https://github.com/NamanGoyalK 的这一贡献：https://github.com/flutter/flutter/pull/184023！

* **了解更多**
Flutter Widget Previewer（组件预览工具）：https://docs.flutter.dev/tools/widget-previewer

### 免 Rosetta 的原生 Apple Silicon 支持
在搭载 Apple Silicon 芯片的 Mac 上进行开发的开发者，不再需要安装 Rosetta 转换层即可运行 Flutter。所有的 macOS 命令行工具（包括我们的 iOS 设备通信二进制文件）均已更新，可原生运行在 ARM 架构上。此次更新领先于 Apple 计划停用 Rosetta 转换支持的步伐，确保您在 Apple 硬件上的开发环境面向未来。展望未来，Flutter 的后续版本将完全停止支持基于 Intel x86 的 Mac 主机。如果您的团队目前仍依赖 Intel 芯片的 Mac 进行开发，建议现在开始规划硬件迁移。

* **了解更多**
在搭载 Apple 芯片的 Mac 上使用 Intel 格式的 App：https://support.apple.com/zh-cn/102527 (support.apple.com)

### 重构 AI 驱动世界下的开发者体验
在过去的一年里，Dart 和 Flutter 生态系统涌现了大量基于智能体（agent-based）的工具，如 Antigravity、Gemini CLI、Claude Code 和 Cursor，这从根本上将开发者的角色演变为架构和协调多个智能体。为了支持这一转变，我们致力于加强我们的开发体验基石，并引入新的工具来强化您的开发工作流。

* **通过 Agentic Hot Reload 实现无缝的 AI 编程助手集成**
  作为 AI 辅助开发的一次重大跨越，我们推出了 **Agentic Hot Reload（智能体热重载）**
MCP（模型上下文协议）服务器和您喜爱的 AI 助手现在将自动查找并连接到正在运行的 Dart 和 Flutter 应用程序。这意味着像 Antigravity 这样的 AI 编程助手现在可以开箱即用地对您的运行应用进行热重载！当您让 AI 助手编辑 UI 时，它会编写代码并自动触发热重载，立即向您展示结果，无需任何手动设置。快来尝试一下吧！此外，我们还：
  * **强化了依赖项搜索**
AI 助手现在可以安全地读取和搜索包依赖项内部的文件，而无需对您的本地 pub 缓存（pub cache）拥有完全的访问权限。
  * **整合了工具链**
我们整合了我们的 MCP 工具定义，从而显着降低了智能体工作流的 Token 消耗成本。

此外，我们最近还推出了 **面向 Dart 和 Flutter 的 Agent Skills（智能体技能）**，这能为您的 AI 编程助手赋予面向任务的、生产级的领域专业知识。这些技能提升了 AI 助手的能力，并在其完成添加集成测试或设置本地化等任务时帮助您节省 Token 消耗，同时确保遵循推荐的最佳实践。

* **了解更多**
介绍 Dart 和 Flutter 智能体技能：/introducing-skills-for-dart-and-flutter-23837c6ec0ae、Dart & Flutter MCP 服务器：https://docs.flutter.dev/ai/mcp-server

### Flutter 助力万屏 AI：构建下一代 AI 原生应用
随着 AI 驱动的功能从简单的内容 summaries 演变为完全自主的智能体助手，我们致力于扩展 Dart 和 Flutter 的生态系统，以便为在各个平台上打造这些体验提供所需的基础设施。

* **Firebase AI Logic**
  Firebase AI Logic 允许您从 Flutter 应用中在客户端调用 Gemini API。
  MacroFactor：https://macrofactor.com/ 是一款使用 Firebase AI Logic：https://pub.dev/packages/firebase_ai 直接连接到 Gemini 模型并利用其多模态能力的 Flutter 应用。我一直在用它记录我的饮食——只需拍张照片即可。这是一个利用 AI 将枯燥繁琐的日常琐事转化为令人愉悦、近乎神奇的用户体验的绝佳范例。
  Firebase AI Logic 现在支持服务器端提示词模板 (Server Prompt Templates)：https://firebase.google.com/docs/ai-logic/server-prompt-templates/get-started?api=dev#high-level-use-template-in-code，无需再将提示词直接嵌入到应用代码中。
面向 Flutter 的 Firebase Agent Skills：https://firebase.google.com/docs/ai-assistance/agent-skills 现已可用，它们能够提供逐步指导，帮助您更高效地构建全栈 Flutter 和 Firebase 应用程序。

![](https://gcore.jsdelivr.net/gh/lzt-code/blog-images@main/img/1ee22d11-eae1-4e5d-9eff-039c1691193c_4146e405.png)

* **了解更多**
MacroFactor 借助 Firebase、Flutter 和 Gemini 为超过 40 万用户通过 AI 革新营养管理：https://cloud.google.com/customers/macrofactor

* **Genkit Dart 预览版**
  我们还非常高兴地宣布推出了 **Genkit Dart 预览版**，这是一个用于构建全栈、AI 驱动及智能体应用的开源框架。它具有支持 Google、Anthropic 和 OpenAI 等提供商的模型无关型 API。它配备了从原型过渡到生产所需的一切，包括类型安全的结构化输出、工具调用（tool calling）、多轮对话以及内置的观测能力（observability）。
  您不仅可以将其运行在服务器端，也可以直接在 Flutter 应用的客户端运行 Genkit Dart！

```dart
import 'package:genkit/genkit.dart';
import 'package:genkit_google_genai/genkit_google_genai.dart';

void main() async {
 final ai = Genkit(plugins: [googleAI()]);

 final response = await ai.generate(
   model: googleAI.gemini('gemini-flash-latest'),
   prompt: 'Why is Dart a great language for AI applications?',
 );

 print(response.text);
}
```

* **了解更多**
Genkit Dart：利用 Dart 和 Flutter 构建全栈 AI 应用：https://dart.dev/blog/announcing-genkit-dart-build-full-stack-ai-apps-with-dart-and-flutter

### Gemma 3n 影响力挑战赛
我们非常自豪能看到 Flutter 开发者不断突破 AI 技术的边界。热烈祝贺 Gemma Vision 的创作者 Tommaso Giovannini 和 Vite Vere 的创作者 Guido Marangoni 在去年的 Gemma 3n 影响力挑战赛：https://www.kaggle.com/competitions/google-gemma-3n-hackathon中分别荣获第一名和第二名。他们都选择了 Flutter 来构建改变生活的重要工具：
* **Gemma Vision** 帮助视力障碍人士感知世界。
* **Vite Vere** 协助认知障碍人士完成日常生活中的任务。

![](https://gcore.jsdelivr.net/gh/lzt-code/blog-images@main/img/d2025dc2-359d-4789-bb02-84954c0b3169_9c0ba7c3.png)

* **了解更多**
Gemma 3n 影响力挑战赛获奖名单：https://www.kaggle.com/competitions/google-gemma-3n-hackathon/hackathon-winners

### Gemma 4
Gemma 4 官方于近期发布，这是一个专为高级推理和智能体工作流、成本控制、设备端数据限制或网络约束场景而设计的轻量级设备端模型。它的多模态能力非常出色，其执行多步骤规划和链式工具调用（chaining tool calls）的能力令人印象深刻。

以往，在多样的硬件设备上管理这些设备端模型是非常复杂的。这就是为什么我对于 LiteRT-LM 感到如此兴奋。

![](https://gcore.jsdelivr.net/gh/lzt-code/blog-images@main/img/88031056-6c7e-4989-89a0-e6e3e602e2a1_da12fe53.png)

* **了解更多**
Gemma 4：https://deepmind.google/models/gemma/gemma-4/

### 面向 Flutter 的 LiteRT-LM
在研读 Gemma Vision 和 Vite Vere：https://ai.google.dev/competition/projects/vite-vere 的代码时，我备受鼓舞地发现它们都利用了 pub.dev 上的 `flutter_gemma` 插件来与 Gemma 模型集成。

而未来这还会变得更好：我们很高兴宣布，面向 Flutter 的完整 **LiteRT-LM 支持** 即将引入 `flutter_gemma` 包。

LiteRT-LM 是 Google 推出的生产级、高性能、开源推理框架。它能抹平硬件差异，使您能够在 Android、iOS、Web、Windows、Linux 和 macOS 这所有 6 个 Flutter 稳定平台上，通过 GPU 和 NPU 加速实现峰值性能，轻松运行像 Gemma 4 这样强大的设备端 AI 模型。

* **了解更多**
`flutter_gemma` 插件包：https://pub.dev/packages/flutter_gemma 以及 LiteRT-LM 概述：https://ai.google.dev/edge/litert-lm/overview。

### Flutter + A2UI = GenUI
当谈到 AI 驱动的用户体验时，我们可能都对铺天盖地的 Markdown（甚至是纯文本）感到有些审美疲劳了。

**生成式 UI (Generative UI，简称 GenUI)** 是一种新型的 UX 范式，其中 AI 可以实时构建和响应真正的 UI 组件，而不仅仅是文本（如 Hatcha 演示应用中所示）。

在过去的一年里，我们的 GenUI 团队一直作为联合项目的合作伙伴来推进这一领域的发展，定义了新兴的 A2UI 协议：https://a2ui.org/。A2UI 是来自 Google 的开源协议，它定义了智能体（agent）和客户端之间如何协作构建用户界面的组合与状态。

自去年年底推出 Flutter GenUI SDK 以来，我们见证了惊人的增长动能，今年年初以来包下载量增长了 500%。

其中一个杰出的例子是 Catagay Ulusoy 编写的 **Finnish it**（Google Play 商店：https://play.google.com/store/apps/details?id=com.sopuacademy.finnishit&hl=en_US，Apple App Store：https://apps.apple.com/us/app/finnish-it-yki-test-practice/id6742380858）。这款应用不仅能通过定制课程计划帮助用户学习芬兰语，还能针对每节课动态生成最合适的 UI。如果您关注了上个月的 Cloud Next 开发者主题演讲，您可能会注意到 Flutter DevRel 负责人 Emma Twersky 专门提到了这款应用并对 Catagay 表示了赞赏！

* **了解更多**
`genui` 插件包：https://pub.dev/packages/genui

#### Visual Layout 实验
来自 Google DeepMind 的 Li-Te Cheng 及其团队是 GenUI 领域的先驱。还记得在 2023 年因为视频中带有红色的 Debug 横幅而引发 Flutter 社区广泛讨论的那个演示：https://youtu.be/v5tRc_5-8G4?si=WZd3l0ZwLUKt1elU&t=97吗？没错，那就是 Li-Te 的团队！

他加入了我们的 "What’s New in Flutter" 演讲，分享了使用 Flutter 构建 Gemini 应用中的“Visual Layout（视觉布局）”实验的经验。以下是 Web 版本：

他谈到了他的团队之所以更倾向于选择 Flutter 作为其首选 UI 工具包的原因……提示：这与我们所有人都热爱 Flutter 的原因是一样的：
* 精美的 UI
* 高效的开发体验
* 多平台支持
* 极为契合 GenUI 的架构设计（这是 Li-Te 的原话！😉）

以下是他总结的、您可以用于您自己的 GenUI 项目的 3 个关键经验：
1. 依靠结构严谨的框架来确保 AI 输出的一致性
2. 使用“AI 批判（AI critic）”闭环来确保可靠的输出
3. 借助模板来平衡生成速度与控制力。

最后，Li-Te 鼓励我们超越纯文本和聊天机器人的局限，转而构建富有表现力、高互动性且令人愉悦的用户体验。

* **了解更多**
面向 Flutter 的 GenUI SDK：https://pub.dev/packages/genui。如果您想了解引导式教程，可以尝试此 Codelab：https://codelabs.developers.google.com/codelabs/genui-intro?hl=en#0。

---

***

## Android 支持

### Googlebook 与外设支持
Flutter 现已做好支持搭载 Gemini 智能的全新 Googlebook 笔记本电脑的准备。由于 Flutter 的设计符合 Android 的大屏应用指南，因此应用能自然地处理外部硬件输入。触控板滚动、鼠标悬停状态、右键快捷菜单以及键盘快捷键等功能均可开箱即用。同时，由于 Flutter 在 macOS、Windows 和 Linux 上拥有成熟的桌面端支持，Flutter 应用在 Googlebook 上将呈现原生且流畅的体验，而非仅仅是拉伸后的移动端界面。您现有的移动端应用无需经历繁重重写，即可在 Googlebook 上获得原生般的舒适体验。

* **了解更多**
隆重推出 Googlebook：为 Gemini 智能而设计：https://blog.google/products-and-platforms/platforms/android/meet-googlebook/

### Android 17
Android 17 即将来临，我们的团队正在积极针对最新的 Android 17 Beta 版本测试 Flutter，以确保您的应用如常运行。我们还主动集成了最新的安全和易用性功能，例如本地网络保护（Local Network Protections）以及安全的动态代码加载（Dynamic Code Loading）。

您可以在 GitHub 上监控我们的持续进度。我们鼓励您下载 Android 17 Beta 版：https://developer.android.com/about/versions/17/get并从今天开始测试您的应用。如果您遇到任何 Bug 或发现缺失的功能，请提交 Issue！：https://github.com/flutter/flutter/issues/new/choose

* **了解更多**
Android 17 GitHub 项目看板：https://github.com/orgs/flutter/projects/248/

### 针对 Android 的 Hybrid Composition++
在 Flutter 应用中嵌入原生 Android 组件（如 Web 视图或地图）历来强迫开发者在帧率（性能）和保真度之间做出妥协。旧的渲染策略常在滚动过程中出现画面撕裂、文本输入异常或 CPU 开销过高等问题。

Flutter 3.44 引入了 **Hybrid Composition++ (HCPP)** 这一可选（opt-in）功能来解决这些挑战。HCPP 不再依赖离屏缓冲区或强迫 Flutter 引擎去处理原生视图，而是直接将图层合成（layer compositing）委派给 Android 系统。该过程利用了 Vulkan 图形库的低底访问，采用硬件缓冲区交换链（hardware buffer swapchains）以及 `SurfaceControl` 事务来使 Flutter UI 与原生 Android 视图保持完美同步。

其带来的效果是高性能的滚动以及精确的触摸输入。它还带来了对 `SurfaceView` 组件的稳定支持，这在旧模式中往往极具挑战。

HCPP 有其特定的 Android API 和硬件要求：https://docs.flutter.dev/platform-integration/android/platform-views#hcpp，因此即便开启，也并非所有设备都能使用 HCPP。在使用上，您无需采用任何新 API，仅需开启配置即可升级您现有的平台视图（Platform Views）。您可以在未来 HCPP 成为默认渲染模式前，通过给 `run` 命令传入 `--enable-hcpp` 标志，或在 `AndroidManifest.xml` 文件中添加以下配置，来提前测试新模式：

```xml
<meta-data
  android:name="io.flutter.embedding.android.EnableHcpp"
    android:value="true" />
```

* **了解更多**
在 Flutter 应用中通过 Platform Views 托管原生 Android 视图：https://docs.flutter.dev/platform-integration/android/platform-views

### Android 屏幕圆角半径支持
为了帮助您在现代移动设备上构建像素级的完美布局，Flutter 现在可以直接与 Android 硬件集成，以支持查询物理和逻辑屏幕圆角半径（#179219：https://github.com/flutter/flutter/pull/179219）。Flutter 现在可以通过 `MediaQuery` 获取屏幕的圆角半径。这使得您的 UI 能够精准贴合硬件几何形状，确保内容永远不会在一些圆角极大的屏幕上被裁剪。

* **了解更多**
`MediaQueryData.displayCornerRadii`：https://main-api.flutter.dev/flutter/widgets/MediaQueryData/displayCornerRadii.html

### Android Gradle Plugin 9.0 与内置 Kotlin
在 Android Gradle 插件 (AGP) 9 之前，Android 应用和插件开发者必须手动将 Kotlin Gradle 插件 (KGP) 添加 to build 文件中，以便系统理解并编译 Kotlin 代码。从 AGP 9.0 开始， Android 构建系统开始原生支持 Kotlin。由于构建系统已经了解如何处理 Kotlin，再次手动添加独立的 KGP 会产生冲突并导致构建失败。此破坏性变更将影响所有使用了 KGP 的应用及 Flutter 插件。

Flutter 团队增加了暂时的向后兼容性，以确保现有项目能够安全构建。对手动引入 KGP 的兼容支持将在未来的版本中移除。

#### 应用开发者指南
如果您开发 Flutter 应用，您需要更新您的 Android 构建文件以移除独立的 Kotlin Gradle 插件 (KGP)。

注意：如果您迁移后的应用使用了一个仍包含 KGP 的旧 Flutter 插件，您的构建仍可能失败。由于这只有插件作者可以解决，请向相关插件作者反馈此问题：https://docs.flutter.dev/release/breaking-changes/migrate-to-built-in-kotlin/for-app-developers#report-incompatible-kotlin-gradle-plugin-usage-to-plugin-authors。

* **了解更多**
完整步骤请参阅应用开发者迁移指南：https://docs.flutter.dev/release/breaking-changes/migrate-to-built-in-kotlin/for-app-developers。

#### 插件作者指南
插件的迁移需要进行类似的 Gradle 文件更改，以及一项重要的版本约束更新。为确保兼容性，您必须更新 `pubspec.yaml` 文件，*将 Flutter 的最低版本约束设置为 3.44*。

* **了解更多**
完整的检查清单，请参考插件作者迁移指南：https://docs.flutter.dev/release/breaking-changes/migrate-to-built-in-kotlin/for-plugin-authors。

#### ABI 过滤变更
ABI 决定了您编译的应用支持哪些设备硬件架构（如 ARM 或 x86）。过去 Flutter 会以编程方式针对每个特定的构建类型（Build Type）应用 ABI 过滤器，而现在我们将其统一配置在基础的 `defaultConfig` 块中。由于 AGP 9 会合并默认配置与具体的构建类型和渠道（Flavor），而不是进行覆盖，因此使用自定义 ABI 配置需要额外的一个步骤。

如果您的应用在特定的构建类型或产品渠道中使用了自定义的 `abiFilters`，您现在需要在构建或运行应用时传递 `-Pdisable-abi-filtering=true` 标志。

* **了解更多**
更多细节请参考 Flavors 开发指南：https://docs.flutter.dev/deployment/flavors#add-unique-build-settings。

---

***

## iOS 支持

![](https://gcore.jsdelivr.net/gh/lzt-code/blog-images@main/img/ac0e4a6b-8848-4c57-8937-3f012440112d_871d0bae.png)

### Swift Package Manager 现已成为 iOS 和 macOS 的默认配置
自 Flutter 3.44 起，**Swift Package Manager (SwiftPM)** 将正式取代 CocoaPods，成为 iOS 和 macOS 应用的默认依赖管理器。Flutter CLI 会自动处理这一迁移过程。当您构建或运行应用时，CLI 会自动将您的 Xcode 项目更新为使用 SwiftPM，无需您再去管理 Ruby 或 CocoaPods 环境！

* **了解更多**
告别 CocoaPods：Swift Package Manager 即将成为 Flutter 的默认配置！：/saying-goodbye-to-cocoapods-swift-package-manager-is-soon-the-default-in-flutter-645a92714a57

Add-to-App（混编集成）也变得更加灵活。如果您将 Flutter 嵌入到现有的原生 iOS 应用中，全新的 `flutter build swift-package` 命令能够将您的 Flutter 应用或模块打包为一个 Swift 软件包（Swift Package），以便在您的原生项目中轻松引用。

* **了解更多**
阅读最新的 Add-to-App 说明文档：https://docs.flutter.dev/add-to-app/ios/project-setup以了解如何与 SwiftPM 进行集成。

如果您的应用依赖的部分插件仍要求使用 CocoaPods，Flutter CLI 会打印警告信息，并暂时针对这些依赖回退到 CocoaPods。我们建议联系包作者进行升级，因为对 CocoaPods 的支持最终将完全移除。为鼓励生态采用，支持 SwiftPM 的包在 pub.dev 评分中将获得额外的加分。

如果您维护着一个 iOS 或 macOS 插件，您需要为您的插件添加 SwiftPM 支持。如果您是在 2024 年试用期间完成的迁移，请确保在 `Package.swift` 文件中将 `FlutterFramework` 添加为依赖项。

如果 SwiftPM 对您的项目造成了无法解决的破坏，您可以通过在 `pubspec.yaml` 中设置 `--enable-swift-package-manager: false` 来暂时停用它。若使用此方案，请在 GitHub 上提交 Bug 报告：https://github.com/flutter/flutter/issues/new/choose并附上您的 Xcode project 文件，以便我们进行调查。请注意，此临时关闭选项最终也会被移除。

* **了解更多**
面向插件作者的 Swift Package Manager 指南：https://docs.flutter.dev/packages-and-plugins/swift-package-manager/for-plugin-authors

### Flutter 支持 UIScene
从 iOS 13 开始，Apple 引入了基于“Scene（场景）”的生命周期来支持多窗口体验。在 WWDC 2025 上，Apple 宣布，使用最新 SDK 构建的应用很快将被强制要求使用 `UIScene` 生命周期来启动。此次更新对于满足 Apple 未来 iOS 版本的审核要求至关重要。

虽然 Flutter 3.44 中没有新 API 变更，但我们要提醒您在 Apple 开始强制推行此新 API 之前完成迁移。如果您的 `AppDelegate` 没有经过深度自定义，Flutter CLI 将自动完成迁移。但如果您的代码对 UI 生命周期事件进行了特定处理，您应当参考完整的迁移指南。

* **了解更多**
`UISceneDelegate` 迁移指南：https://docs.flutter.dev/release/breaking-changes/uiscenedelegate

### iOS 联想输入（实验性）
我们引入了对 iOS 原生输入框内行内联想输入（inline predictive text）的实验性支持（#183650：https://github.com/flutter/flutter/pull/183650）。该功能默认关闭，但您可以通过启用 `TextField.enableInlinePrediction` 进行开启和测试。启用后，用户在应用中输入时，可以通过按 **空格（Space）** 键来接受 iOS 的预测文本（例如，输入“My n”并接受预测的“ame”）。请注意，此联想输入的视觉样式仍在积极优化调整中，我们非常期待您在功能定型前给予我们的反馈。

* **了解更多**
`TextField.enableInlinePrediction`：https://main-api.flutter.dev/flutter/material/TextField/enableInlinePrediction.html

---

***

## Web 支持

### 无障碍功能
无障碍体验与用户偏好的一致性获得了大幅增强。我们现在开箱即用支持浏览器的 `prefers-reduced-motion` 设置，用以自动禁用动画；同时，现在通过使用 `aria-description` 可以为表单验证错误提供即时的屏幕阅读器反馈。

* **了解更多**
MDN 上的 prefers-reduced-motion 说明：https://developer.mozilla.org/zh-CN/docs/Web/CSS/@media/prefers-reduced-motion (mozilla.org)

### 平台与工具链
开发工作流和浏览器集成的流畅度大幅跃升。现在，通过在焦点移动时重用 DOM 表单，引擎已经能完美处理 iOS 26 Safari 中的 `autofill`（自动填充）功能，并优化了 Web 端的滚动与键盘事件合成。此外，CLI 工具链通过直接为 `flutter run` 带来 `--base-href` 参数支持，简化了 Web 应用的管理和调度，使其行为与生产环境下的构建配置相匹配。

* **了解更多**
PR #182024：https://github.com/flutter/flutter/pull/182024、PR #179703：https://github.com/flutter/flutter/pull/179703、PR #180692：https://github.com/flutter/flutter/pull/180692

---

***

## 桌面端支持

![](https://gcore.jsdelivr.net/gh/lzt-code/blog-images@main/img/6a78e83b-a1a8-40d5-a169-d93c071b9565_24406e25.png)

**我们非常高兴地宣布与 Canonical 扩大合作关系，他们现在将正式担任 Flutter 桌面端的“主导维护者（Lead Maintainer）”和“战略顾问（Strategic Steward）”。** 凭借其深厚的系统级技术实力，Canonical 将主导 Flutter 桌面端路线图，并负责 Linux、Windows 和 macOS 嵌入器（embedders）的日常维护工作。

此项合作只是我们整体生态扩展规划的第一步。未来，我们将继续积极扩大治理委员会，引入更多合作伙伴，把 Flutter 的高性能和跨平台体验带往更广泛的终端设备与行业领域。

关于这项合作的进一步发展，敬请期待！

若想向 Flutter 团队咨询合作事宜，请联系 partners@flutter.dev。

### 窗口化 API（实验性）
*⚠️ 注意：多窗口相关功能目前仅在 **main 通道** 可用。现阶段它们还不适合在生产环境中使用。*

Canonical 在桌面端实验性多窗口 API 方面取得了极其瞩目的进展！新特性包括：
* **工具提示 (Tooltips)**
Flutter 现在在 Linux、macOS 和 Windows 上原生支持浮动提示窗口（#182348：https://github.com/flutter/flutter/pull/182348, #180895：https://github.com/flutter/flutter/pull/180895, #179147：https://github.com/flutter/flutter/pull/179147）。
* **弹窗 (Popups)**
macOS 目前已支持独立弹窗（#182371：https://github.com/flutter/flutter/pull/182371），Linux 和 Windows 将在未来的版本中提供支持。
* **对话框 (Dialogs)**
Material 库的 `showDialog` 函数现在可以在支持多窗口的系统上自动创建独立的子对话框窗口（#181861：https://github.com/flutter/flutter/pull/181861）。

最后，Linux 现已支持按内容尺寸自适应大小的视图（#182924：https://github.com/flutter/flutter/pull/182924）。这使您能够根据窗口中的内容动态调整其大小，非常适用于弹窗或浮动提示框。

* **了解更多**
想提前一睹桌面端实验性多窗口 API 的风采，可以参阅 `multiple_windows` 官方示例：https://github.com/flutter/flutter/tree/master/examples/multiple_windows。

### Windows 触控笔支持
对于数字艺术工作者和笔记爱好者来说，使用 Flutter 构建的 Windows 应用迎来了巨大的升级！感谢社区成员 CodeDoctorDE：https://github.com/CodeDoctorDE 带来的卓越贡献，Flutter Windows 现已全面支持触控笔输入，包括对触控笔旋转角度和压力敏感度（压感）的精确追踪。

* **了解更多**
PR 165323: 允许在 Windows 上使用触控笔：https://github.com/flutter/flutter/pull/165323

---

***

## 嵌入式支持

### 丰田 (Toyota)
**丰田 RAV4 曾荣膺 2025 年全球最畅销车型。现在，2026 款 RAV4 采用了 Flutter 来驱动其多媒体系统。**

上个月，我经历了我职业生涯中最引以为傲的一个高光时刻：有机会前往德克萨斯州普莱诺，访问丰田汽车北美总部及 Toyota Connected 公司，并与工程团队深入交流。他们分享了在设计、构建和交付车载娱乐多媒体系统时，Flutter 如何帮助他们彻底改变游戏规则——从办公室内的开发测试机，一直到千家万户车道上的实车。作为一名 Flutter 工程师，同时也是一个从小在全丰田车系家庭长大的车迷，看到 2026 款 RAV4 上运行着 Flutter，我由衷地感到狂喜。我在出行路上已经见到了它们无数次。（这大概就是我们所说的——无处不在吧？）

非常感谢丰田汽车北美和 Toyota Connected 团队的热情款待！

![](https://gcore.jsdelivr.net/gh/lzt-code/blog-images@main/img/86362907-a85a-4f1e-bee4-2fd83654377f_9cfd371d.png)

* **了解更多**
丰田官方新闻稿 《全新演进：丰田多媒体系统即将来到您身边的屏幕上》：https://pressroom.toyota.com/the-latest-evolution-of-toyotas-multimedia-coming-to-a-screen-near-you/

### LG

![](https://gcore.jsdelivr.net/gh/lzt-code/blog-images@main/img/13542049-c952-4ead-852f-05dc6903591a_a804d5f3.png)
LG 即将推出 webOS SDK，以帮助开发者轻松构建面向 webOS 设备的 Flutter 应用。这一举措推动了 Flutter 进军大屏幕及更广泛领域的步伐。

该 webOS SDK 将会包含对 Firebase、视频播放器、游戏手柄等外设的插件支持，并且同样能完美享受您所熟知且喜爱的 Flutter 功能，如状态热重载（stateful hot reload）以及使用 Riverpod 进行状态管理。

请在接下来的几周内密切关注这一令人兴奋的发布！

---

***

## 图形与引擎优化

此版本为 Impeller 渲染后端带来了许多针对性的性能与渲染优化。

### Impeller 改进
* **Vulkan**
  此版本引入了多项针对 Vulkan 的改进，包括更佳的高效缓存内存管理，以及在遭遇掉帧时更加科学的 GPU/CPU 步调同步。
* **使用 SDF 渲染更平滑的圆形**
  渲染圆形的底层数学算法已更新为基于有向距离函数（signed-distance functions，简称 SDF）。解决了以往特定情况下可能出现的边缘锯齿问题（#183536：https://github.com/flutter/flutter/pull/183536, #183184：https://github.com/flutter/flutter/pull/183184）。

![](https://gcore.jsdelivr.net/gh/lzt-code/blog-images@main/img/272faaf3-6630-4606-94d9-d9dc31dbb8b4_69511eba.png)
* **阴影与透视投影修复**
  优化了 Impeller 对透视矩阵的处理逻辑，纠正了阴影渲染以及透视变换矩阵的异常行为（#181434：https://github.com/flutter/flutter/pull/181434, #183187：https://github.com/flutter/flutter/pull/183187）。

### FragmentShader 改进
得益于以下增强功能，编写片段着色器（fragment shader）现在变得更加直观且不易出错：

* **Get Uniform by Name API**
  您现在可以直接在着色器中按变量名称绑定 uniform，而无需再手动计算内存偏移，这极大简化了着色器代码的初始化配置：

```csharp
void setUp(ui.FragmentShader shader) {
  shader.getUniformFloat('foobar').set(1.234);
}
```

* **了解更多**
编写和使用 FragmentShaders：https://docs.flutter.dev/ui/design/graphics/fragment-shaders、`FragmentShader.getUniformFloat`：https://main-api.flutter.dev/flutter/dart-ui/FragmentShader/getUniformFloat.html

* **更清晰的着色器编译器诊断**
  着色器编译器现在在编译与 Skia 不兼容的着色器时，会自动生成警告信息，帮助您在部署到生产环境之前识别那些可能导致跨平台渲染错误的问题（#182786：https://github.com/flutter/flutter/pull/182786, #183146：https://github.com/flutter/flutter/pull/183146）。

---

***

## 框架层优化

此版本不仅开启了深层次的架构转型，同时也贯彻了对产品品质和社区推动的细节优化的严格追求。随着我们将 Material 和 Cupertino 库解耦并迁移至独立包（`material_ui` 和 `cupertino_ui`）的工作正式启动，核心框架自身也在持续走向成熟，并带来了 Web 渲染优化、底层稳定性提高以及更强大的平台级整合。

### Material 与 Cupertino 更新及解耦
此版本代表了 Material 和 Cupertino 库发展史上的一个巨大里程碑。这些库的代码在此版本中已正式冻结（Frozen），这代表着它们作为核心框架内置组成部分的最后一次更新。在此之后，它们将彻底迁移至独立的第三方 Package：`material_ui` 和 `cupertino_ui`。在下个稳定版发布时，核心框架中现有的内置库将被标记为废弃（Deprecated），届时您将能够平滑迁移至全新、独立进行版本演进的第三方包。

* **了解更多**
如需了解该项架构转变的更多信息，请查阅有关冻结公告的博客文章：/flutters-material-and-cupertino-code-freeze-d32d94c59c38并关注有关将这些库从核心框架解耦的主要跟踪 Issue：https://github.com/flutter/flutter/issues/172932。

尽管处于冻结状态，此版本仍然融入了诸多细致的打磨：

* **Cupertino 现代化菜单**
迎来了一次重大的革新。基于灵活底座 `RawMenuAnchor` 重构出的全新 `CupertinoMenuAnchor` 组件，能为 iOS 应用程序带来更加坚实且符合 iOS 系统原生触感的菜单交互体验（#182036：https://github.com/flutter/flutter/pull/182036）。这主要归功于社区贡献者 davidhicks980：https://github.com/davidhicks980 的杰出贡献，他也是 RawMenuAnchor 的创作者。
  * **了解更多**
`CupertinoMenuAnchor`：https://main-api.flutter.dev/flutter/cupertino/CupertinoMenuAnchor-class.html
* **Material 3 动画菜单**
在 Material 侧，`MenuAnchor` 迎来了 Material 3 风格动画的打磨，展现了更润滑的响应。此外，`SubmenuButton` 引入了全新的 `hoverOpenDelay` 延迟悬停参数，为您微调子菜单的悬停触发行为提供了便利（#176494：https://github.com/flutter/flutter/pull/176494）。注意：该动画默认关闭，需要通过将 animated 参数设为 true 来开启。
  * **了解更多**
`MenuAnchor`：https://main-api.flutter.dev/flutter/material/MenuAnchor-class.html、`SubmenuButton.hoverOpenDelay`：https://main-api.flutter.dev/flutter/material/SubmenuButton/hoverOpenDelay.html
* **CupertinoSheetRoute 拖拽联动**
在此版本中，`CupertinoSheetRoute` 内部包含的可滚动内容现已能够与抽屉拉伸拖拽手势完美联动，提供了丝滑的滚动和向下滑动关闭的过渡体验（#177337：https://github.com/flutter/flutter/pull/177337）。对于需要自定义拖拽区域的开发者，全新提供的 `scrollableBuilder` 参数允许您将由组件管理的 `ScrollController` 传递至底部的滚动区域，协助您轻松统筹手势控制逻辑。
  * **了解更多**
`CupertinoSheetRoute`：https://api.flutter.dev/flutter/cupertino/CupertinoSheetRoute-class.html、`CupertinoSheetRoute.scrollableBuilder`：https://main-api.flutter.dev/flutter/cupertino/CupertinoSheetRoute/scrollableBuilder.html
* **CarouselView 循环滚动**
`CarouselView` 组件在此版本中迎来了功能性飞跃。它现在全面支持无限循环滚动（#175710：https://github.com/flutter/flutter/pull/175710），令您可以自由实现平滑无缝且首尾相连的轮播图效果。同时它还提供了新的 `onIndexChanged` 回调接口以及控制器上的 `leadingItem` 状态，以便在用户交互轮播图时更精确地跟踪当前项的变化（#180667：https://github.com/flutter/flutter/pull/180667）。
  * **了解更多**
`CarouselView`：https://main-api.flutter.dev/flutter/material/CarouselView-class.html
* **高级样式与聚焦设计**
新的设计原语令实现高级视觉样式更为简易。例如新的 `ShapedInputBorder` 可以支持您将自定义的任意 `ShapeBorder` 应用于输入框边框上（#177220：https://github.com/flutter/flutter/pull/177220）。这常用于通过 `RoundedSuperellipseBorder` 让 Material 的输入框样式模拟出极具 iOS 风格的超椭圆质感。同样地，`CupertinoFocusHalo` 现在也完美兼容了超椭圆几何，确保不同几何布局下的聚焦光晕（Focus Halo）指示符样式高度统一（#180724：https://github.com/flutter/flutter/pull/180724）。
  * **了解更多**
`ShapedInputBorder`：https://main-api.flutter.dev/flutter/material/ShapedInputBorder-class.html
* **状态控制和列表容器精修**
在 Material 下，支撑 `ExpansionTile` 底层的 `Expansible` 组件在此版本中获得了增强：其 `ExpansibleController` 和 `ExpansionTileController` 均增设了便捷的 `toggle()` 开关控制方法，并辅以了文档示例的补充（#181320：https://github.com/flutter/flutter/pull/181320, #180273：https://github.com/flutter/flutter/pull/180273）。另外，Material 设计中的多类列表子项，包括 `RadioListTile`、`CheckboxListTile` 以及 `SwitchListTile`，现已能规范接收并应用 `WidgetStatesController`，极大便利了通过状态对它们的视图展现进行集中、编程化的管理（#180367：https://github.com/flutter/flutter/pull/180367）。

### 无障碍功能：为所有用户提供更包容的体验
确保应用能面向所有人毫无阻碍地使用，依然是 Flutter 框架的重中之重。在此版本中，我们加深了与底层系统辅助特性的整合，提高了语义层宣告（Semantic announcement）的精准度，并升级了基础控件的可用度：

* 针对 iOS 开发者，本版本接入了多项全新的**无障碍动画机制**（#178102：https://github.com/flutter/flutter/pull/178102）。现在您的 Flutter 应用能够智能匹配用户的系统级首选项：
  * **自动播放动画图像（Auto-play animated images）**
检测用户是否更偏好暂停自动播放的 GIF 等动图内容。
  * **自动播放视频预览（Auto-play video previews）**
知晓用户是否已经在系统层面禁用了视频预览的自动放映。
  * **偏好非闪烁光标（Prefer non-blinking cursor）**
方便应用对容易被光标闪烁干扰注意力或感到追踪困难的用户提供静止的非闪烁输入指示。
  * 这些配置选项统一封装并暴露于 `AccessibilityFeatures` 对象之中，便于您在 iOS 上打造更人性化的 UI 界面。
* **进度指示器的无障碍优化**
您现在可以为 `ProgressIndicator` 传入自定义的百分比文本（如“50%”）来充当其 `SemanticsValue`（#183670：https://github.com/flutter/flutter/pull/183670）。这使得屏幕阅读器能够以更自然、更人性的语言朗读任务进度，而不是小数。
* **核心语义行为重构**
对 `Slider` 滑动条组件的语义区域（semantics node）执行了重组，使之更精准地匹配其实际物理尺寸和定位，从而为依靠盲文探索或特制外设进行操作的用户改进了定位体验（#184168：https://github.com/flutter/flutter/pull/184168）。此外，修复了滚动容器的一项缺陷，保证处于屏幕外不可见的语义标签将不再会先于可见内容被意外朗读出来，保证了清晰明朗的纵览导航流（#184155：https://github.com/flutter/flutter/pull/184155）。

### 0x0 尺寸组件的容错性
我们在该发布周期中倾注了大量心力，以确保框架在面临 0 宽度、0 高度（即 0x0 空间环境）时，不会意外触发布局异常或运行时崩溃。感谢社区成员 ahmedsameha1：https://github.com/ahmedsameha1 稳健且连贯的贡献，我们已经为核心框架下的诸多组件追加了零尺寸检测与容错支持，其中包括：`Hero`（#180954：https://github.com/flutter/flutter/pull/180954）、`Icon`（#181021：https://github.com/flutter/flutter/pull/181021）、`AnimatedPadding`（#181235：https://github.com/flutter/flutter/pull/181235）以及 `GridPaper`（#180906：https://github.com/flutter/flutter/pull/180906）。上述提升有助于保证您的应用即便在面临复杂的视图动画过渡或极限挤压容器时，系统仍可泰然自若、稳定长效。

### SelectableRegion 选区优化
我们针对 `SelectableRegion` 修复了两项影响体验的关键缺陷，用以保证原生与 Web 浏览器下的排版高保真度以及文本选择体验：

* **Web 端约束丢弃修复**
以往，`SelectableRegion` 在 Web 端渲染时，在特殊情形下可能会导致其嵌套组件意外缩小或塌陷。更新后其能够忠实、不经篡改地向下传递排版物理约束（Layout constraints），确保样式表现的前后如一（#184083：https://github.com/flutter/flutter/pull/184083）。
* **多行文本拷贝精准度**
在选区内执行跨行选定并执行文本拷贝动作时，排版中的回车换行信息现在能够完美地留存在剪贴板中，而不会出现丢失乱行的问题（#184421：https://github.com/flutter/flutter/pull/184421）。

---

***

## 破坏性变更与弃用

本版本伴随了一些必要的旧技术演化与标记弃用，这是推动 Flutter 走向轻量和现代化必经的一步。

### RawMenuAnchor 回调行为调整
为在定制化需求下提供更加自主和可预测的行为表现，我们微调了 `RawMenuAnchor` 几个底层回调行为的触发逻辑。

* **了解更多**
关于 RawMenuAnchor 关闭回调顺序调整的说明：https://docs.flutter.dev/release/breaking-changes/raw-menu-anchor-close-order。

核心功能及参数标记弃用一览：
* **`CupertinoSheetRoute` 滚动事件统筹**
在 `showCupertinoSheet` 以及 `CupertinoSheetRoute` 中包含的 `builder` 和 `pageBuilder` 均已标记为弃用，请迁移使用全新的 `scrollableBuilder`（#177337：https://github.com/flutter/flutter/pull/177337）。这能帮助您无缝联动列表滚动与抽屉手势拖曳关闭行为。
* **`ReorderableListView` 拖拽行为重构**
传统的 `onReorder` 触发器标记弃用，由更为灵敏和准确的 `onReorderItem` 所替代（#178242：https://github.com/flutter/flutter/pull/178242）。这个全新的回调能够基于“移除并在新坐标重新装载”的执行序列，为您反馈最符合真实世界期望的 `newIndex` 信息。
* **工具链更新**
考虑到目前 Web 端热重载已通过更为高效、通用的内核来承担，传统命令行工具中的 `--web-hot-reload` 参数现已被废弃（#181884：https://github.com/flutter/flutter/pull/181884）。此外，旧的 `plugin_ffi` 代码模版同样被弃用，后续请直接采用最新、集成了完整 FFI 自动化支持的原生通用插件模板（#181588：https://github.com/flutter/flutter/pull/181588）。

* **了解更多**
关于此版本中各项破坏性变更和详细的迁徙指导，请移步官方网站阅览 Flutter Breaking Changes：https://docs.flutter.dev/release/breaking-changes 说明页。

---

***

## Flutter 无处不在，服务日常

Flutter 的触角已深入到移动、桌面、Web 及嵌入式计算领域的深水区。尽管每项单一的新特性的单列出来便足够振奋人心，但在它们的合力之下，这个坚实的平台正源源不断地为全球多达 150 万开发者赋予构建无边界跨终端应用的能力。无论您身处哪种行业或构建何类工具，从备受推崇的生产力软件如 **NotebookLM**、**Talabat**、**Zoho**、**Karaca**，一直到大放异彩的车载系统（如 2026 款丰田 RAV4 以及 LG webOS 生态），Flutter 始终以默默耕耘的姿态，编织着每一刻的数字日常。

***

## Flutter 人人共建，人人共享

Flutter 今天的繁荣成长，完全离不开每一个来自前线社区的代码奉献、Bug 反馈与真挚建议！我们无比珍惜这股力量，无论是通过在 GitHub 上提交缺陷、在各大技术板块下的真知爪见，还是即将开展的本季度开发者问卷调查，都请留下您的宝贵声音。这正是支撑我们不断把您梦寐以求的特性带进真实世界的动力之源。

在这个生态里，不仅包含着像 Canonical、LG、丰田这样的行业领袖，更重要的是有 150 多万名满怀理想、活跃于一线的开发者与我们携手同行。能和您在这个美妙的 Dart & Flutter 生态大家庭中并肩奋战，我们由衷感到自豪与喜悦。

若想在第一时间内获得所有的新功能、性能提升以及最新的 Impeller 引擎优化，您只需要在终端内执行：

```bash
flutter upgrade
```

***

> 🤝 如果看到这里的同学对客户端开发或者Flutter开发感兴趣，欢迎联系老刘，我们互相学习。
>
> 🎁 点击免费领老刘整理的《Flutter开发手册》，覆盖90%应用开发场景。
>
> 🚀 [覆盖90%开发场景的《Flutter开发手册》](https://mp.weixin.qq.com/s/6FeO9IoHbEuM-vhISitUxw)
    

> 📂 老刘也把自己历史文章整理在GitHub仓库里，方便大家查阅。
> 
> 🔗 <https://github.com/lzt-code/blog>
