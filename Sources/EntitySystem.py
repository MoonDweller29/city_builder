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
        self.id = 0

    def on_start(self):
        pass

    def draw(self):
        pass

    def update(self):
        pass

    def on_destroy(self):
        pass

class EntitySystem:
############################################################################
#                       Public interface
############################################################################

    def get_grid(self):
        return self.get_entity(self.gridId)

    def add_entity(self, entity):
        id = self.__get_unused_id()

        #self.entitiesToStart.append(id)

        self.entities[id] = entity
        self.entities[id].id = id

        self.entities[id].on_start()

        return id

    def get_entity(self, id):
        # @TODO check for KeyError
        return self.entities[id]

    def destroy_entity(self, id):
        self.entitiesToDelete.append(id)

        self.get_entity(id).on_destroy()

    def update(self):
        self.__update_preprocess()

        # @TODO Check copy of dictionary - seems to be shady
        for entity in self.entities.copy().values():
            entity.update()

    def draw(self):
        for entity in sorted(self.entities.values(), key=lambda e: e.drawOrder):
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
        self.entitiesToStart = []
        self.lastFreeId = -1

    def __get_unused_id(self):
        self.lastFreeId += 1
        return self.lastFreeId

    def __update_preprocess(self):
        for id in self.entitiesToDelete:
            del self.entities[id]

        self.entitiesToDelete.clear()

        #for id in self.entitiesToStart:
        #    self.get_entity(self.entitiesToStart[id]).on_start()

        #self.entitiesToStart.clear()
