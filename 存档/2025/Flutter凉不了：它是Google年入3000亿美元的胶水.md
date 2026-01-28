# Flutter凉不了：它是Google年入3000亿美元的胶水

![](https://files.mdnice.com/user/142171/a7d61a33-bcdf-44ff-b806-d972b92cfed4.jpg)

---

**哈喽，我是老刘**

老刘做Flutter开发7年了，这期间很多人都会问一个问题“Flutter会不会凉了？”

前两年在还时不时会传出“Flutter凉了”的消息，可 Flutter 却一直保持着高速发展。

那么你有没有想过这个问题？

不是所有的工具都能活得久，很多技术没几年就被抛弃了。

而 Flutter 作为 Google 的跨平台开发框架，为啥 Google 还在源源不断地投入？

要理解 Flutter 为什么"凉不了"，得先搞明白：**Google 是怎么赚钱的，以及Flutter 在这个赚钱流程中扮演什么角色。**

---

## Google 2024 年收入大盘：钱从哪儿来？

根据 Alphabet 2024 年的财务数据，Google 的收入可以分成三个大板块：

信息来源： https://fourweekmba.com/how-does-google-make-money/

![](https://i0.wp.com/fourweekmba.com/wp-content/uploads/2024/01/how-does-google-make-money.png?resize=1536%2C1159&ssl=1)

| 收入板块 | 2024年金额 | 占比 |
|---------|----------|------|
| 广告业务（搜索、YouTube、AdSense/AdMob） | 2,460亿美元 | 70% |
| Google Cloud（含Workspace） | 550亿美元 | 16% |
| 其他（Play抽成、硬件、订阅服务等） | 490亿美元 | 14% |
| **合计** | **≈3,500亿美元** | **100%** |

**总结一下**：
- 广告是 Google 的绝对主力，占七成收入
- Cloud 和其他业务虽然占比小，但增速很快
- 每个板块的增长都依赖"用户覆盖面"和"流量"

---

## Flutter 与三大收入板块的关系

### Flutter 的三重身份

#### 1️⃣ 广告业务的"流量扩张器"（≈78%）

Google 的广告不仅在搜索页、YouTube 上，还在成千上万个 App 里

每个用 Flutter 开发的 App，都是 Google 广告的一个"新地盘"

**Flutter 的作用**：
- 降低了跨平台 App 开发的门槛
- 开发者用 Flutter 写一次代码，同时登陆 iOS 和 Android
- 2024年6月，Google 发布了正式版 Google Mobile Ads SDK 插件
- 支持开屏广告、原生广告、插屏、激励视频，一套代码 Android/iOS 通用

爆款文字游戏《4 Pics 1 Word》用 Flutter 重写后，直接通过该 SDK 展示插页和激励视频，**收入未受影响**。

这说明什么？

Flutter App 的变现能力 = 原生 App

但开发成本更低、上线速度更快

这会让更多开发者愿意做 App，Google 的广告库存也跟着增加

---

#### 2️⃣ Google Cloud 的"前端入口"（≈16%）

Google Cloud 一直在拼增速，2024 年收入 550 亿，还在高速增长阶段。

但企业用户需要的是"完整解决方案"，不是单纯的云服务。

**Flutter 的新身份**：

![Flutter 在 Google Cloud Next 上的首次亮相](https://storage.googleapis.com/cloudnext-assets/event-assets/25/home/startups/tout.2024-11-10.webp)

2024年5月，Google Cloud Next 大会上，Flutter **首次正式亮相**

展示的不是 Flutter 本身，而是"Flutter + Firebase + Cloud Run + Firestore"的完整闭环，前端用 Flutter，后端全跑在 Google Cloud 上。

**更强的组合**：
- Flutter + Firebase + Gemini API
- 意思是：前端、后端、AI 能力全在 Google 生态内
- 企业客户一站式接入，Google 的 Cloud 资源、Firebase 账单、AI API 调用量都增加了

**底层逻辑**：
```
企业采用 Flutter + Firebase
→ 后端迁移到 Google Cloud
→ 使用 Gemini API
→ 产生 Cloud 资源消耗 + AI API 调用费
→ Google Cloud 营收增加
```

---

#### 3️⃣ 其他收入的"生态粘合剂"（≈5%）

**细分一下**：

**a) Google Play 的抽成**
- Flutter 开发的 App 在 Play 上架后，产生应用内购或付费下载
- Google 照样抽 15–30%
- Flutter 本身没赚钱，但它做的事是：**降低开发门槛 → App 数量增加 → Play 生态供给增加**

**b) 支付系统绑定**
- Flutter 官方提供 In-App Purchase 插件和 Google Pay 集成
- 开发者一键接入，Google 从流水里抽成
- 用户习惯了 Google Pay，Google 的支付生态就越来越强

**c) 硬件生态**
- Flutter 支持在 Android、Linux 嵌入式、甚至 Android-based Nest Hub 上运行
- 硬件本身微利，但可以捆绑 Google One、YouTube Premium 等订阅
- 多屏体验，Google 订阅用户数增加

**底层逻辑**：
```
Flutter App 生态完善
→ 开发者积极性高
→ 优质 App 增加
→ Play Store 体验更好
→ 用户付费意愿增加
→ Google 的 Play 抽成、订阅捆绑收入都增加
```

---

## 为什么说 Flutter 是"胶水"？

Flutter 本身不赚钱。但它像胶水一样：

**把更多开发者** 黏在 Google 的工具链里（而不是 React Native、Swift UI）
**把更多应用** 黏在 Google 的广告网络、Cloud、支付系统里
**把更多最终用户** 黏在 Google 的广告、视频、订阅生态里

结果是什么？

- 广告库存增加 → 广告营收增加
- Cloud 用户增加 → Cloud 营收增加
- Play 生态完善 → 衍生收入增加

**Flutter 的投资回报率看起来不直观，但如果你从"放大器"的角度看，它对 Google 三条主要收入线都起到了乘数效应。**

---

## 总结

**Flutter 凉不了，因为它不是 Google 的负担，而是 Google 最强有力的"赚钱胶水"。**

它把开发者、应用、用户黏在 Google 的广告、云和支付生态里。Google 放弃 Flutter，就相当于从自己的三条主要收入线各砍一刀。

所以，放心用 Flutter 吧——**这是一个被 Google 的商业利益保护着的框架。**

> 如果看到这里的同学对客户端开发或者Flutter开发感兴趣，欢迎联系老刘，我们互相学习。
>
> 点击免费领老刘整理的《Flutter开发手册》，覆盖90%应用开发场景。
>
> 可以作为Flutter学习的知识地图。
>
> [覆盖90%开发场景的《Flutter开发手册》](https://mp.weixin.qq.com/s?__biz=MzkxMDMzNTM0Mw==&mid=2247483665&idx=1&sn=56aec9504da3ffad5797e703c12c51f6&chksm=c12c4d11f65bc40767956e534bd4b6fa71cbc2b8f8980294b6db7582672809c966e13cbbed25#rd)