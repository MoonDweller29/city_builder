# Entity class - all objects in game inherit from it
#
# Sample for new Entity child
# class Child(Entity):
# def __init__(self):
#     super().__init__()

# def update(self):
#     super().update()

# def draw(self):
#     super().draw()


class Entity:
    def __init__(self):
        self.drawOrder = 0

    def draw(self):
        pass

    def update(self):
        pass

class EntitySystem:
############################################################################
#                       Public interface
############################################################################

    def add_entity(self, entity):
        id = self.__get_unused_id()

        self.entities[id] = entity

        return id

    def get_entity(self, id):
        # @TODO check for KeyError
        return self.entities[id]

    def destroy_entity(self, id):
        self.entitiesToDelete.append(id)

    def update(self):
        self.__delete_marked()

        for entity in self.entities.values():
            entity.update()

    def draw(self):
        for entity in sorted(self.entities.values(), key=lambda e: e.drawOrder, reverse=True):
            entity.draw()

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
        self.entitiesToDelete = []
        self.lastFreeId = -1

    def __get_unused_id(self):
        self.lastFreeId += 1
        return self.lastFreeId

    def __delete_marked(self):
        for id in self.entitiesToDelete:
            del self.entities[id]
        self.entitiesToDelete.clear()
