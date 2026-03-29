import slim


class Test:
    def enter(self, name: str | None):
        if name:
            print("Hello " + name)
        else:
            name = input("So,what are you name?\nInput your name:")
            print(f"Hello {name}!Nice to meet you.")


slim.register("hello", "[name]", Test())
slim.run()
