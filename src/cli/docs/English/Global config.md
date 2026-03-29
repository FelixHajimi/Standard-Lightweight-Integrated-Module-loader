# This article will explain how to configure `setting.json`
> Why is `setting.json` necessary?  
> `setting.json` stores all global settings, and the program will not run without it
## Example
```json
{
  "language": "en-us",
  "command_config": "command.json",
  "command_dir": "command",
  "debug": false,
  "other": {...}
}
```

- language is the global language, such as en-us, indicating that all commands uniformly use English for output/logging
- command_config is the command configuration, command.json means that all command configurations are stored in the command.json file
- command_dir is the command calling folder, after reading command_config, files will be called within this folder
- debug is a debug switch, commands can use debug for debugging purposes
- other is for other settings, commands can call this key to retrieve settings