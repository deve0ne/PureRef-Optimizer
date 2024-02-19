from PIL import Image
import io
from multiprocessing import Pool, freeze_support
from PureRef_format.purformat.read import read_pur_file
from PureRef_format.purformat.write import write_pur_file
from PureRef_format.purformat.purformat import PurFile


def compress_image(image_data, max_dimension):
    image = Image.open(io.BytesIO(image_data))
    info = image.info
    info.pop("exif", None)
    resized = False
    scale = 1
    new_width = new_height = 1

    # Рассчитываем новый размер изображения
    old_width, old_height = image.size
    
    max_current_dimension = max(old_width, old_height)

    # Проверяем, нужно ли изменять размер изображения
    if max_current_dimension > max_dimension:
        aspect_ratio = old_width / old_height
        if aspect_ratio == 1:  # Изображение квадратное
            new_width = new_height = max_dimension
        else:  # Изображение прямоугольное
            new_area = max_dimension * max_dimension
            new_width = int((new_area * aspect_ratio) ** 0.5)
            new_height = int((new_area / aspect_ratio) ** 0.5)

        # Изменяем размер изображения
        image = image.resize((new_width, new_height))
        scale = new_width / old_width
        resized = True

    # Конвертируем изображение в палитровый режим
    image = image.convert("P", palette=Image.ADAPTIVE, colors=256)

    with io.BytesIO() as output:
        image.save(
            output,
            format="PNG",
            optimize=True,
            compression=9,
            interlace=False,
            info=info,
        )
        return output.getvalue(), (new_width, new_height), scale, resized


def process_image(image):
    compressed_image_data, new_size, scale, resized = compress_image(
        image.pngBinary, 512
    )
    image.pngBinary = compressed_image_data

    if resized:
        for transform in image.transforms:
            old_width = transform.width
            old_crop_x = transform.xCrop
            old_crop_y = transform.yCrop
            old_points = transform.points

            # reset cropping
            transform.reset_crop(*new_size)

            # restore cropping
            new_points = []
            for i in range(len(old_points[0])):
                new_x = old_points[0][i] * scale
                new_y = old_points[1][i] * scale
                new_points.append((new_x, new_y))

            transform.points = [
                [point[0] for point in new_points],
                [point[1] for point in new_points],
            ]

            transform.xCrop = float(old_crop_x * scale)
            transform.yCrop = float(old_crop_y * scale)

            transform.scale_to_width(old_width)

    return image


import time


def process_pureref_file(input_pureref_filepath, output_pureref_filepath, processes=8):
    

    output_file = PurFile()
    read_pur_file(output_file, input_pureref_filepath)

    with Pool(processes=processes) as pool:
        output_file.images = pool.map(process_image, output_file.images)

    write_pur_file(output_file, output_pureref_filepath)


def main():
    start_time = time.time()
    input_pureref_filepath = "Patriot ref.pur"
    output_pureref_filepath = "tower_compressed.pur"
    process_pureref_file(input_pureref_filepath, output_pureref_filepath)
    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")


if __name__ == "__main__":
    # freeze_support()  # Only necessary if you're freezing your script with tools like py2exe or PyInstaller
    main()
