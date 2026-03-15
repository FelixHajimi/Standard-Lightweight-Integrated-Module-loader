# SLIM
> **S**tandard **L**ightweight **I**ntegrated **M**odule-loader

The original design intention of SLIM is only one: **to compress the "definition cost" of command-line tools to the limit**

- **Traditional process**: Create parser -> Add parameters one by one -> Set type/help/default value -> Write parsing logic -> Handle exceptions -> **Start writing business logic**
- **SLIM process**: Write one line of configuration string -> **Directly write business logic**

You don't need to learn complex APIs, don't need to initialize objects, as long as you can write a parameter string, your command is defined

```python
# Traditional way: dozens of lines of boilerplate
parser = argparse.ArgumentParser()
parser.add_argument('output', help='Output directory')
parser.add_argument('--verbose', action='store_true', help='Verbose mode')
parser.add_argument('files', nargs='+', help='Input files')
args = parser.parse_args()
# ... also need to handle type conversion and validation ...

# SLIM way: one line definition
# command.json
{ "script": "- <output> [verbose:true] @files" }

# Corresponding business function, parameters automatically injected
def enter(output: str, verbose: str, files: list[str]):
    # Directly start writing core logic, no preprocessing parsing code needed
    pass
```

## Syntax Overview

All complex parameter logic is condensed into a few simple symbols

Remember these symbols, and you can define any command

| Symbol | Example | Definition Effect |
| :---: | :--- | :--- |
| **`<required parameter>`** | `<file>` | Forces user input, reports an error if missing |
| **`[optional parameter]`** | `[debug]` | User can input or not, defaults to `None` if missing |
| **`(regular expression)`** | `<@file(.*\.(?:png\|jpg\|svg))>` | Regex validation |
| **`:length`** | `<@file:5>` | Specifies length |
| **`=default value`** | `[port=8080]` | Automatically fills with default value when user does not input |

**Must be written in the order `(regex):length=default value`**

---

## How to Use

After cloning the repository, you will get the core engine `slim.py`, and you can create a new command in just three steps

### Step 1: Global Settings

Create `setting.json` in your project directory and enter the following content
```json
{
  "language": "en-us",
  "commandConfig": "command.json",
  "commandDir": "command",
  "debug": false
}
```

### Step 2: Define Interface

Edit `command.json` and describe your command structure with one line string

```json
{
  "compress_images": "- <output_dir> [quality:80] @images(.*\\.(png|jpg))"
}
```
*That's it for definition, no need to write classes, function signatures, or parsing logic*

### Step 3: Implement Business Logic

Create a file with the same name `compress_images.py` in the `command` directory
SLIM will automatically read the configuration, parse parameters, and inject them into the `enter` function in order

```python
# command/compress_images.py

def enter(output_dir: str, quality: str, images: list[str]):
    # At this point, all parameters have been parsed and cleaned
    # output_dir: required string
    # quality: string, defaults to "80"
    # images: list, only contains files matching .png or .jpg
    
    valid_images = [img for img in images if img is not None]
    
    print(f"Task started: compressing {len(valid_images)} files to {output_dir}")
    print(f"Quality setting: {quality}")
    
    # Directly write core business code here
    # ...
```

### Run

Configure an alias for quick calling (optional):
```bash
function slim { python slim.py $@;}
```

Execute command:
```bash
slim compress_images ./dist 90 ./src/a.png ./src/b.txt ./src/c.jpg
```

**Parsing result:**
- `output_dir` = `"./dist"`
- `quality` = `"90"` (overrides default value)
- `images` = `["./src/a.png", None, "./src/c.jpg"]` (`b.txt` is automatically marked as `None` because it doesn't match the regex)

---

## Why SLIM Can Greatly Improve Efficiency?

1.  **Definition is Completion**: Once the parameter string is written, the interface definition is done, no intermediate steps
2.  **Clean Logic**: There is no parameter parsing, type conversion, or validation code in business functions, only pure business logic
3.  **Configuration Driven**: Modifying command behavior only requires changing the string in JSON, no need to touch Python code, suitable for rapid prototype iteration
4.  **Automatic Cleaning**: Using regex syntax completes data filtering at the definition stage, and the data received by the business layer is highly usable

## Specifications and Constraints

- **Filename matching**: Filenames in `command/*.py` must strictly match the key names in `command.json`
- **Parameter order**: The parameter order in the `enter` function must be exactly the same as the definition order in the configuration string