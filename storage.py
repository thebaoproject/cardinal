import json
import disnake


class Database:
    def __init__(self, file: str):
        self.dtb = []
        self.file = file
        self.refresh()

    def search(self, uid: int, username: str = None):
        """
        Searches for the specific user and id.
        If multiple user profiles were found, and the user id is not specified,
        returns a list of found entries

        :param username:
        :param uid:
        :return: Sucess, value
        """
        self.refresh()
        same_name = []
        for user in self.dtb:
            if user["name"] == username:
                same_name.append(user)

        if uid is not None:
            for entry in same_name:
                if entry["id"] == uid:
                    return True, entry
        else:
            return True, same_name

        if not same_name:
            return False, []

    def write(self):
        """
        Writes the whole supplied object.

        :return:
        """
        self.refresh()
        with open(self.file, "w") as dtbf:
            dtbf.write(json.dumps(self.dtb))

    def refresh(self):
        self.dtb = json.loads(self.file)


class Profile:
    def __init__(self, guild: disnake.Guild, uid: int, username: str = None):
        dtb = Database("dtb.json")
        success, r = dtb.search(uid, username)
        # Gets the user
        self.exist = success
        self.user = None
        data = None
        for usr in guild.members:
            if usr.name == r["name"] and uid == r["id"]:
                self.user = usr
                data = r
                break
        if data is not None:
            success = True
        else:
            success = False
        if success:
            self.description = data["description"]
            self.banned = data["punishments"]["banned"]
            self.ban_due = data["punishments"]["ban_due"]
            self.language = data["lang"]
            user = None
            for usr in guild.members:
                if usr.name == data["invite"]["id"] and usr.id == data["invite"]["id"]:
                    user = usr
                    break
            if user is None:
                self.inviter = None
            else:
                self.inviter = user
            self.invite_link = data["invite"]["link"]["content"]
            self.invite_creator = Profile(
                guild, data["invite"]["link"]["original"]["id"], data["invite"]["link"]["original"]["name"]
            )
        else:
            self.description = None
            self.banned = False
            self.ban_due = None
            self.inviter = None
            self.invite_link = None
            self.invite_creator = None
            self.language = None

    def commit(self):
        """
        Commits all of the current state to the database.
        """
        dtb = Database("dtb.json")
        for entry in dtb.dtb:
            if entry["name"] == self.user.name and entry["id"] == self.user.id:
                entry["description"] = self.description
                entry["punishments"]["banned"] = self.banned
                entry["punishments"]["ban_due"] = self.ban_due
                entry["name"] = self.user.name
                entry["id"] = self.user.id
                entry["invite"]["link"]["content"] = self.invite_link
                entry["invite"]["original"]["name"] = self.inviter.name
                entry["invite"]["original"]["id"] = self.inviter.id
        dtb.write()
