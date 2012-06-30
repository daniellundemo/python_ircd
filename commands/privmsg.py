from commands.base import Command
from models.actor import Actor
from models.actorcollection import ActorCollection
from models.channel import Channel
from models.user import User
from numeric_responses import *
from message import Message as M


class PrivmsgCommand(Command):
    required_parameter_count = 0
    command = 'PRIVMSG'

    def from_user(self, receivers=None, text=None):
        if receivers is None:
            return ERR_NORECIPIENT(self.command, self.actor)
        if text is None:
            return ERR_NOTEXTTOSEND(self.actor)
        resp = []
        # TODO: check for ERR_TOOMANYTARGETS
        for receiver in receivers.split(','):
            if Channel.exists(receiver):
                users = [user
                         for user in Channel.get(receiver).users
                         if user is not self.user]
                resp.append(M(
                    ActorCollection(users),
                    self.command, receiver, text,
                    prefix=self.user))
            elif User.exists(receiver):
                resp.append(M(
                    Actor.by_user(User.get(receiver)),
                    User.get(receiver),
                    self.user.nickname, self.command, receiver, text))
            # TODO: Implement wildcards
            # TODO: check for ERR_WILDTOPLEVEL, RPL_AWAY, ERR_NOTOPLEVEL
            else:
                resp.append(ERR_NOSUCHNICK(receiver, self.actor))
        return resp
