from enum import Enum

# TODO replace this whole mess with database intergration

class Status(Enum):
    Offline = 1
    Online = 2
    Idle = 3

class User:
    id: int
    name: str
    password: str
    display_name: str
    status: Status
    note: str
    friends: list[int]
    servers: list[int]

    def __init__(self, id: int, name: str, password: str, display_name: str, note: str, friends: list[int], servers: list[int]):
        self.id = id
        self.name = name
        self.password = password
        self.display_name = display_name
        self.note = note
        self.friends = friends
        self.servers = servers

        self.status = Status.Offline

    def json(self):
        return {
            "user_id": self.id,
            "username": self.name,
            "display_name": self.display_name,
            "status": self.status,
            "note": self.note
        }


class Message:
    id: int
    author_id: int
    content: str

    def __init__(self, id: int, author_id: int, content: str):
        self.id = id
        self.author_id = author_id
        self.content = content




class Channel:
    id: int
    name: str
    messages: list[Message]

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.messages = []


class Server:
    id: int
    name: str
    channels: list[Channel]
    members: list[int]
    id_owner: int

    def __init__(self, id: int, name: str, channels: list[Channel], members: list[int], id_owner: str):
        self.id = id
        self.name = name
        self.channels = channels
        self.id_owner = id_owner

        self.members = members


    def add_channel(self, name: str = ""):
        new_id = self.channels[-1].id + 1
        if name == "":
            if self.user[-1:] == 's': name = f"{self.user}' channel{new_id}"
            else:                     name = f"{self.user}'s channel{new_id}"
        self.channels.append(Channel(new_id, name))
        


users = [
    User(1, "name1", "password1", "displayname1", "note1", [2, 3], [1, 2]),
    User(2, "name2", "password2", "displayname2", "note2", [1, 3], [1, 2]),
    User(3, "name3", "password3", "displayname3", "note3", [2, 4], [1, 2]),
    User(4, "name4", "password4", "displayname4", "note4", [3], [1, 2]),
]


servers = [
    Server(1, "server1",
            [
                Channel(1, "channel1"),
                Channel(2, "channel2"),
            ],
           [1, 2, 3, 4],
           1
    ),
    Server(2, "server2",
           [
                Channel(3, "channel3"),
                Channel(4, "channel4")
           ],
           [1, 2, 3, 4],
           1
    ),
]
