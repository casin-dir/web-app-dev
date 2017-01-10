# Итератор для удаления дубликатов
class Unique(object):
    def __init__(self, items, **kwargs):
        self.items = list(items)
        self.index = -1
        self.lst = []
        self.len = len(self.items)
        self.ignore_case = kwargs.get('ignore_case')

    def __next__(self):
        self.index += 1
        if self.index == self.len:
            raise StopIteration
        buffer = self.items[self.index]
        buf_str = str(buffer)
        if self.ignore_case:
            buf_str = buf_str.lower()
            while buf_str in self.lst:
                self.index += 1
                if self.index == self.len:
                    raise StopIteration
                buffer = self.items[self.index]
                buf_str = str(buffer).lower()
            self.lst.append(buf_str)
            return buffer
        else:
            while buffer in self.lst:
                self.index += 1
                if self.index == self.len:
                    raise StopIteration
                buffer = self.items[self.index]
            self.lst.append(buffer)
            return buffer

    def __iter__(self):
        return self
