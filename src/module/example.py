import slim


class Test:
    def enter(self, name: str):
        print("Hello " + str(name))


slim.register("hello", "[name=Felix]", Test())
slim.run()
