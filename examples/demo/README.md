# 示例库：小林

> 这是一个**虚构**的迷你库，用来展示「填满之后长什么样」。
> 小林是一个虚构的全栈开发者；里面的人名、公司、项目都是假的。

```
examples/demo/memory/
├─ facts/           3 个 YAML
├─ entries/         3 条（core / record / record）
├─ knowledge/       1 篇
├─ experience/      1 篇
├─ decisions.md     1 条
├─ commitments.md   1 条
└─ open-threads.md  4 条
```

跑一遍索引：

```bash
python tools/build_index.py --root examples/demo/memory
```

然后看 `examples/demo/memory/INDEX.md`。
