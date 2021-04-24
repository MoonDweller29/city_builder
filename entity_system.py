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
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(EntitySystem, cls).__new__(cls)
            cls.__instance.__init__singleton()
        return cls.__instance

    def __init__singleton(self):
        self.entities = {}
        
        self.last_free_id = -1

    def AddEntity(self, entity):
        id = self.__GetUnusedId()

        self.entities[id] = entity

        return id

    def GetEntity(self, id):
        return self.entities[id]

    def __GetUnusedId(self):
        self.last_free_id += 1

        return self.last_free_id

    def Update(self):
        for entity in self.entities.values():
            entity.Update()

    def Draw(self):
        for entity in sorted(self.entities.values(), key=lambda e: e.drawOrder, reverse=True):
            entity.Draw()
