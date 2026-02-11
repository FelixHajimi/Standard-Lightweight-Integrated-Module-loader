import json
import sys
import logging
import importlib.util as pathImport

logging.basicConfig(
    filename="./last.log",
    format="[%(levelname)s](%(asctime)s)<%(pathname)s>\n%(message)s",
    level=logging.DEBUG,
    encoding="utf-8",
)

commandConfig: dict = json.load(open("./command.json", encoding="utf-8"))
args = sys.argv[1:]
commands = {
    key: f"./command/{"/".join(key.split("."))}.py"
    for key in commandConfig
}


def runFunc(func, config: str, argsStart: int):
    if config == "-":
        func()
    else:
        configSplit = config[2:].split(" ")
        data = {}
        for index, arg in enumerate(configSplit):
            try:
                if arg[0] == "<" and arg[-1] == ">":
                    data[arg[1:-1]] = args[index + 1 + argsStart]
                elif arg[0] == "[" and arg[-1] == "]":
                    if ":" in arg:
                        if len(args) - 1 >= index + 1 + argsStart:
                            data[arg[1:-1].split(":")[0]] = args[index + 1 + argsStart]
                        else:
                            data[arg[1:-1].split(":")[0]] = arg[1:-1].split(":")[1]
                    else:
                        data[arg[1:-1]] = (
                            args[index + 1 + argsStart]
                            if len(args) - 1 >= index + 1 + argsStart
                            else ""
                        )
            except IndexError as error:
                print(f"索引选取错误: {error}\n{config}")
                return
        func(**data)


commandConfig = {
    key: commandConfig[key]
    for key in sorted(commandConfig, key=lambda item: len(item), reverse=True)
}
for id, config in commandConfig.items():
    if id == ".".join(args[: len(id.split("."))]):
        spec = pathImport.spec_from_file_location("func", commands[id])
        func = pathImport.module_from_spec(spec)
        spec.loader.exec_module(func)
        runFunc(func.enter, config, len(args[: len(id.split("."))]) - 1)
        exit()
logging.error("未找到该命令")
print("ERROR: 未找到该命令")
