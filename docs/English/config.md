# This article will explain how to configure `command.json`

## command.json Configuration Guide

`command.json` is the command configuration file used to define the parameter formats and types for all available commands. This file is located in the `PATH` directory, with the specific path specified by the `command_config` field in `setting.json`.

### File Format

```json
{
    "Command ID": "Command configuration string",
    "Command ID.subcommand": "Command configuration string"
}
```

Command IDs use dots to indicate hierarchy, but are separated by spaces when used on the command line.

### Command Configuration String Syntax

Two parameter types are supported:
- Required parameter: `<parameter name(regex):length>type`
- Optional parameter: `[parameter name(regex):length=default value]type`

#### Parameter Descriptions
- **Parameter name**: Consists of letters, numbers, and underscores, must start with a letter or underscore
- **Regex** (optional): Wrapped in parentheses, requires double escaping in JSON
- **Length** (optional): `:number` for fixed-length array, `:0` for capturing all remaining parameters
- **Default value** (optional): Only available for optional parameters, format `=value`
- **Type** (optional): `string` (default), `int`, `float`, `bool`, `json`

### Examples

#### Basic Examples
```json
{
    "user": "<action>",
    "user.add": "<name> [age]int",
    "user.delete": "<user_id>int [force]bool",
    "user.list": "[page=1]int [size=20]int"
}
```

#### Regex Validation (Note double escaping)
```json
{
    "user.add": "<username(^[a-zA-Z][a-zA-Z0-9_]{3,15}$)> [email(^[\\w\\.-]+@[\\w\\.-]+\\.[\\w]+$)]",
    "user.date": "<date(^\\d{4}-\\d{2}-\\d{2}$)>",
    "user.phone": "<phone(^1[3-9]\\d{9}$)>"
}
```

#### Array Parameters
```json
{
    "user.batch": "<ids:3>int",
    "user.search": "<keyword> [tags:0]",
    "user.multi": "<values:0>float"
}
```

#### Complex Types
```json
{
    "data.import": "<config>json",
    "user.add": "<name> [roles:0]json [age=0]int"
}
```