#!/usr/bin/env python
__version__ = "0.1.dev0"

import argparse


def main(args=None):
  parser = argparse.ArgumentParser(description='Apply watermark to an image')
  parser.add_argument('image_file')
  parser.add_argument('watermark_text')
  args = parser.parse_args()
  print('watermark is running')
  print(args)
  print(args.image_file)
  print(args.watermark_text)
