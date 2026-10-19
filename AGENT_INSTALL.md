# 让 agent 自己装

> 这个文件是写给 agent 看的，也是写给人看的：人负责把下面整段复制过去。

## 前提

agent 需要：**读写文件**、**跑 python**、能看见这个仓库的路径。

## 复制这段

```
我要在这个项目里加一个文件式记忆库。

1. 先读 <仓库>/README.md 和 <仓库>/docs/01-why.md。
2. 把 <仓库>/template/memory 复制成 <项目>/memory。
3. 按 <仓库>/docs/02-layers.md 的判据，把能确定的先填；
   不确定的留空并标 TODO，不要编。
4. 运行 python <仓库>/tools/build_index.py --root <项目>/memory。
5. 最后回给我：读了哪些文件、填了哪几处、留空了哪几处、索引生成了没有。
```

## 人验收这一遍

- [ ] 打开 `memory/facts/*.yaml`，每条都有 `source`；没有出处的删掉
- [ ] 打开 `memory/entries/`，第一条里没有编造的事
- [ ] `memory/INDEX.md` 顶部的「待复核」是空的（还没到期的）
- [ ] `memory/README.md` 已经放进 agent 指令

## 为什么第 3 步要写「不要编」

绝大多数 agent 装到这一步都会「顺手把空填上」——它不知道你的城市，就猜一个；不知道你在做什么，就按目录名编。

编完之后没人发现，库就脏了。**空着比编造好**：空着是 TODO，编造是负债。

## 装完还想加东西

- 常想起来的事 → 写进 `memory/topics.txt`
- 重复踩的坑 → 写进 `memory/experience/`
- 换了机器、换了项目 → 更新 `memory/facts/04_environment.yaml`

都改完再跑一次索引。
