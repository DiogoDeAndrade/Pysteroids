"""Color helper class and functions"""

class Color:
    """Color class. 

    It stores RGBA values as floats, in a range from 0 to 1."""
    def __init__(self, r, g, b, a):
        """Creates a new color
        
        Arguments:
            r {float} -- Red component, [0..1]

            g {float} -- Green component, [0..1]

            b {float} -- Blue component, [0..1]

            a {float} -- Alpha component, [0..1]
        """
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def tuple(self):
        """Returns a tuple version of the color value, for use with Pygame.

        For example, tuple(Color(0, 0.5, 1.0, 1)) = (0, 127, 255, 255)
        """
        return (self.r * 255, self.g * 255, self.b * 255, self.a * 255)

    @staticmethod
    def from_tuple(t):
        """Creates a new color from a tuple.

        For example, Color.from_tuple((0, 127, 255, 255) == Color(0, 0.5, 1.0, 1)
        """
        return Color(t[0] / 255.0, t[1] / 255.0, t[2] / 255.0, t[3] / 255.0)

    @staticmethod
    def interpolate_with_array(colors, t):
        """Returns a color given an array that stores a gradient, for a specific parametric t.
        
        Arguments:
            colors {Color[]} -- Array that stores the gradient. The array assumes the elements are evenly spaced in parametric space.

            t {float} -- Parametric t that describes how far in the gradient to sample. If t = 0, returns first element of the gradient array, if t = 1, returns the last element of the gradient array. Anything in between gets interpolated.
        
        Returns:
            Color -- Sampled color, interpolated if necessary.
        """
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
        """Interpolates between the given colors.
        
        Arguments:
            c1 {Color} -- Start color
            c2 {Color} -- End color
            t {float} -- Parametric t. if t = 0, returns c1, if t = 1, returns c2, anything in between is interpolated.
        
        Returns:
            Color -- Interpolated color.
        """
        return Color((1-t) * c1.r + t * c2.r,
                     (1-t) * c1.g + t * c2.g,
                     (1-t) * c1.b + t * c2.b,
                     (1-t) * c1.a + t * c2.a)
