#!/usr/bin/env python                                               
 
""" 
create_synset.py is a code specifically designed for 
jpgs crawled from bobaedream.co.kr 
to create synsets.txt and synset_names.txt

TODO (hsong):
- NONE
 
"""

import getopt
import re
import sys

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


def generate_synset_file(h_car, jpg_file, synset_file, synset_name_file):
    f_out_synset = open(synset_file, 'w+')
    f_out_synset_name = open(synset_name_file, 'w+')
    f_jpg = open(jpg_file, 'r+')

    prev_model_id = ''
    for line in f_jpg:
        (d, make_id, model_id, jpg_id) = line.rstrip().split('/', 4)
        key = "%s_%s" % (make_id, model_id)

        if prev_model_id == '' or not prev_model_id == model_id:
            model_name = ''
            if key in h_car:
                model_name = h_car[key]
            else:
                print "WARN 00003: inexisting key [%s] was referenced from h_car [%s]" % (key, line.rstrip())
                continue
            f_out_synset.write("%s/%s\n" % (make_id, model_id))
            f_out_synset_name.write("%s/%s %s\n" % (make_id, model_id, model_name))
        prev_model_id = model_id

    f_out_synset.close()
    f_out_synset_name.close()
    f_jpg.close()


def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'c:j:s:w:')
    except getopt.GetoptError:
        print 'create_train_val.py -car <input car list> -jpg <input jp .list> -synsets <output synset file> -synset_words <output synset_words file>'
        sys.exit(2)

    car_file = ''
    jpg_file = ''
    synset_file = ''
    synset_name_file = ''
    for opt, arg in opts:
        if opt == '-c':
            car_file = arg
            print 'Input car list file: [%s]' % car_file
        elif opt == '-j':
            jpg_file = arg
            print 'Input jpg list file: [%s]' % jpg_file
        elif opt == '-s':
            synset_file = arg
            print 'Output synset file: [%s]' % synset_file
        elif opt == '-w':
            synset_name_file = arg
            print 'Output synset_words file: [%s]' % synset_name_file
        else:
            print 'ERROR 00000: Input argument [%s] [%s]' % (opt, arg)

    h_car = read_car_file(car_file)
    generate_synset_file(h_car, jpg_file, synset_file, synset_name_file)


if __name__ == "__main__":
    main(sys.argv[1:])
