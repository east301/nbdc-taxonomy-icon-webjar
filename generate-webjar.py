#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# generate-webjar.py
#
# A tiny script to re-package taxonomy icons from NBDC as WebJars.
#
# @author   Shu Tadaka
# @license  CC0
#

import argparse
import csv
import json
import os
import zipfile


def main():
    #
    parser = argparse.ArgumentParser()
    parser.add_argument('taxonomy_icon')
    parser.add_argument('taxonomy_icon_png')
    parser.add_argument('output')
    parser.add_argument('--name', default='nbdc-taxonomy-icon')
    parser.add_argument('--version', default='20130321')
    args = parser.parse_args()

    #
    webjar_path_prefix = 'META-INF/resources/webjars'
    with open(args.taxonomy_icon, 'rb') as fin, zipfile.ZipFile(args.output, 'w') as fout:
        #
        species = set()
        for index, record in enumerate(csv.reader(fin)):
            #
            if index == 0:
                continue

            #
            taxonomy_id = record[2]
            if (not taxonomy_id) or (not taxonomy_id.isdigit()):
                continue

            #
            species.add(taxonomy_id)
            for offset, type in enumerate(('L', 'NL', 'S', 'NS')):
                #
                source = os.path.join(args.taxonomy_icon_png, record[4 + offset])
                destination = '{}/{}/{}/{}-{}.png'.format(
                    webjar_path_prefix, args.name, args.version, taxonomy_id, type)

                #
                fout.write(source, destination)

        #
        destination = '{}/{}/species.json'.format(webjar_path_prefix, args.name, args.version)
        fout.writestr(destination, json.dumps(sorted(species)))


if __name__ == '__main__':
    main()
