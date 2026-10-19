# 事实记录的写法

`facts/` 是**唯一权威的事实源**。别的文件可以引用它，但不要复制它。

## 一条记录

```yaml
records:
  - id: workplace             # 唯一、稳定；别用中文，别改
    value: "某公司 · 运维"     # 事实本身，一句话
    updated_at: 2026-03-01    # 这条事实何时确认
    source: 用户自述           # 从哪知道的
    confidence: high          # high / medium / low
    note: ""                  # 可选：边界、例外
```

## 规矩

- `id` 一旦用了就别改；真要改，旧的标 `superseded_by`，新的另起一条。
- `value` 写事实，不写评价。「他最近很累」不是事实；「他连续上了 6 天夜班」是。
- `source` 必须写。没有出处的条目，等于谣言。
- `confidence` 是给自己看的：`low` 的条目，用之前先问一句。
- 顶层 `last_updated` 只是文件的日期，**每条的 `updated_at` 才算数**。

## 什么不该进这里

- 一次性的对话内容 → 写 `entries/`
- 怎么装、怎么修 → 写 `knowledge/`
- 「这个人靠不靠谱」→ 不进库；库只记发生过什么
