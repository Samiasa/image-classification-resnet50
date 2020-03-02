# NIST-developed software is provided by NIST as a public service. You may use, copy and distribute copies of the software in any medium, provided that you keep intact this entire notice. You may improve, modify and create derivative works of the software or any portion of the software, and you may copy and distribute such modifications or works. Modified works should carry a notice stating that you changed the software and should note the date and nature of any such change. Please explicitly acknowledge the National Institute of Standards and Technology as the source of the software.
# NIST-developed software is expressly provided "AS IS." NIST MAKES NO WARRANTY OF ANY KIND, EXPRESS, IMPLIED, IN FACT OR ARISING BY OPERATION OF LAW, INCLUDING, WITHOUT LIMITATION, THE IMPLIED WARRANTY OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, NON-INFRINGEMENT AND DATA ACCURACY. NIST NEITHER REPRESENTS NOR WARRANTS THAT THE OPERATION OF THE SOFTWARE WILL BE UNINTERRUPTED OR ERROR-FREE, OR THAT ANY DEFECTS WILL BE CORRECTED. NIST DOES NOT WARRANT OR MAKE ANY REPRESENTATIONS REGARDING THE USE OF THE SOFTWARE OR THE RESULTS THEREOF, INCLUDING BUT NOT LIMITED TO THE CORRECTNESS, ACCURACY, RELIABILITY, OR USEFULNESS OF THE SOFTWARE.
# You are solely responsible for determining the appropriateness of using and distributing the software and you assume all risks associated with its use, including but not limited to the risks and costs of program errors, compliance with applicable laws, damage to or loss of data, programs or equipment, and the unavailability or interruption of operation. This software is not intended to be used in any situation where a failure could cause risk of injury or damage to property. The software developed by NIST employees is not subject to copyright protection within the United States.

import sys
if sys.version_info[0] < 3:
    raise RuntimeError('Python3 Required')

import skimage.io
import numpy as np
import csv
import os
import skimage
import skimage.transform
import argparse
from isg_ai_pb2 import ImageNumberPair
import shutil
import lmdb
import random


def read_image(fp):
    img = skimage.io.imread(fp, as_gray=True)
    return img


def write_img_to_db(txn, img, number, key_str):
    if type(img) is not np.ndarray:
        raise Exception("Img must be numpy array to store into db")
    if type(number) is not np.ndarray:
        number = np.asarray(number)
    if len(img.shape) > 3:
        raise Exception("Img must be 2D or 3D [HW, or HWC] format")
    if len(img.shape) < 2:
        raise Exception("Img must be 2D or 3D [HW, or HWC] format")

    if len(img.shape) == 2:
        # make a 3D array
        img = img.reshape((img.shape[0], img.shape[1], 1))

    datum = ImageNumberPair()
    if len(img.shape) == 3:
        # if color, record the number of channels
        datum.channels = img.shape[2]
    else:
        datum.channels = 1
    datum.img_height = img.shape[0]
    datum.img_width = img.shape[1]
    datum.image = img.tobytes()
    datum.number = number.tobytes()

    datum.img_type = img.dtype.str
    datum.num_type = number.dtype.str

    txn.put(key_str.encode('ascii'), datum.SerializeToString())
    return


def generate_database(img_list, database_name, image_filepath, csv_filepath, output_folder):
    output_image_lmdb_file = os.path.join(output_folder, database_name)

    if os.path.exists(output_image_lmdb_file):
        print('Deleting existing database')
        shutil.rmtree(output_image_lmdb_file)

    if not os.path.exists(csv_filepath):
        raise RuntimeError('Ground Truth csv filepath missing: "{}"'.format(csv_filepath))

    image_env = lmdb.open(output_image_lmdb_file, map_size=int(5e12))
    image_txn = image_env.begin(write=True)

    # load the ground truth csv file into a dict
    ground_truth = dict()
    with open(csv_filepath, 'r') as fh:
        reader = csv.reader(fh, delimiter=',')
        for row in reader:
            ground_truth[row[0]] = float(row[1].strip())

    txn_nb = 0
    for i in range(len(img_list)):
        print('  {}/{}'.format(i, len(img_list)))
        img_file_name = img_list[i]
        block_key, _ = os.path.splitext(img_file_name)

        img = read_image(os.path.join(image_filepath, img_file_name))
        num = ground_truth[img_file_name]

        key_str = '{}_:{}'.format(block_key, num)
        txn_nb += 1
        write_img_to_db(image_txn, img, num, key_str)

        if txn_nb % 1000 == 0:
            image_txn.commit()
            image_txn = image_env.begin(write=True)

    image_txn.commit()
    image_env.close()


def main(image_folder, csv_filepath, output_folder, dataset_name, train_fraction, image_format):
    if image_format.startswith('.'):
        # remove leading period
        image_format = image_format[1:]

    image_folder = os.path.abspath(image_folder)
    output_folder = os.path.abspath(output_folder)

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    # find the image files for which annotations exist
    img_files = [f for f in os.listdir(image_folder) if f.endswith(image_format)]

    # in place shuffle
    random.shuffle(img_files)

    idx = int(train_fraction * len(img_files))
    train_img_files = img_files[0:idx]
    test_img_files = img_files[idx:]

    print('building train database')
    database_name = 'train-{}.lmdb'.format(dataset_name)
    generate_database(train_img_files, database_name, image_folder, csv_filepath, output_folder)

    print('building test database')
    database_name = 'test-{}.lmdb'.format(dataset_name)
    generate_database(test_img_files, database_name, image_folder, csv_filepath, output_folder)


if __name__ == "__main__":
    # Define the inputs
    # ****************************************************

    # Setup the Argument parsing
    parser = argparse.ArgumentParser(prog='build_lmdb', description='Script which converts folder of images into a pair of lmdb databases for training.')

    parser.add_argument('--image_folder', dest='image_folder', type=str, help='filepath to the folder containing the images', default='../data/images/')
    parser.add_argument('--csv_filepath', dest='csv_filepath', type=str, help='filepath to the file containing the ground truth labels', default='../data/ground_truth.csv')

    parser.add_argument('--output_folder', dest='output_folder', type=str, help='filepath to the folder where the outputs will be placed', default='../data/')
    parser.add_argument('--dataset_name', dest='dataset_name', type=str, help='name of the dataset to be used in creating the lmdb files', default='mnist')
    parser.add_argument('--train_fraction', dest='train_fraction', type=float,
                        help='what fraction of the dataset to use for training (0.0, 1.0)', default=0.8)
    parser.add_argument('--image_format', dest='image_format', type=str,
                        help='format (extension) of the input images. E.g {tif, jpg, png)', default='tif')

    args = parser.parse_args()
    image_folder = args.image_folder
    csv_filepath = args.csv_filepath
    output_folder = args.output_folder
    dataset_name = args.dataset_name
    train_fraction = args.train_fraction
    image_format = args.image_format

    main(image_folder, csv_filepath, output_folder, dataset_name, train_fraction, image_format)




