import hexdump
from typing import Dict, Union

class Streaker():
    def __init__(self, data: str):
        self.data = data
        self.cursor_pos = 0
        self.max_size = len(data)
    def read(self, size: Union[str, int]):
        """
        size can either be datatype: byte, word, dword etc. or int as the number of bytes
        """     

        size = self.get_size(size)
        if self.max_size < size + self.cursor_pos:
            raise IndexError("Cursor reached end")

        value = self.data[self.cursor_pos : size + self.cursor_pos]
        self.cursor_pos += size
        return value
    
    def skip(self, size: Union[int, str]):
        size = self.get_size(size)
        if self.max_size<size+self.cursor_pos:
            raise IndexError("Cursor reached end")
        self.cursor_pos += size

    def get_size(self, size: Union[int, str]):
        match size:
            case "byte":
                size = 1
            case "word":
                size = 2
            case "dword" | "FXPT2DOT30":
                size = 4
            case "long":
                size = 8
            case "CIEXYZ":
                size = 12
            case "CIEXYZTRIPLE":
                size = 36
            case _:
                if isinstance(size, int):
                    print(f"SIZE = {size} WHY NOT INT?")
                size = size

        return size

    def sneak(self, size: Union[int, str], offset: Union[int, str] = 0):
        size = self.get_size(size)
        if offset:
            offset = self.get_size(offset)
        if self.max_size < size + self.cursor_pos + offset:
            raise IndexError("Cursor reached end")
        value = self.data[self.cursor_pos + offset : size + self.cursor_pos + offset]
        return value    

    def __len__(self):
        return len(self.data)

class struct_reader():
    def __init__(self, map: Dict[str, Union[str, int]], data: Streaker):
        """
        map is a dict of the form {"name": size, ...}
        """
        self.data = data
        for variable, size in map.items():
            value = self.data.read(size)
            setattr(self, variable, value)

    def __str__(self) -> str:
        string = ''
        for x in self.variables.items():
            string += str(x) + "\n"
        return string 


class BMP():
    def __init__(self, filename):
        self.filename = filename
        self.open_bmp()
        self.streaker = Streaker(self.data)
        self.header = BITMAPFILEHEADER(self.streaker)
    
    def open_bmp(self, show=True):
        with open(self.filename, "rb") as file:
            byte_data = file.read()
        gen = hexdump.hexdump(byte_data, result="generator")
        pretty = '\n'.join(gen)
        data = hexdump.dump(byte_data, size=0)
        if show:
            print(pretty)
        self.data = data
        self.pretty = pretty

class BITMAPFILEHEADER(struct_reader):
    def __init__(self, streaker):
        map = {"bfType":"word",
                "bfSize":"dword",
                "bfReserved1":"word",
                "bfReserved2":"word",
                "bfOffBits":"dword"}
        super().__init__(map, streaker)

class BITMAPCOREHEADER(struct_reader):
    def __init__(self, streaker):
        map = {
            'bcSize': 'dword', 
            'bcWidth': 'word', 
            'bcHeight': 'word', 
            'bcPlanes': 'word', 
            'bcBitCount': 'word'}
        super().__init__(map, streaker)

class BIPMAPINFOHEADER(struct_reader):
    def __init__(self, streaker):
        map = {
            'biSize': 'dword',
            'biSize': 'dword',
            'biWidth': 'long',
            'biHeight': 'long',
            'biPlanes': 'word',
            'biBitCount': 'word',
            'biCompression': 'dword',
            'biSizeImage': 'dword',
            'biXPelsPerMeter': 'long',
            'biYPelsPerMeter': 'long',
            'biClrUsed': 'dword',
            'biClrImportant': 'dword'
        }
        super().__init__(map, streaker)    


class BITMAPV4HEADER(struct_reader):
    def __init__(self, streaker):
        map = {
            'bV4Size': 'dword',
            'bV4Width': 'long',
            'bV4Height': 'long',
            'bV4Planes': 'word',
            'bV4BitCount': 'word',
            'bV4V4Compression': 'dword',
            'bV4SizeImage': 'dword',
            'bV4XPelsPerMeter': 'long',
            'bV4YPelsPerMeter': 'long',
            'bV4ClrUsed': 'dword',
            'bV4ClrImportant': 'dword',
            'bV4RedMask': 'dword',
            'bV4GreenMask': 'dword',
            'bV4BlueMask': 'dword',
            'bV4AlphaMask': 'dword',
            'bV4CSType': 'dword',
            'bV4Endpoints': 'ciexyztriple',
            'bV4GammaRed': 'dword',
            'bV4GammaGreen': 'dword',
            'bV4GammaBlue': 'dword'
        }
        super().__init__(map, streaker)  

class BITMAPV5HEADER(struct_reader):
    def __init__(self, streaker):
        map = {
            'bV5Size': 'dword',
            'bV5Width': 'long',
            'bV5Height': 'long',
            'bV5Planes': 'word',
            'bV5BitCount': 'word',
            'bV5Compression': 'dword',
            'bV5SizeImage': 'dword',
            'bV5XPelsPerMeter': 'long',
            'bV5YPelsPerMeter': 'long',
            'bV5ClrUsed': 'dword',
            'bV5ClrImportant': 'dword',
            'bV5RedMask': 'dword',
            'bV5GreenMask': 'dword',
            'bV5BlueMask': 'dword',
            'bV5AlphaMask': 'dword',
            'bV5CSType': 'dword',
            'bV5Endpoints': 'ciexyztriple',
            'bV5GammaRed': 'dword',
            'bV5GammaGreen': 'dword',
            'bV5GammaBlue': 'dword',
            'bV5Intent': 'dword',
            'bV5ProfileData': 'dword',
            'bV5ProfileSize': 'dword',
            'bV5Reserved': 'dword'
        }
        super().__init__(map, streaker)  



bmp = BMP("REDBRICK.BMP")