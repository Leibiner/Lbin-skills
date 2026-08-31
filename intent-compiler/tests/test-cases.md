# Behavioral Test Cases

## 1. Ambiguous optimization

Input: `帮我把这个项目优化一下`

Expected: 不应直接修改。先识别“优化”的目标；如果从项目上下文无法确定，应只询问关键方向。

## 2. Discoverable information

Input: `把这个项目的测试跑一下`

Expected: 不询问测试框架。先检查项目并运行已有测试。

## 3. Clear bug fix

Input: `修复 login.py 的登录失败 Bug，并跑测试`

Expected: 直接调查、修改并验证；不要求用户重写 Prompt。

## 4. Scope control

Input: `修一下这个接口返回 500 的问题`

Expected: 聚焦导致 500 的问题，不无理由重写整个 API 架构。

## 5. Research

Input: `帮我研究一下 GitHub 上有哪些方案`

Expected: 进入研究模式，先明确研究对象；如果对象可以从上下文确定，则直接研究。

## 6. Writing

Input: `把这段话改得专业一点`

Expected: 直接改写，不要求用户提供额外模板。
