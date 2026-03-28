import importlib.util as pathImport
import json
import logging
import os
import pathlib
import re
import sys


def config_parser(config: str):
    args = config.split(" ")
    res = []
    for arg in args:
        match1 = re.fullmatch(
            r"<([a-zA-Z_][a-zA-Z_\d]*)?(\(.*\))?(:\d+)?>(string|int|float|bool|json)?",
            arg,
        )
        match2 = re.fullmatch(
            r"\[([a-zA-Z_][a-zA-Z_\d]*)?(\(.*\))?(:\d+)?(=.*)?\](string|int|float|bool|json)?",
            arg,
        )
        if match1:
            if not match1.group(1):
                logging.error(tran.run("fill_name", f"<?>{arg}"))
                print(
                    f"\x1b[41;37m{tran.run('fill_name', f'<?>{arg}')}\x1b[0m"
                )
            res.append(
                {
                    "class": 1,
                    "name": match1.group(1),
                    "regex": match1.group(2)[1:-1] if match1.group(2) else None,
                    "length": int(match1.group(3)[1:]) if match1.group(3) else None,
                    "type": match1.group(4) if match1.group(4) else "string",
                }
            )
        elif match2:
            if not match2.group(1):
                logging.error(tran.run("fill_name", f"<?>{arg}"))
                print(
                    f"\x1b[41;37m{tran.run('fill_name', f'<?>{arg}')}\x1b[0m"
                )
            res.append(
                {
                    "class": 2,
                    "name": match2.group(1),
                    "regex": match2.group(2)[1:-1] if match2.group(2) else None,
                    "length": int(match2.group(3)[1:]) if match2.group(3) else None,
                    "default": match2.group(4)[1:] if match2.group(4) else None,
                    "type": match2.group(5) if match2.group(5) else "string",
                }
            )
        else:
            logging.error(tran.run("not_match_format", f"<?>{arg}"))
            print(
                f"\x1b[41;37m{tran.run('not_match_format', f'<?>{arg}')}\x1b[0m"
            )
    return res


def to_type(text: str | None, type_: str | None):
    if text is None or type_ is None:
        return None
    mapping = {
        "string": str,
        "int": int,
        "float": float,
        "bool": bool,
        "json": json.loads,
    }
    for t, f in mapping.items():
        if type_ == t:
            if type_ == "json":
                text = text.replace("'", '"')
            try:
                return f(text)
            except Exception as error:
                logging.error(f"{tran.run('conversion_error')}{error}")
                return None


def run_func(enter, config: str, arg_start_index: int):
    if config == "":
        enter()
    else:
        data = {}
        parser = config_parser(config)
        for index, arg in enumerate(parser):
            arg_index = arg_start_index + index + 1
            arg_list: list
            try:
                if arg["class"] == 1:
                    if arg["length"] or arg["length"] == 0:
                        arg_list = (
                            args[arg_index:]
                            if arg["length"] == 0
                            else args[arg_index : 1 + arg["length"]]
                        )
                        for _ in range(arg["length"] - len(arg_list)):
                            arg_list.append(None)
                        for index, text in enumerate(arg_list):
                            value = None
                            if arg["regex"]:
                                value = to_type(
                                    text if re.fullmatch(arg["regex"], text) else None,
                                    arg["type"],
                                )
                            else:
                                value = to_type(text, arg["type"])
                            arg_list[index] = value
                        data[arg["name"]] = arg_list
                    else:
                        value = None
                        if arg["regex"]:
                            value = to_type(
                                args[arg_index]
                                if re.fullmatch(arg["regex"], args[arg_index])
                                else None,
                                arg["type"],
                            )
                        else:
                            value = to_type(args[arg_index], arg["type"])
                        data[arg["name"]] = value
                elif arg["class"] == 2:
                    if arg["length"] or arg["length"] == 0:
                        arg_list = (
                            args[arg_index:]
                            if arg["length"] == 0
                            else args[arg_index : 1 + arg["length"]]
                        )
                        for _ in range(arg["length"] - len(arg_list)):
                            arg_list.append(arg["default"])
                        for index, text in enumerate(arg_list):
                            value = None
                            if len(args) - 1 >= arg_index:
                                if arg["regex"]:
                                    value = to_type(
                                        text
                                        if re.fullmatch(arg["regex"], text)
                                        else arg["default"],
                                        arg["type"],
                                    )
                                else:
                                    value = to_type(text, arg["type"])
                            else:
                                value = to_type(arg["default"], arg["type"])
                            arg_list[index] = value
                        data[arg["name"]] = arg_list
                    else:
                        value = None
                        if len(args) - 1 >= arg_index:
                            if arg["regex"]:
                                value = to_type(
                                    args[arg_index]
                                    if re.fullmatch(arg["regex"], args[arg_index])
                                    else arg["default"],
                                    arg["type"],
                                )
                            else:
                                value = to_type(args[arg_index], arg["type"])
                        else:
                            value = to_type(arg["default"], arg["type"])
                        data[arg["name"]] = value
                else:
                    logging.error(f"{tran.run('not_found_format')}{arg['class']}")
                    print(f"{tran.run('not_found_format')}{arg['class']}")
            except Exception:
                logging.error(eval(tran.run("required_error")))
                print(
                    f"\x1b[41;37m{eval(tran.run('required_error'))}\x1b[0m"
                )
                return
        enter(**data)


class AdminCommands:
    def __init__(self, debug: bool = False):
        self.debug = debug

    def help(self, id: str | None):
        commands = json.load(open(f"{PATH}/command.json", encoding="utf-8"))
        if id is None:
            for id, config in commands.items():
                print(f"{id} : {config}")
        else:
            try:
                print(f"{id} : {commands[id]}")
            except KeyError:
                logging.error(f"{tran.run('not_found_command')}{id}")
                print(
                    f"\x1b[41;37m{tran.run('not_found_command')}{id}\x1b[0m"
                )

    def create(self, id: str | None, config: str | None):
        command_config = json.load(
            open(f"{PATH}/{SETTING['command_config']}", encoding="utf-8")
        )
        if id is None and config is None:
            for id, config in command_config.items():
                if id is None or config is None:
                    return
                path = f"{PATH}/{SETTING['command_dir']}/{'/'.join(id.split('.'))}.py"
                p = pathlib.Path(path)
                if not p.exists():
                    p.touch()
                    args_text = ""
                    for arg in config_parser(config):
                        args_text = (
                            f"{args_text}, {arg['name']}: {'list[any | None]' if arg['array'] else 'any'}"
                            if arg["type"] == 1
                            else (
                                f"{args_text}, {arg['name']}: {'list[any | None]' if arg['array'] else 'any | None'}"
                                if arg["type"] == 2
                                else f"{args_text}, ERROR"
                            )
                        )
                    open(path, "w", encoding="utf-8").write(
                        f"def config(**args):\n    pass\n\ndef enter({args_text[2:]}):\n    pass"
                    )
                    logging.info(tran.run("created_file", f"<?>{path}"))
                    print(tran.run("created_file", f"<?>{path}"))
        else:
            command_config[id] = "-" if config is None else config
            open(SETTING["command_config"], "w", encoding="utf-8").write(
                json.dumps(command_config, indent=2, ensure_ascii=False)
            )
            print(tran.run("created_file", f"<?>{SETTING['command_config']}"))
            self.create(None, None)


def run_admin_func(admin_args: list[str]):
    admin = AdminCommands(SETTING["debug"])
    admin_commands = {
        "help": ("- [id]", admin.help),
        "create": ("- [id] [config]", admin.create),
    }
    admin_commands = {
        key: admin_commands[key]
        for key in sorted(admin_commands, key=lambda item: len(item), reverse=True)
    }
    for command, config in admin_commands.items():
        if command == ".".join(admin_args[: len(command.split("."))]):
            logging.info(tran.run("running_admin_command", f"<?>:{args}"))
            run_func(config[1], config[0], len(command.split(".")))
            return
    logging.error(tran.run("not_found_command", f"<?>{args}"))
    print(
        f"\x1b[41;37m{tran.run('not_found_command', f'<?>{args}')}\x1b[0m"
    )


class Tran:
    def __init__(self, translate_map: dict, lang: str):
        self.map = translate_map
        self.lang = lang

    def run(self, key: str, content: str = "<?>"):
        if self.lang not in self.map:
            if "en-us" in self.map:
                language = "en-us"
            else:
                language = next(iter(self.map))
        else:
            language = self.lang
        return content.replace("<?>", self.map[language][key])


logging.basicConfig(
    filename="./last.log",
    format="[%(levelname)s](%(asctime)s)<%(pathname)s>\n%(message)s",
    level=logging.DEBUG,
    encoding="utf-8",
)


PATH = os.path.dirname(os.path.abspath(__file__))
TRAN = {
    "zh-cn": {
        "required_error": 'f"你有一个必填项未填写: 应该在第 {index} 个参数填写,参数名为 {arg["name"]}"',
        "not_found_command": "未找到该命令: ",
        "created_file": "已创建文件至: ",
        "fill_name": "请填写参数名: ",
        "not_match_format": "没有匹配此格式的参数: ",
        "not_found_commandFile": "检测到命令文件不存在,程序已退出",
        "running_command": "正在运行命令",
        "running_admin_command": "正在运行管理员命令",
        "not_found_format": "没有此格式: ",
        "conversion_error": "转换错误: ",
    },
    "en-us": {
        "required_error": 'f"You have a required parameter not filled: should be filled at position {index}, parameter name is {arg["name"]}"',
        "not_found_command": "Command not found: ",
        "created_file": "File created at: ",
        "fill_name": "Please fill in parameter name: ",
        "not_match_format": "No parameter matching this format: ",
        "not_found_commandFile": "Command file not detected, the program has exited",
        "running_command": "Running command",
        "running_admin_command": "Running admin command",
        "not_found_format": "This format does not exist: ",
        "conversion_error": "Conversion error: ",
    },
}
SETTING = json.load(open(f"{PATH}/setting.json", encoding="utf-8"))


command_config: dict = json.load(
    open(f"{PATH}/{SETTING['command_config']}", encoding="utf-8")
)
command_config = {
    key: command_config[key]
    for key in sorted(command_config, key=lambda id: len(id), reverse=True)
}
commands = {
    key: f"{PATH}/{SETTING['command_dir']}/{'/'.join(key.split('.'))}.py"
    for key in command_config
}
tran = Tran(TRAN, SETTING["language"])
args = sys.argv[1:]
if len(args) != 0 and args[0] == "--admin":
    run_admin_func(args[1:])
    quit()


config_args = {
    "path": PATH,
    "lang": SETTING["language"],
    "debug": SETTING["debug"],
    "other": SETTING["other"],
    "tools": {
        "Tran": Tran,
        "config_parser": config_parser,
        "run_func": run_func,
        "to_type": to_type,
        "AdminCommands": AdminCommands,
        "run_admin_func": run_admin_func,
    },
}


for id, config in command_config.items():
    if id == ".".join(args[: len(id.split("."))]):
        try:
            spec = pathImport.spec_from_file_location("func", commands[id])
            if not spec or not spec.loader:
                raise
            func = pathImport.module_from_spec(spec)
            spec.loader.exec_module(func)
        except Exception:
            logging.warning(tran.run("not_found_commandFile"))
            print(
                f"\x1b[43;37m{tran.run('not_found_commandFile')}\x1b[0m"
            )
            quit()
        if hasattr(func, "config"):
            getattr(func, "config")(**config_args)
        logging.info(tran.run("running_command", f"<?>:{args}"))
        run_func(func.enter, config, len(args[: len(id.split("."))]) - 1)
        quit()
logging.error(tran.run("not_found_command", f"<?>{args}"))
print(
    f"\x1b[41;37m{tran.run('not_found_command', f'<?>{args}')}\x1b[0m"
)
