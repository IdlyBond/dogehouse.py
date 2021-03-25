from dogehouse import DogeClient, event
import tokens
from dogehouse.entities import User, Message, BaseUser
import shelve
import time
from math import ceil



class Client(DogeClient):
    @event
    async def on_ready(self):
        print(f"Successfully connected as {self.user}!")
        await self.create_room("PyDogecoonBotTest!")
        await self.get_top_public_rooms()

    @event
    async def on_user_join(self, user: User):
        print(f"Welcome {user.mention}")
        await self.send(
            f"Welcome {user.mention}. I am dogecoon_py created with dogehouse_py. Type !woof to see comands",
            whisper=[user.id])
        print(self.room)

    @event
    async def on_message(self, message: Message):
        print(message.author.username + ": " + message.content)
        if message.content.startswith("!woof"):
            await self.send(
                f"Hi {message.author.mention}:DogeCool:. Use !doge to get one or !stats to see your doges!")
        elif message.content.startswith("!doge"):
            user = get_user_or_none(message.author.id)
            if user is None:
                await self.send("You got +1 Doge!  :DogeCool:   :DogeCool: ")
                add_doge(message.author)
            elif time.time() < (user.time + 5*60):
                await self.send(f"Wait {abs(int(ceil(time.time() - (user.time + 5*60))/60))} minutes for another Doge :Doge3D: ! \nVery time. Much long")
            else:
                await self.send("You got +1 Doge!  :DogeCool:   :DogeCool: ")
                add_doge(message.author)
        elif message.content.startswith("!stats"):
            user = get_user_or_none(message.author.id)
            if user is None:
                await self.send("Yet you have no Doges(\n But you can grab one with !doge :Doge3D: ")
            else:
                await self.send(f"You have a total of {user.doge_count} Doges!\n So wow. Mush doge")
        elif message.content.startswith("!55333"):
            await self.join_room(self.rooms[0].id)


class UserInfo:
    def __init__(self, user_id: str, doge_count: int = 0, time: float = 0):
        self.user_id = user_id
        self.doge_count = doge_count
        self.time = time


def get_user_or_none(user_id: str):
    shelf = shelve.open('user_data')
    try:
        item = shelf[user_id]
        shelf.close()
        return item
    except KeyError:
        return None


def update_user(user: UserInfo):
    shelf = shelve.open('user_data')
    shelf[user.user_id] = user
    shelf.close()


def add_doge(user: BaseUser):
    user_info = get_user_or_none(user.id)
    if user_info is None:
        update_user(UserInfo(user.id, 1, time.time()))
    else:
        update_user(UserInfo(user.id, int(user_info.doge_count) + 1, time.time()))


if __name__ == "__main__":
    Client(token=tokens.token, refresh_token=tokens.refresh_token).run()
