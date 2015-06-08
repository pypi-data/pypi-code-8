from fabric.colors import red, green, yellow

def error(message):
    print red(message)

def warning(message):
    print yellow(message)

def info(message):
    print green(message)

# EOF
