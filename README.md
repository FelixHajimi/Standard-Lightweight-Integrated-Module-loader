# SLIM

> **S**tandard **L**ightweight **I**ntegrated **M**odule-loader

## What the Project Does

SLIM is a command-line framework that allows you to define CLI commands by writing ordinary Python functions, with the framework automatically handling tedious tasks such as argument parsing, type conversion, and command routing.

You only need to focus on business logic—leave the rest to SLIM.

## When to Use

- When you need to quickly build CLI tools
- When you want to modularly manage multiple commands
- When you don't want to write repetitive code for argparse or click
- When you need to support nested multi-level commands (e.g., `user add`, `user delete`, `user list`)

## Advantages and Disadvantages

**Advantages:**
- Define commands using function signatures—intuitive and simple
- Automatic argument parsing and type conversion
- Supports regex validation, array parameters, and default values
- Lightweight with no dependencies

**Disadvantages:**
- Not suitable for GUI applications
- Complex business logic still requires manual implementation
- Regex expressions need double escaping in JSON

## How to Add New Features

1. Define the command and parameter format in `command.json`
2. Run `python slim.py --admin create` to generate the code file
3. Implement the `enter` function in the generated command file
4. Test by running `python slim.py your-command arguments`

## Documentation

```
docs/
├─ English/
│  ├─ Admin mode.md      # Admin mode instructions
│  ├─ API.md             # API interface documentation
│  ├─ config.md          # Command configuration syntax
│  ├─ Global config.md   # Global configuration instructions
│  └─ Tools.md           # Built-in tool usage
└─ 中文/
   ├─ 全局设置.md
   ├─ 工具.md
   ├─ 接口.md
   ├─ 操作员模式.md
   └─ 配置.md
```