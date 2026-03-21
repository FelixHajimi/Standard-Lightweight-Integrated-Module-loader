# SLIM

> **S**tandard **L**ightweight **I**ntegrated **M**odule-loader  
> 标准轻量级集成模块加载器

## 项目是干什么用的

你有没有写过这样的代码？

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--name", required=True)
parser.add_argument("--age", type=int)
args = parser.parse_args()

def add_user(name, age):
    print(f"添加用户: {name}, {age}岁")

add_user(args.name, args.age)
```

每次加一个新命令，都要重复这些样板代码。参数多了还要处理类型转换、默认值、校验规则，代码越来越臃肿。

SLIM 把这个过程反过来：**你写函数，SLIM 帮你生成命令行接口**。

```python
def enter(name: any, age: any | None = None):
    print(f"添加用户: {name}, {age}岁")
```

就这么简单。参数从哪来、类型怎么转、命令怎么路由，SLIM 全包了。

## 在什么场景会用到

**场景一：快速原型工具**

今天想写个脚本批量处理文件，明天又想加个新功能。用 SLIM，加一个新命令就像写一个新函数，不用每次重新搭架子。

**场景二：多命令工具集**

像 `git` 那样，有 `git commit`、`git push`、`git log` 多个子命令。SLIM 天然支持命令嵌套，`user add` 和 `user delete` 可以放在不同文件里，互不干扰。

**场景三：团队协作的工具**

有人负责写业务逻辑，有人负责定义命令格式。命令格式写在 `command.json` 里，一目了然。新人接手也能快速看懂有哪些命令、每个命令需要什么参数。

**场景四：需要灵活参数的命令**

有的命令要接收多个值，有的要接收 JSON 配置，有的参数要正则校验。SLIM 的参数语法把这些需求都覆盖了，不用自己写解析逻辑。

## 优势与缺陷

**优势：**

- **声明式参数定义**：`<name> [age]int <tags:0>` 一行搞定参数名、类型、数组、可选性
- **自动类型转换**：字符串自动转 int、float、bool、json，转换失败也不会炸
- **零依赖**：只用 Python 标准库，丢到任何环境都能跑
- **自动生成代码**：`--admin create` 一键生成命令文件，不用手写目录结构
- **多语言支持**：内置中英文，可以扩展更多语言
- **日志记录**：所有命令执行都有日志，方便排查问题

**缺陷：**

- **正则表达式要双重转义**：JSON 里写 `\d` 要写成 `\\d`，刚开始容易忘
- **复杂业务还是自己写**：SLIM 只管命令入口，具体逻辑还是你写
- **只适合命令行**：做 Web 服务、GUI 程序用不上
- **学习成本**：需要理解参数语法规则，但文档很全

## 如何添加新功能

假设你想加一个 `user search` 命令，支持按关键词搜索，可以指定返回数量，还可以传过滤条件。

**第一步：定义命令格式**

打开 `command.json`，添加一行：
```json
{
    "user.search": "<keyword> [limit=10]int [filters:0]json"
}
```
这行配置的意思是：
- `keyword`：必填，字符串
- `limit`：可选，整数，默认 10
- `filters`：可选，接收剩余所有参数，每个参数按 JSON 解析

**第二步：生成代码文件**

```bash
python slim.py --admin create
```
系统会自动创建 `commands/user/search.py`，并根据参数配置生成函数签名。

打开文件，你会看到：
```python
def enter(keyword: any, limit: any = 10, filters: list[any | None] | None = None):
    pass
```

**第三步：写业务逻辑**

```python
def enter(keyword: any, limit: any = 10, filters: list[any | None] | None = None):
    print(f"搜索关键词: {keyword}")
    print(f"返回数量: {limit}")
    if filters:
        print(f"过滤条件: {filters}")
    
    # 在这里写你的搜索逻辑
    # results = search_users(keyword, limit, filters)
    # for user in results:
    #     print(user)
```

**第四步：运行测试**

```bash
python slim.py user search python
# 搜索关键词: python
# 返回数量: 10

python slim.py user search python 5 '{"role":"admin"}' '{"active":true}'
# 搜索关键词: python
# 返回数量: 5
# 过滤条件: [{'role': 'admin'}, {'active': True}]
```

搞定。整个流程不到五分钟，以后想加新命令重复这个流程就行。

## 文档

详细文档在 `docs/` 目录：

```
docs/
├─ English/
│  ├─ Admin mode.md      # 管理员模式：如何管理命令文件
│  ├─ API.md             # 接口文档：框架提供的所有 API
│  ├─ config.md          # 配置语法：参数格式的完整说明
│  ├─ Global config.md   # 全局设置：setting.json 配置项
│  └─ Tools.md           # 工具使用：内置工具（Tran、to_type 等）
└─ 中文/
   ├─ 全局设置.md
   ├─ 工具.md
   ├─ 接口.md
   ├─ 操作员模式.md
   └─ 配置.md
```

建议先看 `config.md`（配置语法），了解如何定义参数；再看 `Admin mode.md`（管理员模式），学会用 `--admin create` 管理命令；需要深入扩展时再看 `API.md` 和 `Tools.md`。