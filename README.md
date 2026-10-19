# agent-memory-kit

> 文件式 agent 记忆库。复制过去，让你的 agent 别再每次开窗都失忆。

不开数据库，不上向量库（除非你真的需要）。
一个文件夹、一套判据、一个索引脚本。

---

## 它解决什么

agent 的上下文是有限的：新开一个窗，昨天说好的事就没了。

这个仓库给 agent 一份**放在磁盘上的记忆**——人能读、能改、能备份，换模型也不用搬家。

---

## 你是哪一种

| 你在做什么 | 从这里开始 |
|---|---|
| 在跑长期 agent，它老忘事 | [为什么用文件](docs/01-why.md) → [怎么用](docs/04-workflow.md) |
| 在做陪伴型 agent | [这一篇](docs/07-for-companion.md) |
| 只是来看架构 | [分层判据](docs/02-layers.md) |
| 想直接上手 | 往下看「10 分钟开始」 |

---

## 10 分钟开始

### 自己装

```bash
cp -r template/memory ./memory
# 打开 memory/topics.txt，先填 5 个你最常想起来的词
python tools/build_index.py --root memory
```

然后把 `memory/README.md` 的内容放进你的 agent 指令里
（`AGENTS.md` / `CLAUDE.md` / 系统提示词，放哪都行）。

### 让 agent 自己装

把 [AGENT_INSTALL.md](AGENT_INSTALL.md) 整段发给它。
它需要会读写文件、会跑 python。

---

## 里面有什么

```
template/memory/     空库骨架：复制这个目录，就是你的库
  facts/             事实层（YAML，唯一权威源）
  entries/           按日期：某天发生了什么
  knowledge/         脱离项目也成立的技法
  experience/        跨项目可复用的经验
  assets/            原始材料，只存不读
tools/build_index.py 生成 INDEX.md 和 entries/CATALOG.md
tools/check.py       只读自检：front-matter、重复 id、断链
docs/                为什么这么设计、怎么用、踩过的坑
examples/demo/       一个填满的假库（虚构用户「小林」）
```

---

## 它不做什么

- **不是向量库的替代品。** 几百到几千条，文件 + 索引足够；到了要语义检索的量级，再上向量库。
- **不替你判断。** 晋升、降级、删不删，脚本只报告，人拍板。
- **不装人格。** 人格回答「我是谁」，库回答「什么是真的」。混在一起，库会变成剧本。

---

## 看一个填满的例子

[`examples/demo/`](examples/demo/) 是一个虚构用户「小林」的迷你库。
跑完索引的样子在 [`examples/demo/memory/INDEX.md`](examples/demo/memory/INDEX.md)。

---

## 为什么是文件

- **可读**：打开就能看，不需要工具
- **可 diff**：每次改动都能看见
- **可迁移**：换模型、换框架、换机器，库不动
- **可审计**：谁在什么时候写了什么，有出处

详见 [docs/01-why.md](docs/01-why.md)。

---

## 目录

| 文件 | 管什么 |
|---|---|
| [docs/02-layers.md](docs/02-layers.md) | 一条信息该进哪层 |
| [docs/03-lifecycle.md](docs/03-lifecycle.md) | 重 / 中 / 轻、复核、晋升降级 |
| [docs/04-workflow.md](docs/04-workflow.md) | 开窗读什么、什么时候写、收尾做什么 |
| [docs/05-pitfalls.md](docs/05-pitfalls.md) | 我们踩过的坑 |
| [docs/06-for-long-running.md](docs/06-for-long-running.md) | 长期 agent 的最小用法 |
| [docs/07-for-companion.md](docs/07-for-companion.md) | 陪伴型 agent 的边界 |

---

## License

MIT
