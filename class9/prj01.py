# 認識裝飾詞的用法


# 定義函數
def say_hello():
    print("Hello!")


# 定義一個可以接收函數當參數的函數
def run_with_announce(func):
    print("準備執行...")
    func()
    print("執行完成!")


print("直接呼叫:")
say_hello()

print()
print("透過 run_with_announce 呼叫:")


def gift_wrap(func):
    def wrapper():
        print("-----前置動作-----")
        func()
        print("-----後置動作-----")

    return wrapper


say_hello = gift_wrap(say_hello)

say_hello()

print("-----------------")


# 第3段:@語法  @bot.event

# 函式定義+@


@gift_wrap
def say_hello():
    print("Hello!")


say_hello()

print("-----------------")


def register_command(name, description):  # 外層函數
    print(f"[登記]指令 /{name}: {description}")

    def decorator(func):  # 中層函數
        def wrapper():  # 內層函數
            print(f"[執行]指令 /{name}")
            func()  # 呼叫外層函數

        return wrapper

    return decorator  # 回傳中層函數


@register_command(name="hello", description="回傳內容")
def hello_command():
    print("Hello, 你好")


hello_command()
print("-----------------")
