#!/usr/bin/env python                                               
 
""" 
create_train_val.py is a code specifically designed for 
jpgs crawled from bobaedream.co.kr 
to create train.txt, val.txt for training / validation.

TODO (hsong):
- NONE
 
"""

import getopt
import re
import sys

N_VAL_JPG_FILE_COUNT = 50


def read_car_file(car_file):
    h_car = dict()
    f_car = open(car_file, 'r+')
    for line in f_car:
        if re.search('^#', line):
            continue

        (make_id, model_id, model_name, number) = line.rstrip().split('|', 4)
        key = "make%s_model%s" % (make_id, model_id)
        h_car[key] = model_name

    f_car.close()
    return h_car


def generate_train_val_file(h_car, jpg_file, train_file, val_file):
    f_out_val = open(val_file, 'w+')
    f_out_train = open(train_file, 'w+')
    f_jpg = open(jpg_file, 'r+')

    i = 0
    index = 0
    prev_model_id = ''
    for line in f_jpg:
        (d, make_id, model_id, jpg_id) = line.rstrip().split('/', 4)
        key = "%s_%s" % (make_id, model_id)

        if not prev_model_id == '' and not prev_model_id == model_id:
            i = 0
            index+=1

        if not key in h_car:
            print "WARN 00003: inexisting key [%s] was referenced from h_car [%s]" % (key, line.rstrip())
            continue

        if i < N_VAL_JPG_FILE_COUNT:
            f_out_val.write("%s/%s/%s %d\n" % (make_id, model_id, jpg_id, index))
        else:
            f_out_train.write("%s/%s/%s %d\n" % (make_id, model_id, jpg_id, index))
                       
        prev_model_id = model_id
        i+=1

    f_out_val.close()
    f_out_train.close()
    f_jpg.close()


def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'c:j:t:v:')
    except getopt.GetoptError:
        print 'create_train_val.py -car <input car list> -jpg <input jp .list> -train <output train file> -val <output validation file>'
        sys.exit(2)

    car_file = ''
    jpg_file = ''
    train_file = ''
    val_file = ''
    for opt, arg in opts:
        if opt == '-c':
            car_file = arg
            print 'Input car list file: [%s]' % car_file
        elif opt == '-j':
            jpg_file = arg
            print 'Input jpg list file: [%s]' % jpg_file
        elif opt == '-t':
            train_file = arg
            print 'Output train file: [%s]' % train_file
        elif opt == '-v':
            val_file = arg
            print 'Output validation file: [%s]' % val_file
        else:
            print 'ERROR 00000: Input argument [%s] [%s]' % (opt, arg)

    h_car = read_car_file(car_file)
    generate_train_val_file(h_car, jpg_file, train_file, val_file)


if __name__ == "__main__":
    main(sys.argv[1:])
