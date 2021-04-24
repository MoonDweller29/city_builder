# Entity class - all objects in game inherit from it
#
# Sample for new Entity child
# class Child(Entity):
# def __init__(self):
#     super().__init__()
#
# def Update(self):
#     super().Update()
#
# def Draw(self):
#     super().Draw()


class Entity:
    def __init__(self):
        self.drawOrder = 0

    def Draw(self):
        pass

    def Update(self):
        pass

class EntitySystem:
############################################################################
#                       Public interface
############################################################################

    def AddEntity(self, entity):
        id = self.__GetUnusedId()

        self.entities[id] = entity

        return id

    def GetEntity(self, id):
        # @TODO check for KeyError
        return self.entities[id]

    def DestroyEntity(self, id):
        self.entities_to_delete.append(id)

    def Update(self):
        self.__DeleteMarked()

        for entity in self.entities.values():
            entity.Update()

    def Draw(self):
        for entity in sorted(self.entities.values(), key=lambda e: e.drawOrder, reverse=True):
            entity.Draw()

############################################################################
#                       Private interface
############################################################################

    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(EntitySystem, cls).__new__(cls)
            cls.__instance.__init__singleton()
        return cls.__instance

    def __init__singleton(self):
        self.entities = {}
        self.entities_to_delete = []
        self.last_free_id = -1

    def __GetUnusedId(self):
        self.last_free_id += 1
        return self.last_free_id

    def __DeleteMarked(self):
        for id in self.entities_to_delete:
            del self.entities[id]
        self.entities_to_delete.clear()
