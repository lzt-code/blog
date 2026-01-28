# Dart宏被砍掉的真相：为什么Go、Python、Java等高级语言都拒绝宏？

**哈喽，我是老刘**

前两天的文章讲了老刘对Dart宏功能的期待和Dart官方取消宏的一点观点。

[Dart的宏取消了，期待3年的功能，说没就没了？](https://mp.weixin.qq.com/s/VtQ2D4cEOVnUTuPJ3-xkig)

有人评论说高级编程语言是不需要宏功能的。

虽然老刘自己是非常支持宏的，但是不得不说这个观点其实也是有一定的道理的。

为啥这么说呢？

接下来我就来对比一下C语言的宏和Dart的build_runner，看看各自的优劣在哪里。

相信对比完大家也就能理解两种处理代码的方式各自的优劣，以及Dart团队在宏功能上的野望。

## 相同点：编译时代码生成的共同优势

虽然C语言宏和Dart的build_runner在实现机制上截然不同，但它们的目标却是一致的。

都是为了在编译之前就把事情搞定，避免运行时的各种开销。

**第一个共同点：编译前代码生成**

想象一下，你写了一个JSON序列化的代码。

如果用运行时反射，每次序列化都要通过反射去读写对象的属性。

但如果用编译前代码生成，编译器直接帮你生成好了专门的序列化代码。

运行时直接调用，速度肯定是提升了很多。

**第二个共同点：告别样板代码地狱**

写过Java的同学都知道，getter和setter能把人写到怀疑人生。

写过C++的同学也知道，各种重复的函数声明和实现能让人抓狂。

C语言宏可以这样解决：

```c
#define GETTER_SETTER(type, name) \
    type get_##name() { return this->name; } \
    void set_##name(type value) { this->name = value; }
```

Dart的build_runner也能实现类似的功能，比如json_annotation：

```dart
@JsonSerializable()
class User {
  final String name;
  final int age;
}
```

编译器自动生成fromJson和toJson方法。

一行注解，省下几十行代码。

## 关键差异：实现机制的不同

说完了相同点，咱们来聊聊最核心的差异。

**文本替换 vs 语义理解：两种截然不同的技术路线**

### C语言宏：文本替换

C语言的宏本质上就是一个文本替换工具。

编译器在词法分析之前，预处理器就把宏展开了。

举个例子：

```c
#define PI 3.14159
#define SQUARE(x) ((x) * (x))

double area = PI * SQUARE(radius);
```

预处理器会直接替换成：

```c
double area = 3.14159 * ((radius) * (radius));
```

C语言的宏本质上就是文本替换。

预处理器不理解代码语义，只是把宏名替换成宏体。

当然这个替换不是简单机械的，而是可以通过条件判断来实现不同场景的替换。

### Dart build_runner：基于AST的智能生成

Dart的build_runner完全不同。

它工作在AST（抽象语法树）层面，真正理解Dart语言的语法和语义。

比如json_serializable这个包：

```dart
@JsonSerializable()
class User {
  final String name;
  final int? email;
  final DateTime createdAt;
}
```

build_runner会：

1. 解析这个类的AST结构
2. 理解每个字段的类型
3. 知道哪些字段可以为null
4. 生成类型安全的序列化代码

生成的代码可能是这样的：

```dart
Map<String, dynamic> _$UserToJson(User instance) => <String, dynamic>{
      'name': instance.name,
      'email': instance.email,
      'createdAt': instance.createdAt.toIso8601String(),
    };
```

注意，它知道DateTime需要调用toIso8601String()方法。

这就是语义理解的威力。

### 类型安全性：天壤之别

C语言宏最大的问题就是没有类型检查。

```c
#define SWAP(a, b) { typeof(a) temp = a; a = b; b = temp; }

int x = 5;
char* y = "hello";
SWAP(x, y);  // 预编译通过，但逻辑错误
```

而Dart的build_runner生成的代码是完全类型安全的：

```dart
// 如果你的字段类型不支持JSON序列化
class User {
  final File file;  // File类型无法序列化
}
```

build_runner会直接报错，告诉你这个类型不支持序列化。

错误信息清晰明了，开发时就能发现问题。

### 作用域和卫生性

C语言宏还有一个致命问题：不卫生（non-hygienic）。

```c
#define SWAP(a, b) { int temp = a; a = b; b = temp; }

int main() {
    int temp = 10;
    int x = 5, y = 7;
    SWAP(x, y);  // temp变量冲突！
}
```

宏展开后：

```c
int main() {
    int temp = 10;
    int x = 5, y = 7;
    { int temp = x; x = y; y = temp; }  // 变量名冲突
}
```

这种问题在复杂项目中就可能会造成很多难以定位的bug。

Dart的build_runner完全不会有这个问题。

它生成的代码遵循正常的Dart作用域规则，不会产生任何意外的变量捕获。

生成的代码就像手写的一样规范。

## C语言宏的独特优势

说了这么多build_runner的好处，是不是觉得C语言宏已经过时了？

别急，老刘要为C语言宏正名了。

有些事情，build_runner真的做不到，而C语言宏却能轻松搞定。

### 真正的条件编译

最典型的例子就是DEBUG_PRINT。

在C语言中，你可以这样写：

```c
#ifdef DEBUG
#define DEBUG_PRINT(x) printf("Debug: %s\n", x); expensive_memory_check()
#else
#define DEBUG_PRINT(x) // 完全消失，不产生任何代码
#endif
```

注意这里的关键：在Release模式下，DEBUG_PRINT(x)这行代码完全不存在。

不是被优化掉，不是被跳过，而是根本就没有这行代码。

连函数调用的开销都没有，连参数计算的开销都没有。

这就是真正的条件编译。

### Dart的替代方案

Dart当然也有类似的机制，比如kDebugMode常量：

```dart
if (kDebugMode) {
  print('Debug: $message');
  expensiveMemoryCheck();
}
```

看起来很像对吧？

但是有个问题：虽然kDebugMode是编译时常量，但是这些代码是真实存在的。

虽然可以通过Dart的tree-shaking能力来移除这些代码，但是这个效果还是有限的。

特别是当你的调试代码比较复杂时，编译器不一定能完全优化掉。

而且另一个问题是每次打印debug信息都需要手动添加kDebugMode判断，真正写过代码的人都知道这是个非常麻烦的事。

还有assert语句：

```dart
assert(() {
  print('Debug: $message');
  expensiveMemoryCheck();
  return true;
}());
```

assert在release模式下确实会被完全移除。

但是语法太不优雅了，而且使用场景受限。

你总不能把所有调试代码都塞到assert里面吧？

### build_runner的根本局限

为什么build_runner做不到真正的条件编译？

这是由它的工作机制决定的。

**时机问题**：build_runner是在编译前生成代码，它无法根据编译模式（debug/release）来差异化生成代码。

**作用域限制**：build_runner只能生成新的文件，无法在调用点进行条件替换。

**语义层面**：build_runner工作在AST（抽象语法树）层面，而条件编译需要更底层的预处理器支持。

举个例子，你想用build_runner实现DEBUG_PRINT，最多只能生成这样的代码：

```dart
void debugPrint(String message) {
  if (kDebugMode) {
    print('Debug: $message');
  }
}
```

但这样的话，函数调用本身还是存在的。

参数的计算也还是存在的。

如果你传给debugPrint的调试信息需要复杂计算，这些计算在release模式下依然会执行。

### 性能敏感场景的差异

在一些性能敏感的场景下，这种差异就很明显了。

比如游戏引擎的渲染循环，每帧可能要执行数万次的调试检查。

C语言宏可以让这些检查在release版本中完全消失。

而Dart的方案，即使被优化，也可能留下一些痕迹。

当然，对于大多数应用开发来说，这点性能差异可能不重要。

但在某些特定场景下，这就是C语言宏不可替代的优势。

## 开发者体验

说完了技术层面的差异，我们再来聊聊开发者体验。

### C语言宏：无感知的完美体验

C语言宏最牛逼的地方，就是你完全感觉不到它的存在。

写代码的时候，你就像写普通代码一样。

编译的时候，编译器自动帮你处理好一切。

IDE的语法高亮、代码补全、错误提示，全都是即时可用的。

你不需要记住任何额外的命令。

不需要等待任何生成过程。

不需要担心生成的代码是否最新。

举个例子，你在写一个C项目，定义了一个DEBUG_PRINT宏：

```c
#ifdef DEBUG
#define DEBUG_PRINT(fmt, ...) printf("Debug: " fmt "\n", ##__VA_ARGS__)
#else
#define DEBUG_PRINT(fmt, ...)
#endif
```

然后在代码里直接用：

```c
DEBUG_PRINT("User login: %s", username);
```

IDE立马就能识别这个宏，给你语法高亮。

编译的时候，根据是否定义了DEBUG，这行代码要么变成printf调用，要么完全消失。

整个过程，你作为开发者完全不需要干预任何事情。

### build_runner：需要人工干预

再看看Dart的build_runner，体验就完全不同了。

首先，你得记住一堆命令：

```bash
dart run build_runner build    # 生成代码
dart run build_runner watch    # 监听文件变化
dart run build_runner clean    # 清理生成的文件
```

这还只是基础的。

如果你想要增量构建，你得用watch模式。

但watch模式有时候会卡住，你得手动重启。

更要命的是，在代码生成之前，IDE会显示一堆错误。

比如你写了这样的代码：

```dart
@JsonSerializable()
class User {
  final String name;
  final int age;
  
  User({required this.name, required this.age});
  
  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
  Map<String, dynamic> toJson() => _$UserToJson(this);
}
```

在你运行build_runner之前，IDE会告诉你：

"_$UserFromJson未定义"
"_$UserToJson未定义"

满屏的红色波浪线。

新手看到这种情况，第一反应可能是：我是不是写错了什么？

### IDE集成的不完善

虽然现在的IDE（比如VS Code、Android Studio）对build_runner有一定的支持。

但远远达不到C语言宏那种无缝集成的程度。

比如，你在VS Code里修改了一个带注解的类。

IDE不会自动触发代码生成。

你得手动运行命令，或者依赖watch模式。

而watch模式有时候会出现问题：

- 文件变化没有被检测到
- 生成过程卡住了
- 和其他工具冲突

这些问题，在C语言的宏系统里是不存在的。

总结一下，在开发者体验方面：

**C语言宏**：
- 零干预，完全透明
- IDE支持完美
- 无需记忆额外命令
- 无稳定性问题

**build_runner**：
- 需要手动执行命令
- IDE集成不完善
- 需要学习和记忆工作流程
- 存在稳定性和性能问题
- 多包项目复杂性高

这就是为什么很多开发者怀念宏功能的原因。

不仅仅是因为build_runner功能不够强大。

还是因为它在用户体验上，确实有很大的改进空间。

相信看到这里大家也能明白当初dart团队对宏的野心有多大了，他们既想要build_runner的先进性，也想要C语言宏的各种优势。

但是通过前面的对比我们可以发现，这两者各自的优势都直指对方的劣势。

而这种结果都是源于他们底层的实现逻辑。

想要不付出任何代价的集合两者的优势，同时又不引入任何的副作用，似乎有点异想天开。

我想可能这也就是为什么Dart的宏功能在这样庞大的构想下，开发中碰到了各种难以解决的问题，并最终被放弃的底层原因。

## 七、结论：技术选择的多维度思考

通过前面的深度对比，老刘想说一个很重要的观点：

**技术没有绝对的先进和落后，只有适合和不适合。**

很多人一听到"宏"这个词，就觉得这是古老的、落后的技术。

但事实上，在某些特定场景下，C语言宏的简洁和高效，是build_runner无法比拟的。

同样，很多人觉得build_runner复杂、麻烦。

但在类型安全、语义理解、代码质量方面，它确实比传统宏要先进得多。

也许未来的技术发展方向，就是在保持先进性的同时，不断优化开发者体验。

让复杂的技术变得简单易用，让强大的功能变得透明无感。

这可能才是技术进步的真正意义。

**真正的技术高手，不是只推崇一种方案的专家，而是能在不同场景选择最适合工具的智者。技术的先进性不仅体现在功能上，更体现在对开发者体验的关注上。**

好了，如果看到这里的同学对客户端、Flutter开发或者MCP感兴趣，欢迎联系老刘，我们互相学习。
点击免费领老刘整理的《Flutter开发手册》，覆盖90%应用开发场景。
可以作为Flutter学习的知识地图。

[覆盖90%开发场景的《Flutter开发手册》](https://mp.weixin.qq.com/s?__biz=MzkxMDMzNTM0Mw==&mid=2247483665&idx=1&sn=56aec9504da3ffad5797e703c12c51f6&chksm=c12c4d11f65bc40767956e534bd4b6fa71cbc2b8f8980294b6db7582672809c966e13cbbed25#rd)