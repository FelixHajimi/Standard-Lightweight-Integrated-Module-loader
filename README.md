# **S**tandard **L**ightweight **I**ntegrated **M**odule-loader

A lightweight command-line tool dispatching framework.  
Registers commands via configuration, auto-loads modules, and supports parameter injection.  
All commands are invoked uniformly—ready to use out of the box with **zero installation**.

## Usage

```sh
python slim.py <command> [arguments...]
```

**Examples:**

```sh
python slim.py fex notes.txt
python slim.py file add temp.txt
```

The program automatically loads the corresponding module from the `./command/` directory based on the command name and executes it.

## Command Development Specification

### Command Requirements

-   **Entry Point**: The main function must be named `enter` and accept named arguments (kwargs).
-   **Feedback**: All commands must return a user-readable feedback message (string).
-   **Location**: Command modules must be placed in the `./command/` directory. The filename (without `.py`) defines the command name.
-   **Logging**: Use the built-in `logging` module for runtime logs. The default log path is `./last.log`.

### Command Registration

Commands are registered and their signatures defined via `command.json`.

**Example Signature:**

```json
{
  "fex": "- <path> [encoding:utf-8] [plugin]"
}
```

**Syntax Guide:**
-   `-`: Represents the command itself.
-   `<*>`: **Required** argument (e.g., `<path>`).
-   `[*]`: **Optional** argument.
    -   Default values can be defined using `:` (e.g., `[encoding:utf-8]` defaults to `utf-8`).

The framework automatically parses command-line inputs and passes them as keyword arguments to the `enter` function.