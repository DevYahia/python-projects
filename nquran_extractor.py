from PIL import Image
import urllib.request
import base64

for i in range(1, 605):
    images_parts = []
    for j in range(3):
        link = f's:29:"warshqasr/quranpic2/{i}.jpg:{j}";|_*7H_'
        if i < 10:
            link = f's:29:"warshqasr/quranpic2/00{i}.jpg:{j}";|_*7H_'
        elif i < 100:
            link = f's:29:"warshqasr/quranpic2/0{i}.jpg:{j}";|_*7H_'
        link_bytes = link.encode('ascii')
        base64_bytes = base64.b64encode(link_bytes)
        base64_link = base64_bytes.decode('ascii')
        full_link = f"https://www.nquran.com/globals/loadimage.php?img={base64_link}"
        urllib.request.urlretrieve(full_link, f'image{j}.png')
        images_parts.append(Image.open(f'image{j}.png'))
    widths, heights = zip(*(i.size for i in images_parts))
    total_height = sum(heights)
    max_width = max(widths)

    new_image = Image.new('RGB', (max_width, total_height))

    y_offset = 0
    for im in images_parts:
        new_image.paste(im, (0, y_offset))
        y_offset += im.size[1]

    if i < 10:
        new_image.save(f'D:/warsh/page00{i}.png')
    elif i < 100:
        new_image.save(f'D:/warsh/page0{i}.png')
    else:
        new_image.save(f'D:/warsh/page{i}.png')
