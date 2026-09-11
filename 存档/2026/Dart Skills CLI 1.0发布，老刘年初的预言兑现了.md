---
title: Dart Skills CLI 1.0发布，老刘年初的预言兑现了
date: 2026-09-10
tags:
  - Dart
  - Flutter
  - AI编程
  - Skills
  - 技术趋势
description: Dart官方发布Skills CLI 1.0，三方库可以随包给AI带一份说明书了。老刘年初关于skill将成为库标配的判断正在兑现，聊聊这个工具链会给库作者和使用者带来哪些变化。
---

# Dart Skills CLI 1.0发布，老刘年初的预言兑现了

**大家好，我是老刘**

今年年初Flutter官方skill发布的时候，老刘表达过一个观点：

> 官方的Skills将是未来开发框架和三方库的标配，就好像现在的官方文档一样。

当时的文章在这里：[Flutter 官方Skill发布，对开发者意味着什么？](https://mp.weixin.qq.com/s/OovZG3aO383EvAvfHvyJpQ)

那篇文章里老刘说自己是躺床上看的。前两天看到Dart官方发布的Skills CLI 1.0，老刘站起来了😄。

这个工具把老刘年初的判断，正式变成了Dart生态工具链里的一环。

***

## Dart Skills CLI 1.0 是个啥？

具体信息可以看官方博客：

> 官方博客文章《Skills CLI 1.0: Bundle and distribute AI agent skills for your packages》
>
> 博客链接 <https://dart.dev/blog/skills-cli-1-0-bundle-and-distribute-ai-agent-skills-for-your-packages>
>
> 作者是Dart团队的Jake Macdonald，发布于2026年9月8日，就在两天前。

简单来说，Skills CLI 1.0是Dart团队发布的一个命令行工具，最早由Serverpod实现，现在由Dart团队亲自接手维护和发布。

它要求包的作者多做一件事，把描述这个仓库如何使用的skill放进仓库的 skills/ 目录里，随包一起发布。目录结构长这样：

```
my-project/
├── src/
├── skills/      <--- skill放这里
├── pubspec.yaml
└── README.md
```

官方推荐用 `dart run skills@` 的语法来运行，这个写法会始终以全局工具的方式跑CLI的最新版本。对库的使用者来说，它能做这几件事：

1. **发现并安装依赖自带的skill**

   在项目根目录跑一句 `dart run skills@ get`，CLI会扫描pubspec.yaml里的直接依赖，找出哪些库打包了skills目录，列出可用的skill让你挑着装。

2. **增量更新**

   后续再跑这个命令，只会显示新增、更新、删除或者之前跳过的skill。想省事的话可以加 `--all` 一键全装。

3. **版本一致**

   skill和依赖包的版本绑定在一起，不会出现skill写的是新用法、项目里锁的库却是旧版本的错配问题。

4. **从任意Git仓库安装skill**

   `dart run skills@ add <git-url>` 可以安装不依附于任何Dart包的通用skill。之前在skills.sh这类聚合站上看到的skill，把 `npx skills` 换成这个命令就能直接装。

5. **不需要Node.js**

   纯Dart实现。对Dart和Flutter开发者来说，管理skill这件事终于不用绕到Node的工具链里去了。

从官方博客列出的例子看，Jaspr、Serverpod、Flutter Scene、GenUI这些包已经开始随包带skill了。

***

## 工业化的新标准

聊完工具本身，老刘想聊聊背后的趋势。

现在你的项目要集成一个三方库，你还会像过去一样，先通读一遍说明文档，再看看demo代码，然后自己动手集成吗？

反正老刘是不会了。我现在的做法一般是把pub或者GitHub仓库的地址丢给AI，让它直接集成到项目里。

当然，AI集成的效果有时候也不尽如人意。

比如Flutter的状态管理库，通常会有好几种不同的使用方案。AI选的那个方案，经常和项目里真正合适的那一个对不上，你得再额外给它加一堆约束，它才能把事情做对。

老刘觉得一个很重要的原因是出在文档上。

很多项目的文档写得比较随意，结构也不清晰，接口设计的再非主流一点，AI对功能的判断就容易出偏差。毕竟文档是写给人看的，人能脑补，AI不行。

这种情况下，如果能给AI提供一份专门写给AI看的使用说明书，而且这份说明书由库的作者自己用AI生成、跟着版本一起维护，前面说的踩坑概率就会小很多。

这也是为啥老刘在年初那篇文章里的判断，skill会成为和官方文档平级的交付物。

简单来说就是，官方文档是给人看的说明书，skill是给AI看的说明书。

以后一个库受不受欢迎，skill写得好，可能比文档写得好更有吸引力。因为你的agent能用的更好。

现在官方亲自下场为这件事提供工具链，说明这个判断已经从预测变成了业界的主流共识。

工具链跟到哪一步，生态的共识一般就已经走到了哪一步。

![skill 作为和项目说明文档平级的交付物](https://fastly.jsdelivr.net/gh/lzt-code/blog@main/存档/2026/assets/standard_evolution.png)

***

## 还需要做什么？

聊到这里，老刘再次斗胆预测一下，Dart Skills CLI只是一个开始。

因为它只帮库的使用者解决了以下问题，怎么方便地装skill，怎么让skill和仓库版本保持同步。

而库的作者这一侧，问题还悬着。

每次发布新版本，怎么保证skill跟着更新了？怎么保证写出来的skill，能让使用者的AI充分理解这个库的用途和用法？

这些都是后续要解决的问题。如果能有大的组织机构站出来，把描述库使用方式的skill结构做成一份更具体的协议，对整个生态会是件好事。

老刘的团队目前已经在项目里做了几个限制：

1. 对外提供API的模块和独立仓库，要求配一份md格式的API说明文档。不强制，但推荐用skill的方式来写。
2. 这份文档的结构和必须包含的元素，通过skill的方式进行约定。换句话说，我们用一个skill帮助agent写这个说明文档的skill。
3. 发布前的检查环节，会验证文档和对应的代码修改是否一致。

***

## 写在最后

从年初的官方skill，到现在的官方工具链，老刘年初的判断正在一步步变成现实。

接下来就看生态里的库作者们有没有及时跟进了。

如果你是库的作者，老刘建议你把skills尽早作为发布的一部分，甚至比文档更重要的一部分。

如果你是库的使用者，现在就可以在自己的项目里跑一句 `dart run skills@ get`，看看你依赖的库有没有给AI准备好说明书。

最后问大家一个问题，你现在集成三方库，还会自己通读文档吗，还是直接丢给AI？欢迎评论区聊聊。

***

> 🤝 如果看到这里的同学对客户端开发或者Flutter开发感兴趣，欢迎联系老刘，我们互相学习。
>
> 🎁 点击免费领老刘整理的《Flutter开发手册》，覆盖90%应用开发场景。
>
> 🚀 [覆盖90%开发场景的《Flutter开发手册》](https://mp.weixin.qq.com/s/6FeO9IoHbEuM-vhISitUxw)

> 📂 老刘也把自己历史文章整理在GitHub仓库里，方便大家查阅。
> 
> 🔗 <https://github.com/lzt-code/blog>
