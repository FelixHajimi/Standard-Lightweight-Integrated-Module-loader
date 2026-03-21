# SLIM

> **S**tandard **L**ightweight **I**ntegrated **M**odule-loader

## What the Project Does

Have you ever written code like this?

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--name", required=True)
parser.add_argument("--age", type=int)
args = parser.parse_args()

def add_user(name, age):
    print(f"Adding user: {name}, {age} years old")

add_user(args.name, args.age)
```

Every time you add a new command, you repeat this boilerplate. When there are more parameters, you also have to handle type conversion, default values, and validation rules, making the code increasingly bloated.

SLIM reverses this process: **you write functions, SLIM generates the command-line interface for you**.

```python
def enter(name: any, age: any | None = None):
    print(f"Adding user: {name}, {age} years old")
```

That's it. Where parameters come from, how types are converted, how commands are routed—SLIM handles it all.

## When to Use

**Scenario 1: Rapid Prototyping Tools**

Today you want to write a script to batch process files, tomorrow you want to add a new feature. With SLIM, adding a new command is like writing a new function—no need to set up the scaffolding each time.

**Scenario 2: Multi-Command Tool Sets**

Like `git` with `git commit`, `git push`, `git log` subcommands. SLIM natively supports command nesting. `user add` and `user delete` can live in different files without interfering with each other.

**Scenario 3: Team Collaboration Tools**

Some team members handle business logic, others define command formats. Command formats are written in `command.json`—clear at a glance. Newcomers can quickly understand what commands exist and what parameters each requires.

**Scenario 4: Commands with Flexible Parameters**

Some commands need to accept multiple values, others need to receive JSON configurations, and some require regex validation. SLIM's parameter syntax covers these needs without you having to write parsing logic.

## Advantages and Disadvantages

**Advantages:**

- **Declarative parameter definition**: `<name> [age]int <tags:0>` defines parameter names, types, arrays, and optionality in one line
- **Automatic type conversion**: Strings automatically convert to int, float, bool, json—failure doesn't crash
- **Zero dependencies**: Uses only Python standard library, runs anywhere
- **Automatic code generation**: `--admin create` generates command files in one click—no need to manually create directory structures
- **Multi-language support**: Built-in Chinese and English, extensible to more languages
- **Logging**: All command executions are logged for easy troubleshooting

**Disadvantages:**

- **Regex requires double escaping**: Writing `\d` in JSON requires `\\d`, easy to forget initially
- **Complex business logic still requires manual implementation**: SLIM only handles command entry; specific logic is still written by you
- **Only suitable for command line**: Not useful for web services or GUI applications
- **Learning curve**: Need to understand the parameter syntax rules, but documentation is comprehensive

## How to Add New Features

Suppose you want to add a `user search` command that searches by keyword, can specify the number of results to return, and can accept filter conditions.

**Step 1: Define the Command Format**

Open `command.json` and add a line:
```json
{
    "user.search": "<keyword> [limit=10]int [filters:0]json"
}
```
This configuration means:
- `keyword`: required, string
- `limit`: optional, integer, defaults to 10
- `filters`: optional, captures all remaining parameters, each parsed as JSON

**Step 2: Generate the Code File**

```bash
python slim.py --admin create
```
The system automatically creates `commands/user/search.py` and generates the function signature based on the parameter configuration.

Open the file and you'll see:
```python
def enter(keyword: any, limit: any = 10, filters: list[any | None] | None = None):
    pass
```

**Step 3: Write Business Logic**

```python
def enter(keyword: any, limit: any = 10, filters: list[any | None] | None = None):
    print(f"Search keyword: {keyword}")
    print(f"Result limit: {limit}")
    if filters:
        print(f"Filter conditions: {filters}")
    
    # Write your search logic here
    # results = search_users(keyword, limit, filters)
    # for user in results:
    #     print(user)
```

**Step 4: Run the Test**

```bash
python slim.py user search python
# Search keyword: python
# Result limit: 10

python slim.py user search python 5 '{"role":"admin"}' '{"active":true}'
# Search keyword: python
# Result limit: 5
# Filter conditions: [{'role': 'admin'}, {'active': True}]
```

Done. The entire process takes less than five minutes. Whenever you want to add a new command, just repeat this workflow.

## Documentation

Detailed documentation is in the `docs/` directory:

```
docs/
├─ English/
│  ├─ Admin mode.md      # Admin mode: how to manage command files
│  ├─ API.md             # API documentation: all APIs provided by the framework
│  ├─ config.md          # Configuration syntax: complete explanation of parameter formats
│  ├─ Global config.md   # Global settings: setting.json configuration items
│  └─ Tools.md           # Tool usage: built-in tools (Tran, to_type, etc.)
└─ 中文/
   ├─ 全局设置.md
   ├─ 工具.md
   ├─ 接口.md
   ├─ 操作员模式.md
   └─ 配置.md
```

It's recommended to start with `config.md` (configuration syntax) to understand how to define parameters, then read `Admin mode.md` to learn how to use `--admin create` to manage commands. When you need deeper extensions, check out `API.md` and `Tools.md`.