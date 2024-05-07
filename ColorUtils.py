# feel free to use this 🙂.

def hex_to_hsv(hex_color : str) -> int:
    """
    Parameters:
        hex color - ex: "#00ff00"
    
    Return:
        h - [0-1]
        s - [0-1]
        v - [0-1]
    """
    r = int(hex_color[1:3], 16) / 255.0
    g = int(hex_color[3:5], 16) / 255.0
    b = int(hex_color[5:7], 16) / 255.0

    min_val = min(r, g, b)
    max_val = max(r, g, b)
    diff = max_val - min_val

    if max_val == min_val:
        h = 0
    elif max_val == r:
        h = (60 * ((g - b) / diff) + 360) % 360
    elif max_val == g:
        h = (60 * ((b - r) / diff) + 120) % 360
    elif max_val == b:
        h = (60 * ((r - g) / diff) + 240) % 360

    s = 0 if max_val == 0 else diff / max_val

    v = max_val

    h /= 360.0

    return h, s, v

def hsv_to_hsl(h : float, s : float, v : float) -> tuple[float]:
    """
    Parameters:
        h - [0-1]
        s - [0-1]
        v - [0-1]

    Return:
        h - [0-1]
        s - [0-1]
        l - [0-1]
    """
    l = (2 - s) * v / 2
    if l != 0:
        if l == 1:
            s = 0
        elif l < 0.5:
            s = s * v / (l * 2)
        else:
            s = s * v / (2 - l * 2)
    return (h, s, l)

def hsv_to_rgb(h : float, s : float, v : float) -> tuple[int]:
    """
    Parameters:
        h - [0-1]
        s - [0-1]
        v - [0-1]

    Return:
        r - [0-255]
        g - [0-255]
        b - [0-255]
    """
    if s == 0.0: v*=255; return (v, v, v)
    i = int(h*6.)
    f = (h*6.)-i; p,q,t = int(255*(v*(1.-s))), int(255*(v*(1.-s*f))), int(255*(v*(1.-s*(1.-f)))); v*=255; i%=6
    v = int(v)
    if i == 0: return (v, t, p)
    if i == 1: return (q, v, p)
    if i == 2: return (p, v, t)
    if i == 3: return (p, q, v)
    if i == 4: return (t, p, v)
    if i == 5: return (v, p, q)

def rgb_to_hex(r : int, g : int, b : int) -> str:
    """
    Parameters:
        r - [0-255]
        g - [0-255]
        b - [0-255]

    Return:
        hex color - ex: "#00ff00"
    """
    return f'#{int(r):02x}{int(g):02x}{int(b):02x}'

def hex_to_rgb(hex : str) -> tuple[int]:
    """
    Parameters:
        hex color - ex: "#00ff00"

    Return:
        luminance - (r, g, b)
    """
    return (int(hex[1:3], 16),int(hex[3:5], 16),int(hex[5:7], 16))

def get_color_luminance(r : int, g : int, b : int) -> float: 
    """
    Parameters:
        r - [0-255]
        g - [0-255]
        b - [0-255]

    Return:
        luminance - [0-1]

    Algorithm is based on the "Relative luminance" formula.
    https://en.wikipedia.org/wiki/Relative_luminance
    """
    return (0.299 * r + 0.587 * g + 0.114 * b) / 255

def optimal_hex_for_readability(r, g, b) -> str:
    """
    Determines the optimal text color for readability based on a given background color.

    Parameters:
        r - [0-255]
        g - [0-255]
        b - [0-255]

    Returns:
        str: A string representing a color in hexadecimal format. 
             Returns "#000000" (black) if the background color is light, 
             and "#ffffff" (white) if the background color is dark. 

    This function can be used to dynamically adjust text color based on the 
    perceived luminance of the background color, improving the readability of the text.
    """
    return "#000000" if get_color_luminance(r, g, b) > 0.5 else "#ffffff"

def generate_monochromatic_colors(hex_color : str) -> list[str]:
    """
    A function that generates a list of monochromatic colors based on the input color.

    Parameters:
        hex_color (str): A string representing a color in hexadecimal format. 
                         For example: "#00ff00" for green.

    Returns:
        list[str]: A list of six strings, each representing a color in hexadecimal format. 
                   These colors are variations of the input color at different brightness levels.
    """
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)

    colors = []
    for i in range(1, 7):
        factor = i / 6.0
        new_r = int(r * factor)
        new_g = int(g * factor)
        new_b = int(b * factor)
        new_hex_color = '#{:02x}{:02x}{:02x}'.format(new_r, new_g, new_b)
        colors.append(new_hex_color)

    return colors