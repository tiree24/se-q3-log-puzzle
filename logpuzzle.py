#!/usr/bin/env python2
"""
Log Puzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Given an Apache logfile, find the puzzle URLs and download the images.

Here's what a puzzle URL looks like (spread out onto multiple lines):
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;
rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

__author__ = "Tiree I got help from Mike the coach"

import os
import re
import sys
import urllib.request
import argparse


def place_sort(url):
    """ helper function to sort by last world """
    split_url = url.split('-')
    return split_url[-1]


def read_urls(filename):
    """Returns a list of the puzzle URLs from the given log file,
    extracting the hostname from the filename itself, sorting
    alphabetically in increasing order, and screening out duplicates.
    """
    url_list = []
    server_name = ''
    sorted_url_list = []
    with open(filename) as f:
        split_filename = filename.split('_')
        server_name = split_filename[-1]
        text = f.read().split(' ')
        for split_str in text:
            if filename == 'place_code.google.com':
                if re.search(r'\w+-\w+\.jpg', split_str):
                    url_list.append('http://' + server_name + split_str)
                    url_list = list(set(url_list))
                    sorted_url_list = sorted(url_list, key=place_sort)
            if filename == 'animal_code.google.com':
                if 'puzzle' in split_str and split_str not in url_list:
                    url_list.append('http://' + server_name + split_str)
                    url_list = list(set(url_list))
                    sorted_url_list = sorted(url_list)
        return sorted_url_list


def download_images(img_urls, dest_dir):
    """Given the URLs already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory with an <img> tag
    to show each local image file.
    Creates the directory if necessary.
    """
    os.mkdir(dest_dir)
    html_image_tags_str = ''
    for i, img_url in enumerate(img_urls):
        print("Retrieving...: ", img_url)
        urllib.request.urlretrieve(
            img_url, filename=dest_dir + '/img' + str(i) + '.jpg')
        html_image_tags_str = html_image_tags_str + \
            '<img src="img' + str(i) + '.jpg">'
    with open(dest_dir + '/index.html', 'w') as f:
        f.write('<html><body>' + html_image_tags_str + '</body></html>')
    return


def create_parser():
    """Creates an argument parser object."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',
                        help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parses args, scans for URLs, gets images from URLs."""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
