from PIL import Image

class CutMethod():
    def __init__(self, path):
        self.image = Image.open(path)
        self.image = self.image.convert('L')

    def test(self):
        threshold = 210
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        print(table)
        self.image = self.image.point(table, '1')
        self.img_array = self.image.load()
        width = self.image.size[0]
        height = self.image.size[1]
        # for i in range(0, 1000):
        for x in range(1, width - 1):
            for y in range(1, height - 1):
                count = 0
                if self.img_array[x, y] == self.img_array[x - 1, y + 1]:
                    count += 1
                if self.img_array[x, y] == self.img_array[x, y + 1]:
                    count += 1
                if self.img_array[x, y] == self.img_array[x + 1, y + 1]:
                    count += 1
                if self.img_array[x, y] == self.img_array[x - 1, y]:
                    count += 1
                if self.img_array[x, y] == self.img_array[x + 1, y]:
                    count += 1
                if self.img_array[x, y] == self.img_array[x - 1, y - 1]:
                    count += 1
                if self.img_array[x, y] == self.img_array[x, y - 1]:
                    count += 1
                if self.img_array[x, y] == self.img_array[x + 1, y - 1]:
                    count += 1
                if count <= 2 and count > 1:
                    self.img_array[x, y] = 1
        self.image.show()

CutMethod(r'C:\win-back\pic\_158763463368.jpeg').test()
