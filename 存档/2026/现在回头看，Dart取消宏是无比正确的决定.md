---
title: "现在回头看，Dart取消宏是无比正确的决定"
date: 2026-09-08
tags: [Dart, AI编程, 编程语言, 宏]
description: "AI时代，宏、注解、编译期代码生成这些帮人类少写代码的工具，反而成了AI理解代码的阻碍。老刘认为编程语言将回归简单清晰、AI友好的原始状态。"
---

**大家好，我是老刘**

我记得当时Dart官方宣布取消宏这个功能的时候，我还专门写过一篇文章，表达对宏的期待落空。

[Dart的宏取消了，期待3年的功能，说没就没了？](https://mp.weixin.qq.com/s/VtQ2D4cEOVnUTuPJ3-xkig)

为啥我如此看重宏这个功能呢？

因为在古法编程的年代，宏是让程序员少写大量重复代码，同时保持代码语义的重要手段之一。

举个例子，你有一段重复性很高的代码，比如为每个数据类都要写getter、setter、toString、hashCode……

宏可以让你只写一行注解，编译器自动帮你生成这些代码。

比如在c++中可以这样写。

```C++
#define DECLARE_GETTER_SETTER(type, name) \
private: \
    type name##_; \
public: \
    type get##name() const { return name##_; } \
    void set##name(const type& value) { name##_ = value; }


class User {
    DECLARE_GETTER_SETTER(std::string, Name)
    DECLARE_GETTER_SETTER(int, Age)
};
```

一个简单的宏定义，就能自动生成getter和setter方法，你定义的所有类都不需要再写一遍模板化的内容了。

如果没有宏，这几十行代码就得全部手写。

更关键的是，这种宏的定义方式是包含语义的。别的程序员读到这里，很容易明白`DECLARE_GETTER_SETTER`这行代码在干什么。

那为什么我现在又说，当初Dart取消宏是无比正确的决定呢？

***

## 时代变了

![](https://gcore.jsdelivr.net/gh/lzt-code/blog-images/img/20260908160738251.png)

因为帮人类程序员写代码的神器，也可能变成让AI看不懂代码的元凶。

AI时代最大的改变，可能就是那些具体的代码细节，真的不需要程序员一行一行手写了。

老刘自己已经很久没有写过一个按钮、一个列表、一个对话框了。

这些具体而细节的功能，交给一个flash-lite级别的模型都能完成得很好。

但过去手写代码时帮我们极大节省时间的这些工具，宏、注解、编译期代码生成，现在反而成了AI理解代码的最大阻碍。

因为这三者本质上是同一类东西，你写在文件里的并不是最终代码，真正的代码要等编译过程才动态生成。

人类可以靠语义去理解一个宏或注解是干什么的，但AI看不到最终生成的代码，它的理解就可能出现很大偏差。

所以当具体的那一行行代码不再需要人类手工编写时，这些曾经帮我们少写代码、简化代码的工具，反而成了开发的阻碍。

换句话说，语法糖的意义在AI时代被最大程度地削弱了。

***

## 未来编程语言的演化

老刘个人的观点，未来编程语言的演化方向应该是在保留人类可读的基础上，尽可能提升AI友好度。

过去编程语言的发展，有百分之七八十都是为了帮人类更高效地写代码。

比如更简洁的语法。下面是一个典型的Dart注解例子。

```dart
@freezed
class User with _$User {
  const factory User({
    required String name,
    required int age,
  }) = _User;
}
```

一行`@freezed`注解，编译期自动生成`==`、`hashCode`、`toString`、`copyWith`、`fromJson`、`toJson`等全部模板代码。

注解帮你省掉的，就是这几十行模板代码。而且这种优化不仅写得少，读起来也更省事。

但AI在理解这段代码时，看不到`_$User`和`_User`的最终实现，因为它们是编译期动态生成的，对AI来说就是黑盒。

如果你的代码都是AI生成的，那这种优化对AI来说只能是负向的优化。

所以老刘的看法是，未来这类编程语言优化或者第三方优化都会逐步消失。

编程语言会回到简单清晰但略显繁琐的原始状态，就像下面这种不用注解的写法。

```dart
class User {
  final String name;
  final int age;

  const User({required this.name, required this.age});

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is User && name == other.name && age == other.age;

  @override
  int get hashCode => Object.hash(name, age);

  // toString、copyWith、toJson、fromJson 同理，略去约20行
}
```

这种代码的AI友好度最高，AI理解起来最准确，生成起来也最简单，轻量级模型就能完全胜任。

简单来说，虽然写起来没那么高效，但已经完全不需要人手写了。越是标准化的代码，AI生成得越准确、越高效。

编程语言的语法，只要保证人类能看懂就行。

现在回看当初那篇文章对宏的期待，不如说是一个古法编程的程序员对手搓代码最后的留恋。

时代变了，留恋也就成了执念。

***

> 🤝 如果看到这里的同学对客户端开发或者Flutter开发感兴趣，欢迎联系老刘，我们互相学习。
>
> 🎁 点击免费领老刘整理的《Flutter开发手册》，覆盖90%应用开发场景。
>
> 🚀 [覆盖90%开发场景的《Flutter开发手册》](https://mp.weixin.qq.com/s/6FeO9IoHbEuM-vhISitUxw)

> 📂 老刘也把自己历史文章整理在GitHub仓库里，方便大家查阅。
> 
> 🔗 <https://github.com/lzt-code/blog>
