import os
import pathlib
import stat
import time


class Tran:
    def __init__(self, translateMap: dict, lang: str):
        self.map: dict
        self.lang: str

    def run(self, key: str, content: str = "<?>") -> str: ...


tran: Tran
TRANMAP = {
    "zh-cn": {
        "is_file": "文件?               ",
        "size": "大小                ",
        "last_modify": "最后修改时间        ",
        "last_visit": "最后访问时间        ",
        "create_or_change": "创建/变更时间       ",
        "mode": "模式                ",
    },
    "en-us": {
        "is_file": "Is file?            ",
        "size": "Size                ",
        "last_modify": "Last modify time    ",
        "last_visit": "Last visit time     ",
        "create_or_change": "Create/Change time  ",
        "mode": "mode                ",
    },
}


def config(lang: str, tools: dict, **args):
    global tran
    tran = tools["Tran"](TRANMAP, lang)


def enter(path: str | None):
    if path is None:
        for file in os.listdir():
            p = pathlib.Path(os.path.abspath(file))
            print(
                f"{file + ('' if p.is_file() else '/')}{(len(max(os.listdir())) - len(file + ('' if p.is_file() else '/'))) * ' '}\t{p.stat().st_size if p.is_file() else '<DIR>'}"
            )
    elif pathlib.Path(path).exists():

        def calcSize(size: int, level: int):
            units = ["B", "KB", "MB", "GB", "TB", "PB"]
            if level < len(units) - 1 and size < 1024:
                return f"{size} {units[level]}"
            return calcSize(size // 1024, level + 1)

        p = pathlib.Path(path)
        print(
            f"""
{p.resolve()}
{tran.run("is_file")}{p.is_file()}
{tran.run("size")}{calcSize(p.stat().st_size, 0) if p.is_file() else "<DIR>"}
{tran.run("last_modify")}{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(p.stat().st_mtime))}
{tran.run("last_visit")}{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(p.stat().st_atime))}
{tran.run("create_or_change")}{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(p.stat().st_ctime))}
{tran.run("mode")}{stat.filemode(p.stat().st_mode)}
"""
        )
