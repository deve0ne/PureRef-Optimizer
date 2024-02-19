import argparse
from PIL import Image
import io
import time
from multiprocessing import Pool
from PureRef_format.purformat.read import read_pur_file
from PureRef_format.purformat.write import write_pur_file
from PureRef_format.purformat.purformat import PurFile


def process_image(args, image):
    compressed_image_data, new_size, scale = compress_image(image.pngBinary, args.max_dimension, args.colors)
    image.pngBinary = compressed_image_data

    if scale < 1:
        for transform in image.transforms:
            fix_transform(transform, new_size, scale)

    return image


def compress_image(image_data, max_dimension, colors):
    with Image.open(io.BytesIO(image_data)) as image:
        scale = min(max_dimension / max(image.size), 1)

        if scale < 1:
            image.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)

        image = image.convert("P", palette=Image.ADAPTIVE, colors=colors)

        with io.BytesIO() as output:
            image.save(output, format="PNG", optimize=True)
            compressed_image_data = output.getvalue()

    return compressed_image_data, image.size, scale


def fix_transform(transform, new_size, scale):
    old_width = transform.width
    new_xCrop = transform.xCrop * scale
    new_yCrop = transform.yCrop * scale
    new_points = [[coord * scale for coord in axis]
                  for axis in transform.points]

    transform.reset_crop(*new_size)

    transform.xCrop = new_xCrop
    transform.yCrop = new_yCrop
    transform.points = new_points

    transform.scale_to_width(old_width)


def process_pureref_file(args):
    output_file = PurFile()
    read_pur_file(output_file, args.input_pureref_filepath)

    with Pool(processes=args.processes) as pool:
        from functools import partial
        process_image_with_args = partial(process_image, args)
        output_file.images = pool.map(process_image_with_args, output_file.images)

    output_pureref_filepath = args.input_pureref_filepath.rsplit('.pur', 1)[0] + "_compressed.pur"
    write_pur_file(output_file, output_pureref_filepath)


def main():
    parser = argparse.ArgumentParser(description="Optimize PureRef files.")
    parser.add_argument("input_pureref_filepath", type=str, help="The input PureRef file path.")
    parser.add_argument("--max_dimension", type=int, default=2048, help="Maximum dimension for the longest side of the image.")
    parser.add_argument("--colors", type=int, default=256, help="Number of colors for the image palette.")
    parser.add_argument("--processes", type=int, default=8, help="Number of processes to use.")
    args = parser.parse_args()

    start_time = time.time()
    process_pureref_file(args)
    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")


if __name__ == "__main__":
    main()
