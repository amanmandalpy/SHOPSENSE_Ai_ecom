import struct
import zlib

# Generate a proper 16x16 ShopSense AI favicon (ICO format with blue gradient color)
# We'll create a proper ICO with a 16x16 32-bit BGRA image

def create_favicon():
    width = height = 16
    
    # Create pixel data: draw a simple "S" shape on dark blue bg
    pixels = []
    for y in range(height):
        for x in range(width):
            # Background: deep blue #1e40af
            r, g, b, a = 30, 64, 175, 255
            
            # Center area for letter
            cx, cy = x - 8, y - 8
            
            # Draw rounded rectangle background gradient
            # Top rounded arc (part of S)
            if 3 <= x <= 12 and 2 <= y <= 7:
                if y <= 4 and (x < 5 or x > 10):
                    pass  # keep bg color at corners
                else:
                    r, g, b = 59, 130, 246  # bright blue accent

            # Bottom rounded arc (part of S) 
            if 3 <= x <= 12 and 8 <= y <= 13:
                if y >= 11 and (x < 5 or x > 10):
                    pass
                else:
                    r, g, b = 99, 102, 241  # indigo accent

            # Middle bar of S
            if 5 <= x <= 10 and 7 <= y <= 8:
                r, g, b = 139, 92, 246  # purple

            # White sparkle dots (like stars) for AI
            if (x == 13 and y == 2) or (x == 14 and y == 4) or (x == 12 and y == 1):
                r, g, b, a = 255, 255, 255, 200

            pixels.append((b, g, r, a))  # ICO uses BGRA order

    # Build ICO file
    # ICO Header: 6 bytes
    ico_header = struct.pack('<HHH', 0, 1, 1)  # reserved=0, type=1 (ICO), count=1

    # Image data offset = 6 (header) + 16 (dir entry)
    img_data_offset = 22

    # Build BITMAPINFOHEADER (40 bytes)
    bmp_header = struct.pack('<IiiHHIIiiII',
        40,         # biSize
        width,      # biWidth
        -height,    # biHeight (negative = top-down)
        1,          # biPlanes
        32,         # biBitCount
        0,          # biCompression (BI_RGB)
        width * height * 4,  # biSizeImage
        0, 0,       # biXPelsPerMeter, biYPelsPerMeter
        0, 0        # biClrUsed, biClrImportant
    )

    # Pixel data
    pixel_bytes = b''.join(struct.pack('BBBB', b, g, r, a) for (b, g, r, a) in pixels)

    img_data = bmp_header + pixel_bytes

    # ICONDIRENTRY (16 bytes)
    dir_entry = struct.pack('<BBBBHHII',
        width,          # bWidth
        height,         # bHeight
        0,              # bColorCount (0 for 32bpp)
        0,              # bReserved
        1,              # wPlanes
        32,             # wBitCount
        len(img_data),  # dwBytesInRes
        img_data_offset # dwImageOffset
    )

    ico_data = ico_header + dir_entry + img_data

    with open(r'd:\PYTHON_PROJECTS\SHOPSENSE_Ai_ecommerce\static\favicon.ico', 'wb') as f:
        f.write(ico_data)

    print(f"favicon.ico created: {len(ico_data)} bytes")

create_favicon()
