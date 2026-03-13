# Flutter 官方Skill发布，对开发者意味着什么？

**大家好，我是老刘**

最近Flutter 官方主动推出了Flutter开发的官方 Skill（还没正式发布）。有不少朋友让老刘谈谈对这件事怎么看。

我是躺床上看的😄

Flutter官方主动推出Skill，说明 Flutter 团队非常敏锐地捕捉到了 AI 编程的趋势，也说明Flutter官方团队对AI编程的重视程度。

这给其他框架（如 RN, KMP）通过了压力，也树立了标杆。

未来，一个框架是否流行，不仅取决于它本身的性能和生态，还取决于它对 AI 是否友好。**“文档写得好”可能不如“Skill写的好”更有吸引力。**

接下来我们先来介绍一下这个Flutter官方的Skill，然后再看看对我们这些Flutter开发者来说，会有哪些影响。

老刘个人觉得这个影响还是蛮大的。

***

## 1. skill 和 agent、mcp 在使用场景上有什么差异？

![](https://fastly.jsdelivr.net/gh/lzt-code/blog@main/存档/2026/assets/skill_vs_mcp.png)

首先Agent可以理解为一个具备特定领域知识和技能的人，他可以规划、记忆和多步执行一个任务，能够独立的完成特定领域的复杂任务。

MCP是通过标准协议，让Agent能调用外部工具，比如调用一个API获取当前天气信息。

而skill是给Agent的一本技术手册，它可以告诉Agent如何完成某个特定的任务，比如计算器这个skill，就能告诉Agent如何进行加减乘除等运算。

更具体一点说，老刘常用的Trae可以理解为一个Agent，他能写各种各样的代码，我日常会用它来写Flutter代码。

而我们可以给他提供一个Riverpod的skill，告诉他如何使用Riverpod来管理状态，以及RIverpod的最佳实践有哪些。

这样Trae写出的Riverpod代码就不会产生幻觉，也更能符合我们项目要求的最佳实践。

本文介绍的Flutter 官方skill，就是为了帮助开发者更方便的使用Flutter框架，提高开发效率。

***

## 2. Flutter 官方skill 都有哪些功能？

Skill是AI的外挂知识库：通过 SKILL.md ，我们把最新的 Flutter 知识（比如 3.41 新特性）喂给 AI，让它从通用程序员变成Flutter专家。

那么这次Flutter官方提供的skill都包含哪些功能呢？

Flutter官方skill的具体说明可以看github上的官方文档：<https://github.com/flutter/skills>

**注意：根据文档说明，该仓库目前仍处于开发阶段，尚未准备好供生产环境使用。**


### 2.1 功能清单

这些 Skill 旨在为 AI Agent提供操作Flutter项目的专业能力。以下是按功能类别的整理：

#### 环境与基础配置

- flutter-environment-setup-windows / macos / linux :
  - 分别用于在 Windows、macOS 和 Linux 上搭建 Flutter 开发环境。
- flutter-architecture :
  - 使用 Flutter 团队推荐的应用架构来构建应用程序。
- flutter-theming :
  - 使用 Flutter 的主题系统自定义应用的外观主题。
- flutter-localization :
  - 配置应用以支持不同的语言和地区（国际化）。

#### UI 与布局

- flutter-layout :
  - 使用 Flutter 的布局组件和约束系统构建应用界面。
- flutter-animation :
  - 为 Flutter 应用添加动画效果。
- flutter-accessibility :
  - 配置应用以支持屏幕阅读器等辅助技术（无障碍功能）。

#### 数据、网络与状态

- flutter-state-management :
  - 管理 Flutter 应用程序的状态。
- flutter-http-and-json :
  - 发起 HTTP 请求以及进行 JSON 数据的编码与解码。
- flutter-databases :
  - 在应用中处理数据库操作。
- flutter-caching :
  - 实现应用数据的缓存机制。

#### 性能与优化

- flutter-performance :
  - 优化 Flutter 应用的性能。
- flutter-app-size :
  - 测量并减小 Flutter 应用包（Bundle, APK, IPA）的体积。
- flutter-concurrency :
  - 在后台线程中执行耗时任务（并发处理）。

#### 原生交互与插件

- flutter-native-interop :
  - 在 Android, iOS 和 Web 上与原生 API 进行交互。
- flutter-platform-views :
  - 在 Flutter 应用中嵌入原生视图（Native View）。
- flutter-plugins :
  - 构建 Flutter 插件，为其他 Flutter 应用提供原生互操作能力。
- flutter-routing-and-navigation :
  - 处理屏幕间的跳转、路由管理及深度链接（Deep Link）。

#### 测试

- flutter-testing :
  - 添加单元测试、组件测试（Widget Test）或集成测试。

### 2.2 如何使用Flutter skill

可以通过以下命令安装这些 skills：

```bash
npx skills add flutter/skills
```

更新 skills：

```bash
npx skills update flutter/skills
```

目前主流的AI开发工具比如Claude Code、Cursor、Trae等都已经提供了对skill的支持。

同时，你也可以利用Flutter skill提供的tool来创建自己的skill，比如创建一个Riverpod使用方法的skill，后续老刘可以写篇文章介绍一下。

接下来我们来看看这对我们这些客户端开发者来说意味着什么？

***

## 3. Flutter 官方skill 发布后，对开发者意味着什么？

### 3.1 降低门槛，新手也能快速“上道”

Flutter 的环境搭建（尤其是在 Windows上配置Android环境）一直是新手的噩梦。

官方提供了 `flutter-environment-setup` 等 skill，意味着 AI 可以手把手甚至自动帮你完成环境配置。

此外，对于复杂的架构（Architecture）和状态管理，新手往往不知道如何起手，有了官方 Skill 加持的 AI，可以直接生成符合官方推荐架构的代码骨架，让新手起步就是最佳实践。

### 3.2 减少 AI “幻觉”，代码质量更有保障

以前我们用 AI 写 Flutter 代码，它可能会给出过时的 API（比如还在用 `FlatButton`），或者混用不同的状态管理逻辑。

老刘这边常用的解决方案是建立一个Flutter开发者智能体，把项目标准的代码规范都写在智能体中。

这样的问题是比较难以保证全面性，时不时需要添加一些新的内容然后同步给所有人。

Flutter 官方 Skill 其实给了我们另一个更优雅的解决方案，相当于给 AI 注入了标准的使用模板。

- **准确性提升**：AI 生成的代码将严格遵循 Flutter 团队的最新规范。
- **一致性增强**：无论是路由管理还是状态管理，AI 都会采用统一的标准写法，而不是东拼西凑。
- **最佳实践落地**：像性能优化（`flutter-performance`）、包体积缩减（`flutter-app-size`）这些高级话题，普通开发者可能不熟悉，但现在的 AI 可以在官方 Skill 的指引下给出专业的优化建议。这部分也是老刘自己的智能体中没有的内容。

### 3.3 开发模式的转变：从查文档到用 Skill

这一点我认为是Skill对软件开发造成的最深远的影响。

我记得之前不少文章里面提到过，在AI时代，**AI友好度**是衡量一个库或者开发框架好坏的新维度。

那要如何提高AI友好度呢？

之前有两个最直观的方面：

1. 框架本身的简洁程度

   老刘经常举的例子就是Flutter的状态管理，对程序员来说，可能Riverpod更为省事好用，但是对于AI来说，可能Bloc就更好。

   因为Bloc所有代码都摆在明面上，不像Riverpod有大量自动生成的代码，而且Riverpod还有多个不同的模式可供选择。

   Bloc的这种简单不管是AI生产代码还是bug定位都会更为精准。

   这样就相当于天然的提升了AI友好度。
   
2. 足够多数量的使用案例

   这个应该很好理解了，因为AI并没有真正的逻辑思维。

   也就是说如果你只给他说明文档，没有任何代码案例，AI是很难生成正确代码的。

   只有基于大量代码案例，AI才能基于模式匹配而生成正确的代码。

那么Skill在提升AI友好度方面有什么帮助呢？

如果说官方文档是提供给开发者的使用说明书，那么一个库或者框架官方提供的Skill，就是给AI的使用说明书。

AI可以不用在训练大模型时有这个库的大量案例，只需要有一份优秀的Skills，就可以完成很好的代码生成。

所以老刘大胆预测，官方的Skills将是未来开发框架和三方库的标配，就好像现在的官方文档一样。

![开发框架标准化的演进：从文档到 Skills](https://fastly.jsdelivr.net/gh/lzt-code/blog@main/存档/2026/assets/standard_evolution.png)

而基于Skills，我们的开发范式将会产生更彻底的变革。

开发者将更多地扮演架构师和验收者的角色，而将繁琐的编码工作更放心的交给AI。

***

## 4. 总结

Flutter 官方 Skill 的发布，标志着 Flutter 开发进入了 **AI Native** 的新阶段。

对于开发者来说，这既是工具的升级，也是角色的挑战。

我们要做的，不仅仅是会写Dart代码，更要学会如何高效地使用这些 Skill，让 AI 成为我们最得力的超级助手。

拥抱变化，从尝试Flutter 官方Skill开始吧！

***

> 🤝 如果看到这里的同学对客户端开发或者Flutter开发感兴趣，欢迎联系老刘，我们互相学习。
>
> 🎁 点击免费领老刘整理的《Flutter开发手册》，覆盖90%应用开发场景。
>
> 🚀 [覆盖90%开发场景的《Flutter开发手册》](https://mp.weixin.qq.com/s?__biz=MzkxMDMzNTM0Mw==\&mid=2247483665\&idx=1\&sn=56aec9504da3ffad5797e703c12c51f6\&chksm=c12c4d11f65bc40767956e534bd4b6fa71cbc2b8f8980294b6db7582672809c966e13cbbed25#rd)

> 📂 老刘也把自己历史文章整理在GitHub仓库里，方便大家查阅。
> 🔗 <https://github.com/lzt-code/blog>

