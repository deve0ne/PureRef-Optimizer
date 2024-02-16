from PIL import Image
import io
from PureRef_format.purformat.read import read_pur_file
from PureRef_format.purformat.write import write_pur_file
from PureRef_format.purformat.purformat import PurFile

def compress_image(image_data, quality=85):
    """
    Compress an image.
    :param image_data: The binary data of the image to compress.
    :param quality: The quality level of the compression, defaults to 85.
    :return: The compressed image data.
    """
    # Load the image data into a PIL Image object
    
    image = Image.open(io.BytesIO(image_data))
    
    # Adjust the compression level (0-9)
    compression_level = 9  # Higher is more compression, but slower
    
    # Remove metadata
    info = image.info
    info.pop("exif", None)
    
    image = image.convert('P', palette=Image.ADAPTIVE, colors=256)
    
    # Compress the image
    with io.BytesIO() as output:
        image.save('compressed.png', format='PNG', optimize=True, compression=compression_level, interlace=False, info=info)
        return output.getvalue()

def process_pureref_file(input_pureref_filepath, output_file, output_pureref_filepath):
    """
    Process a PureRef file: read it, compress its images, and write to a new file.
    :param input_file_path: Path to the input PureRef file.
    :param output_file_path: Path where the output PureRef file will be saved.
    """
    # Read the PureRef file
    read_pur_file(output_file, input_pureref_filepath)
    
    # Compress each image in the PureRef file
    for image in output_file.images:       
        compressed_image_data = compress_image(image.pngBinary)
        image.pngBinary = compressed_image_data
    
    # Write the modified PureRef file to a new file
    write_pur_file(output_file, output_pureref_filepath)

input_pureref_filepath = 'tower.pur'
output_pureref_file = PurFile()
output_pureref_filepath = "tower_compressed.pur"
process_pureref_file(input_pureref_filepath, output_pureref_file, output_pureref_filepath)