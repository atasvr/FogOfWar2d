
class GameObject(object):
    def __init__(self, name, active, x, y):
        self.name = name
        self.active = active
        self.x = x
        self.y = y
        self.render = None

    def BeginPlay(self):
        return None

    def Update(self):
        return None

    def Render(self):
        return None
    def Destroy(self):
        return None
