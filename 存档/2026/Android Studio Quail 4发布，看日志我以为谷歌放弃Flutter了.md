---
title: Android Studio Quail 4发布，看日志我以为谷歌放弃Flutter了
date: 2026-09-14
tags: [Flutter, Android Studio, AI编程, 开发者工具]
description: Android Studio Quail 4四个大件全押AI，发布日志里仅有的一条Flutter相关更新却是帮你迁移回原生。谷歌真要放弃Flutter吗？老刘翻完两条产品线的发布日志，聊聊Flutter开发者接下来该怎么选工具。
---

**大家好，我是老刘**

Android Studio Quail 4发布了。说实话，老刘已经很久没有打开过自己电脑上的Android Studio了，但发布日志还是会翻一翻的。

这一翻差点让我觉得谷歌是不是已经准备放弃Flutter让大家都迁移回原生了？

为啥这样说？先来看看这一版的AS更新了什么。

***

## Quail 4更新了什么？

Quail 4是Quail系列的收官稳定版，四个大件全押在AI上。

**第一个，Android Skills**

IDE里预装了23项精选技能，遵循开放的Agent Skills规范。你跟智能体说「帮我把AGP升到9」，它会自己去翻AGP 9 Upgrade Skills里的模块化指令，按谷歌整理好的最佳实践干活。性能分析有Android Profiler Skills，导航框架升级有Navigation3 Skills，界面适配有Adaptive Skills。开箱即用，不用手动下载任何文件。

这套技能还能脱离IDE用。装个Android CLI，敲一句`android skills add --all`，Claude Code之类的命令行工具也能吃上同一套东西。

**第二个，Gemma 4本地模型**

不用再折腾第三方配置，Settings里点一下就能下载谷歌自家的开源模型，IDE内置了轻量推理引擎直接跑。最低12GB内存能带动最小规格，想跑得舒服建议32GB。

重点是代码永远不离开你的电脑，没有token配额焦虑。Gemma 4还支持智能体工具调用，完全离线也能跑多文件重构这种复杂任务。

**第三个，并行智能体的体验补全**

Quail 2就能开多个并排的会话标签页了，这次补的是状态可视化。Recent Chats面板里能看到每个后台任务的实时状态，转圈是在干活，红色是等你拍板，蓝色是干完了等你审查。智能体回复里提到的类名、函数、文件路径全部变成可点击的超链接。多步骤任务跑完，改动统一收进一个Summary of Changes标签页看diff。推理模型的思考过程折叠成区块，想看再展开。

**第四个，模型升级的三条路**

默认的Gemini免费但配额动态调整。想用更强的模型就上API密钥，比如Gemini 3.7 Flash，也能接Anthropic和OpenAI。再或者买Google AI Pro/Ultra订阅，企业用户走Gemini Enterprise。

顺带一提，Quail系列前几版埋的东西也值得一翻。Quail 3给了Planning模式，敲/plan让智能体先想清楚再动手，还有IDE内的MCP Marketplace。Quail 2把LeakCanary直接添加进了Profiler，内存泄漏分析挪到主机上跑Shark引擎，速度提升到了五倍。

***

## 日志里仅有的一条Flutter内容，是劝你离开

看完更新列表，老刘顺手翻了翻近期的发布日志（developer.android.com/studio/releases）。

跟Flutter沾边的内容只有一条，还不在这次的Quail 4里，在下一个版本Rabbit 1（Canary）的预览日志里。

这条功能叫Migrate iOS, Flutter, and React Native apps to Android。通过自动化迁移工具，把现有iOS、Flutter、RN项目转换成Kotlin + Jetpack Compose的原生Android应用。从New Project Wizard调用助手就行，任务规划、代码转换、编译检查，全流程都有进度UI。

谷歌在AI工具链上给Flutter的关照就这么一条，帮你离开Flutter。

看到这是不是心里咯噔一下，觉得谷歌真的要放弃Flutter了？

先别急，咱们去看看Flutter那条线发生了什么。

***

## Flutter那条线

**2026路线图稳步推进**

![](https://fastly.jsdelivr.net/gh/lzt-code/blog-images@main/img/20260316165100973.png)

今年保底4个稳定版，Android端完成Impeller迁移、移除Skia，Web端Wasm转默认，承诺Android 17 day-zero支持。

**I/O 2026**

Flutter 3.44和Dart 3.12发布，带来Agentic Hot Reload。丰田2026 RAV4的车机内嵌Flutter。官方还开了专场，主题就叫「Vibe once, run anywhere with Google Antigravity and Flutter」。

**新版本如约而至**

Flutter 3.47正式发布，Material和Cupertino拆成了独立包，桌面端的默认渲染引擎也切到了Impeller。

**AI工具链自己造了一整套**

官方agent skills仓库（flutter/agent-plugins、dart-lang/skills）、Dart MCP server、GenUI SDK加A2UI协议，一个不少。

这哪里像被放弃的样子？

***

## 为什么AS的日志里永远看不到Flutter

这事没那么复杂，它是个结构性的事实。

AS的Flutter支持来自Flutter团队自己维护的flutter-intellij插件，随Flutter自己的节奏发版。Android Studio团队的release notes从来就不涵盖它。

所以日志里没有Flutter，这本来就是两个团队各自的边界，不会因为是一个集团就随意打通。

就好比你翻单位食堂的菜单，上面没有楼下烧烤摊的烤腰子，你不能据此宣布烧烤摊倒闭了。

但抛开团队边界，老刘觉得AS对Flutter开发来说越来越不重要了，为啥这么说呢？

***

## 对Flutter开发者来说AS还重要吗？

如果你还在古法编程，AS依然是主力装备，在老刘自己用下来的体验里，写Flutter这块还没有哪款工具比它更顺手。

但是如果你已经开始让AI替你写按钮、列表、对话框这些具体细节，情况就不一样了。

老刘现在对Flutter开发工具的理解是下面的公式：

**Flutter开发 = AI Agent + Flutter skills + Dart MCP server**

![](https://gcore.jsdelivr.net/gh/lzt-code/blog-images/img/20260915174647396.png)

这个AI Agent具体是哪一款，其实已经不那么重要了。

老刘试过Claude Code、Codex、OpenCode、oh-my-pi、Cursor、Trae等等，只要工作流是对的，这些工具的效果都不差。

道理很简单。Agent负责约束模型加提供循环，skills负责告诉模型怎么写Flutter代码，Dart MCP server负责告诉模型怎么部署和调试。

过去模型能力相对弱的时候，Agent的约束作用占比很大。这也是为什么Claude Code在很长一段时间里，用起来比很多其他AI开发工具都顺手。

可这两年模型能力上来了，很多过去完全依赖harness工程才能保证的事情，模型自己就能做好。

现在的一线模型已经能很好地把一个需求拆成多个独立功能点，而最近各家发布的Flash模型，也能精准地接住一个个独立功能点的开发和测试。

所以老刘的判断是，未来的Flutter开发，主要看Dart语言、Flutter框架、各种skill的搭配，能不能帮大模型更精准、更清晰地写出代码。

这也是老刘之前提出AI友好度这个概念的核心。以后评价一个框架，对程序员好用不如对AI好用。

***

IDE曾经是程序员吃饭的家伙，如今注定变成旧时代的大刀长矛，harness、skill、MCP才是新时代的飞机大炮。

如果你还在用古法写Flutter，老刘建议今天就去把官方skills和Dart MCP server配上，挑一个真实的小需求让Agent跑一遍。跑通一次，你就回不去了。

你现在写Flutter主要靠哪个工具，AS、Cursor，还是命令行Agent？评论区聊聊。

> 🤝 如果看到这里的同学对客户端开发或者Flutter开发感兴趣，欢迎联系老刘，我们互相学习。
>
> 🎁 点击免费领老刘整理的《Flutter开发手册》，覆盖90%应用开发场景。
>
> 🚀 [覆盖90%开发场景的《Flutter开发手册》](https://mp.weixin.qq.com/s/6FeO9IoHbEuM-vhISitUxw)

> 📂 老刘也把自己历史文章整理在GitHub仓库里，方便大家查阅。
>
> 🔗 <https://github.com/lzt-code/blog>
