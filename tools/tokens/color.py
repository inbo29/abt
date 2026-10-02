import math
def oklch_to_hex(L, C, h):
    a = C*math.cos(math.radians(h)); b = C*math.sin(math.radians(h))
    l_ = L + 0.3963377774*a + 0.2158037573*b
    m_ = L - 0.1055613458*a - 0.0638541728*b
    s_ = L - 0.0894841775*a - 1.2914855480*b
    l, m, s = l_**3, m_**3, s_**3
    r = 4.0767416621*l - 3.3077115913*m + 0.2309699292*s
    g = -1.2684380046*l + 2.6097574011*m - 0.3413193965*s
    bl = -0.0041960863*l - 0.7034186147*m + 1.7076147010*s
    def enc(x):
        x = max(0.0, min(1.0, x))
        return 12.92*x if x <= 0.0031308 else 1.055*x**(1/2.4) - 0.055
    return '#%02x%02x%02x' % tuple(round(enc(v)*255) for v in (r, g, bl))
def lum(hexc):
    hexc = hexc.lstrip('#')
    rgb = [int(hexc[i:i+2], 16)/255 for i in (0, 2, 4)]
    lin = [c/12.92 if c <= 0.04045 else ((c+0.055)/1.055)**2.4 for c in rgb]
    return 0.2126*lin[0] + 0.7152*lin[1] + 0.0722*lin[2]
def cr(a, b):
    la, lb = lum(a), lum(b)
    if la < lb: la, lb = lb, la
    return (la+0.05)/(lb+0.05)
