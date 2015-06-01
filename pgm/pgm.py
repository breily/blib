import re
import matrix

# RE to match comment lines (occuring at beginning of line)
COMMENT = re.compile('^#.*')
# RE to match format (P2 = ASCII PGM, P5 = binary PGM)
FORMAT = re.compile('^P[1-6]$')
# RE to match width (first) and height (second)
DIMENSIONS = re.compile('^(?P<w>[0-9]{1,3}) (?P<h>[0-9]{1,3})$')
# RE to match an int expressing number of gray levels
GRAYLEVELS = re.compile('^[0-9]{1,3}$')

class PGM:
    def __init__(self, filename=None):
        self.format = None
        self.width = -1
        self.height = -1
        self.gray_levels = -1
        self.data = ''
        self.filename = filename

        self.lines = []

        if self.filename is not None:
            self.load(self.filename)
        else:
            print 'debug: no PGM file specified'
            self.filename = None

    def __repr__(self):
        return '<PGM: %s>' % (self.filename)

    def load(self, filename):
        fp = open(filename, 'rb')
        for line in fp.readlines():
            self.lines.append(line)
            m = DIMENSIONS.match(line.strip())
            if m:
                self.width = int(m.group('w'))
                self.height = int(m.group('h'))
            #elif COMMENT.match(line): continue
            elif FORMAT.match(line.strip()): self.format = line.strip()
            elif GRAYLEVELS.match(line.strip()): self.gray_levels = int(line.strip())
            else:
                self.data += line
    
        if len(self.data.split()) != self.width * self.height:
            if self.format == 'P2':
                print 'error: P2 image data does not match dimensions')
        if len(self.data) != self.width * self.height:
            if self.format == 'P5':
                print 'error: P5 image data does not match dimensions')

        self.filename = filename
        self.build_data()

    def build_data(self):
        self.image = matrix.zerosm(self.width, self.height)
        self.imaged = matrix.zerosm(self.width, self.height)
        if self.format == 'P5':
            i = 0
            for r in xrange(self.height):
                for c in xrange(self.width):
                    self.image[r][c] = ord(self.data[i])
                    self.imaged[r][c] = ord(self.data[i]) / float(self.gray_levels)
                    i += 1
        elif self.format == 'P2':
            print 'error: P2 images not currently supported')

    def write(self, filename):
        fp = open(filename, 'wb')
        fp.write('%s\n'    % self.format)
        fp.write('%s %s\n' % (self.width, self.height))
        fp.write('%s\n'    % self.gray_levels)
        fp.write(bytearray(matrix.flat(self.image)))
        fp.write('\n')
        fp.close()

