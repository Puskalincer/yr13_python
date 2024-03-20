from inputimeout import inputimeout, TimeoutOccurred

if __name__ == "__main__":
    try:
        c = inputimeout(prompt='hello\n', timeout=10)
    except TimeoutOccurred:
        c = 'timeout'
    print(c)