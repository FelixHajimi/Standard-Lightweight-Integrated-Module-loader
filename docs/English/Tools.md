# This article will explain the usage of all tools in the config function API

## Tran
`Tran` is an internationalization translation class used to obtain corresponding translation text based on the current language setting.

### Initialization
```python
tran = Tran(translate_map: dict, lang: str)
```
- **translate_map**: Multi-language dictionary with structure `{ "language code": { "key": "translated text" } }`
- **lang**: Current language code (e.g., `"zh-cn"`, `"en-us"`)

### Methods

#### `run(key: str, content: str = "<?>") -> str`
Gets the translation text for the specified key and replaces `"<?>"` in `content` with the translated content.

- **key**: Translation key name
- **content**: String containing the placeholder `"<?>"`, defaults to `"<?>"`

### Example
```python
TRAN = {
    "zh-cn": {
        "hello": "Hello",
        "welcome": "Welcome, <?>"
    },
    "en-us": {
        "hello": "Hello",
        "welcome": "Welcome, <?>"
    }
}

tran = Tran(TRAN, "zh-cn")
print(tran.run("hello"))            # Output: Hello
print(tran.run("welcome", "<?> user"))  # Output: Welcome, user
```

---

## config_parser
Parses a command configuration string and converts the parameter definitions into structured data.

### Function Signature
```python
def config_parser(config: str) -> list[dict]
```

### Parameters
- **config**: Configuration string, e.g., `<name(string)> [age:int]`

### Returns
Returns a list of dictionaries, each dictionary representing a parameter definition.

**Dictionary Field Descriptions:**
- **class**: Parameter type, `1` for required parameter `<...>`, `2` for optional parameter `[...]`
- **name**: Parameter name
- **regex**: Regular expression validation rule (optional)
- **length**: Array length (optional, `0` means capture all remaining parameters)
- **default**: Default value (only present when `class=2`)
- **type**: Parameter type (`string`, `int`, `float`, `bool`, `json`)

### Example
```python
config = "<name(string)> [age:int] [tags:0](json)"
result = config_parser(config)
# Returns:
# [
#   {"class": 1, "name": "name", "regex": None, "length": None, "type": "string"},
#   {"class": 2, "name": "age", "regex": None, "length": None, "default": None, "type": "int"},
#   {"class": 2, "name": "tags", "regex": None, "length": 0, "default": None, "type": "json"}
# ]
```

---

## to_type
Converts a string to a specified type, supporting type conversion and exception handling.

### Function Signature
```python
def to_type(text: str | None, type_: str | None) -> any | None
```

### Parameters
- **text**: String to convert
- **type_**: Target type (`string`, `int`, `float`, `bool`, `json`)

### Returns
The converted value, returns `None` if conversion fails or parameters are invalid.

### Example
```python
print(to_type("123", "int"))        # Output: 123
print(to_type("3.14", "float"))     # Output: 3.14
print(to_type("true", "bool"))      # Output: True
print(to_type('{"a":1}', "json"))   # Output: {'a': 1}
print(to_type("abc", "int"))        # Output: None
```

---

## run_func
Executes a command function, parses command line arguments according to the configuration, and calls the target function.

### Function Signature
```python
def run_func(enter, config: str, arg_start_index: int) -> None
```

### Parameters
- **enter**: Function to execute (typically the `enter` function of a command module)
- **config**: Command configuration string (format same as `config_parser`)
- **arg_start_index**: Parameter start index (starting position within `sys.argv`)

### Functionality
1. Parses `config` to generate parameter definitions
2. Extracts values from `args` based on parameter definitions
3. Performs type conversion and regex validation on values
4. Calls the `enter` function using `**kwargs`

### Example
Assuming command configuration `"<name> [age:int]"` and `args = ["John", "25"]`, after execution it is equivalent to calling:
```python
enter(name="John", age=25)
```

---

## AdminCommands
Admin command class that provides help information viewing and command creation functionality.

### Initialization
```python
admin = AdminCommands(debug: bool = False)
```

### Methods

#### `help(id: str | None) -> None`
Displays command help information.

- **id**: Command ID, if `None` lists all commands

#### `create(id: str | None, config: str | None) -> None`
Creates a new command file or updates command configuration.

- **id**: Command ID (e.g., `"user.add"`)
- **config**: Command configuration string (e.g., `"<name> [age:int]"`)
- When both `id` and `config` are `None`, generates command files based on existing configuration

### Example
```python
admin = AdminCommands(debug=True)

# Display help for all commands
admin.help(None)

# Display help for a specific command
admin.help("user.add")

# Create or update a command
admin.create("user.add", "<name> [age:int]")
```

---

## run_admin_func
Entry function for running admin commands.

### Function Signature
```python
def run_admin_func(admin_args: list[str]) -> None
```

### Parameters
- **admin_args**: List of admin command arguments (excluding `--admin`)

### Functionality
1. Initializes an `AdminCommands` instance
2. Matches the admin command (e.g., `help`, `create`)
3. Calls the corresponding admin command function
4. If the command does not exist, reports an error and exits

### Example
Assuming command line input:
```bash
python main.py --admin help user.add
```
At this point `admin_args = ["help", "user.add"]`, `run_admin_func` will call `admin.help("user.add")`.