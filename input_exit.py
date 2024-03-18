from inputimeout import inputimeout, TimeoutOccurred

if __name__ == "__main__":
    try:
        c = inputimeout(prompt='hello\n', timeout=3)
    except TimeoutOccurred:
        c = 'timeout'
    print(c)