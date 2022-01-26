

class SessionFactory:
    asession = None

    @staticmethod
    def get_async_session(self):
        if self.asession is None:
            self.asession = self.getNewAsession()
        return self.asession




