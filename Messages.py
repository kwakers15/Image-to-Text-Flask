class Messages:
    def __init__(self, name, senderName, receiverName):
        self.conversationName = name.split("_")[0]
        self.senderName = senderName
        self.receiverName = receiverName
        self.messages = []

    def addMessage(self, message, sender):
        self.messages.append(
            Map(self.senderName if sender else self.receiverName, message)
        )

    def getDictRepresentation(self):
        result = {}
        result[self.conversationName] = []
        result[self.conversationName].append([self.senderName, self.receiverName])

        for i in range(len(self.messages)):
            message = self.messages[i]
            if message.getName() == self.senderName:
                result[self.conversationName].append([message.getMessage(), ""])
            else:
                result[self.conversationName].append(["", message.getMessage()])
        return result

    def printMessages(self):
        for message in self.messages:
            print(message.getName() + ": " + message.getMessage())


class Map:
    def __init__(self, name, message):
        self.name = name
        self.message = message

    def getName(self):
        return self.name

    def getMessage(self):
        return self.message
