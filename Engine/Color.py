
class Color:
    def __init__(self, r, g, b, a):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def tuple(self):
        return (self.r * 255, self.g * 255, self.b * 255, self.a * 255)

    @staticmethod
    def from_tuple(t):
        return Color(t[0] / 255.0, t[1] / 255.0, t[2] / 255.0, t[3] / 255.0)

    @staticmethod
    def interpolate_with_array(colors, t):
        l = len(colors)
        range = 1.0 / l
        idx1 = (int)(t / range)
        if (idx1 >= l):
            idx1 = l - 1
        idx2 = idx1 + 1
        if (idx2 >= l):
            idx2 = l - 1

        if (idx1 == idx2):
            return colors[idx1]

        c1 = colors[idx1]
        c2 = colors[idx2]

        tt = (t - (idx1 * range)) / ((idx2 * range) - (idx1 * range))

        return Color.interpolate(c1, c2, tt)

    @staticmethod
    def interpolate(c1, c2, t):
        return Color((1-t) * c1.r + t * c2.r,
                     (1-t) * c1.g + t * c2.g,
                     (1-t) * c1.b + t * c2.b,
                     (1-t) * c1.a + t * c2.a)
