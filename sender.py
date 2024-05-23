async def get_receiver():
    with open("users.txt", "r") as file:
        for line in file:
            info = line.rstrip().split()
            yield int(info[0]), info[1]
