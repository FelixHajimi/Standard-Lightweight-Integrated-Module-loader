def enter(path: str, encoding: str):
    print(open(path, encoding=encoding).read())
