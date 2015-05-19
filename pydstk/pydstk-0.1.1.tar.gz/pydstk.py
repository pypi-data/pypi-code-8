#!/usr/bin/env python3
"""Data Science Toolkit client for Python.

This module provides client library functions and CLI for the Data Science
Toolkit. The module was forked from the original dstk.py library provided with
the Data Science Toolkit.

See http://www.datasciencetoolkit.org/developerdocs#python for more details.
"""

import csv
import io
import json
import mimetypes
import os
import re
import requests
import sys

API_BASE = 'http://www.datasciencetoolkit.org'
API_VERSION = 50


# This is the main interface class. You can see an example of it in use
# below, implementing a command-line tool, but you basically just instantiate
# dstk = DSTK()
# and then call the method you want
# coordinates = dstk.ip2coordinates('12.34.56.78')
# The full documentation is at http://www.datasciencetoolkit.org/developerdocs
class DSTK(object):
  """Client class for dstk api."""

  def __init__(self, api_base=None, check_version=True):
    """Constructor for the dstk api client.

    Args:
      api_base: str, base url for the dstk server.
      check_version: bool, whether to check the server api version on startup.
    """
    if api_base is None:
      api_base = os.getenv('DSTK_API_BASE', API_BASE)
    self.api_base = api_base

    if check_version:
      self.check_version()

  def check_version(self):
    """Check the server api version."""
    api_url = '%s/info' % self.api_base

    try:
      response = requests.get(api_url)
      response_data = response.json()
      server_api_version = response_data['version']
    except:
      raise Exception(
        'The server at %s does not seem to be running DSTK, '
        'or version information could not be found.' % self.api_base)

    if server_api_version < API_VERSION:
      raise Exception(
        'DSTK: Version %s found at %s but %s is required' % (
          server_api_version, api_url, API_VERSION))

  def ip2coordinates(self, ips):

    if not isinstance(ips, (list, tuple)):
      ips = [ips]

    api_url = '%s/ip2coordinates' % self.api_base
    api_body = json.dumps(ips)
    response = requests.post(api_url, data=api_body)
    response_data = response.json()

    if 'error' in response_data:
      raise Exception(response_data['error'])

    return response_data

  def street2coordinates(self, addresses):

    if not isinstance(addresses, (list, tuple)):
      addresses = [addresses]

    api_url = '%s/street2coordinates' % self.api_base
    api_body = json.dumps(addresses)
    response = requests.post(api_url, data=api_body)
    response_data = response.json()

    if 'error' in response_data:
      raise Exception(response_data['error'])

    return response_data

  def coordinates2politics(self, coordinates):

    api_url = '%s/coordinates2politics' % self.api_base
    api_body = json.dumps(coordinates)
    response = requests.post(api_url, data=api_body)
    response_data = response.json()

    if 'error' in response_data:
      raise Exception(response_data['error'])

    return response_data

  def text2places(self, text):

    api_url = '%s/text2places' % self.api_base
    api_body = text
    response = requests.post(api_url, data=api_body)
    response_data = response.json()

    if 'error' in response_data:
      raise Exception(response_data['error'])

    return response_data

  def file2text(self, file_name, file_object):

    api_url = '%s/file2text' % self.api_base
    content_type = guess_content_type(file_name)
    files = {'file': ('inputfile', file_object, content_type)}
    response = requests.post(api_url, files=files)
    response_data = response.text

    return response_data

  def text2sentences(self, text):

    api_url = '%s/text2sentences' % self.api_base
    api_body = text
    response = requests.post(api_url, data=api_body)
    response_data = response.json()

    if 'error' in response_data:
      raise Exception(response_data['error'])

    return response_data

  def html2text(self, html):

    api_url = '%s/html2text' % self.api_base
    api_body = html
    response = requests.post(api_url, data=api_body)
    response_data = response.json()

    if 'error' in response_data:
      raise Exception(response_data['error'])

    return response_data

  def html2story(self, html):

    api_url = '%s/html2story' % self.api_base
    api_body = html
    response = requests.post(api_url, data=api_body)
    response_data = response.json()

    if 'error' in response_data:
      raise Exception(response_data['error'])

    return response_data

  def text2people(self, text):

    api_url = '%s/text2people' % self.api_base
    api_body = text
    response = requests.post(api_url, data=api_body)
    response_data = response.json()

    if 'error' in response_data:
      raise Exception(response_data['error'])

    return response_data

  def text2times(self, text):

    api_url = '%s/text2times' % self.api_base
    api_body = text
    response = requests.post(api_url, data=api_body)
    response_data = response.json()

    if 'error' in response_data:
      raise Exception(response_data['error'])

    return response_data

  def text2sentiment(self, text):

    api_url = '%s/text2sentiment' % self.api_base
    api_body = text
    response = requests.post(api_url, data=api_body)
    response_data = response.json()

    if 'error' in response_data:
      raise Exception(response_data['error'])

    return response_data

  def coordinates2statistics(self, coordinates):

    api_url = '%s/coordinates2statistics' % self.api_base
    api_body = json.dumps(coordinates)
    response = requests.post(api_url, data=api_body)
    response_data = response.json()

    if 'error' in response_data:
      raise Exception(response_data['error'])

    return response_data

def guess_content_type(filename):
  return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

# End of the interface. The rest of this file is an example implementation of a
# command line client.

def ip2coordinates_cli(dstk, options, inputs, output):

  writer = csv.writer(sys.stdout)

  input_ips = []
  for input_line in inputs:
    ip_match = re.match(r'[12]?\d?\d\.[12]?\d?\d\.[12]?\d?\d\.[12]?\d?\d', input_line)
    if ip_match is not None:
      input_ips.append(ip_match.group(0))
    else:
      print('No match')

  result = dstk.ip2coordinates(input_ips)

  if options['showHeaders']:
    for ip, info in result.items():
      if info is None:
        continue
      row = ['ip_address']
      for key, value in info.items():
        row.append(str(key))
      writer.writerow(row)
      break

  for ip, info in result.items():

    if info is None:
      info = {}

    row = [ip]
    for key, value in info.items():
      row.append(str(value))

    writer.writerow(row)

  return

def street2coordinates_cli(dstk, options, inputs, output):

  writer = csv.writer(sys.stdout)

  result = dstk.street2coordinates(inputs)

  if options['showHeaders']:
    for ip, info in result.items():
      if info is None:
        continue
      row = ['address']
      for key, value in info.items():
        row.append(str(key))
      writer.writerow(row)
      break

  for ip, info in result.items():

    if info is None:
      info = {}

    row = [ip]
    for key, value in info.items():
      row.append(str(value))

    writer.writerow(row)

  return

def coordinates2politics_cli(dstk, options, inputs, output):

  writer = csv.writer(output)

  coordinates_list = []
  for an_input in inputs:
    coordinates = an_input.split(',')
    if len(coordinates) != 2:
      output.write(
        'You must enter coordinates as a series of comma-separated pairs, eg 37.76,-122.42')
      exit(-1)
    coordinates_list.append([coordinates[0], coordinates[1]])

  result = dstk.coordinates2politics(coordinates_list)

  if options['showHeaders']:
    row = ['latitude', 'longitude', 'name', 'code', 'type', 'friendly_type']
    writer.writerow(row)

  for info in result:

    location = info['location']
    politics = info['politics']

    for politic in politics:
      row = [
        location['latitude'],
        location['longitude'],
        politic['name'],
        politic['code'],
        politic['type'],
        politic['friendly_type'],
      ]
      writer.writerow(row)

  return

def file2text_cli(dstk, options, inputs, output):

  for file_name in inputs:
    if os.path.isdir(file_name):
      children = os.listdir(file_name)
      full_children = []
      for child in children:
        full_children.append(os.path.join(file_name, child))
      file2text_cli(dstk, options, full_children, output)
    else:
      file_object = get_file_or_url_object(file_name)
      if options['showHeaders']:
        output.write('--File--: '+file_name+"\n")
      result = dstk.file2text(file_name, file_object)

      print(result)
  return

def text2places_cli(dstk, options, inputs, output):

  writer = csv.writer(output)

  if options['showHeaders']:
    row = [
      'latitude', 'longitude', 'name', 'type', 'start_index', 'end_index',
      'matched_string', 'file_name']
    writer.writerow(row)
  options['showHeaders'] = False

  if options['from_stdin']:
    result = dstk.text2places("\n".join(inputs))
    text2places_format(result, 'stdin', writer)
    return

  for file_name in inputs:
    if os.path.isdir(file_name):
      children = os.listdir(file_name)
      full_children = []
      for child in children:
        full_children.append(os.path.join(file_name, child))
      text2places_cli(dstk, options, full_children, output)
    else:
      file_object = get_file_or_url_object(file_name)
      result = dstk.text2places(file_object)
      text2places_format(result, file_name, writer)

  return

def text2places_format(result, file_name, writer):
  for info in result:

    row = [
      info['latitude'],
      info['longitude'],
      info['name'],
      info['type'],
      info['start_index'],
      info['end_index'],
      info['matched_string'],
      file_name
    ]
    writer.writerow(row)
  return

def html2text_cli(dstk, options, inputs, output):

  if options['from_stdin']:
    result = dstk.html2text("\n".join(inputs))
    print(result['text'])
    return

  for file_name in inputs:
    if os.path.isdir(file_name):
      children = os.listdir(file_name)
      full_children = []
      for child in children:
        full_children.append(os.path.join(file_name, child))
      html2text_cli(dstk, options, full_children, output)
    else:
      file_object = get_file_or_url_object(file_name)
      if options['showHeaders']:
        output.write('--File--: '+file_name+"\n")
      result = dstk.html2text(file_object)
      print(result['text'])
  return

def text2sentences_cli(dstk, options, inputs, output):

  if options['from_stdin']:
    result = dstk.text2sentences("\n".join(inputs))
    print(result['sentences'])
    return

  for file_name in inputs:
    if os.path.isdir(file_name):
      children = os.listdir(file_name)
      full_children = []
      for child in children:
        full_children.append(os.path.join(file_name, child))
      text2sentences_cli(dstk, options, full_children, output)
    else:
      file_object = get_file_or_url_object(file_name)
      if options['showHeaders']:
        output.write('--File--: '+file_name+"\n")
      result = dstk.text2sentences(file_object)
      print(result['sentences'])

  return

def html2story_cli(dstk, options, inputs, output):

  if options['from_stdin']:
    result = dstk.html2story("\n".join(inputs))
    print(result['story'])
    return

  for file_name in inputs:
    if os.path.isdir(file_name):
      children = os.listdir(file_name)
      full_children = []
      for child in children:
        full_children.append(os.path.join(file_name, child))
      html2story_cli(dstk, options, full_children, output)
    else:
      file_object = get_file_or_url_object(file_name)
      if options['showHeaders']:
        output.write('--File--: '+file_name+"\n")
      result = dstk.html2story(file_object)
      print(result['story'])

  return

def text2people_cli(dstk, options, inputs, output):

  writer = csv.writer(sys.stdout)

  if options['showHeaders']:
    row = [
      'matched_string', 'first_name', 'surnames', 'title', 'gender',
      'start_index', 'end_index', 'file_name']
    writer.writerow(row)
  options['showHeaders'] = False

  if options['from_stdin']:
    result = dstk.text2people("\n".join(inputs))
    text2people_format(result, 'stdin', writer)
    return

  for file_name in inputs:
    if os.path.isdir(file_name):
      children = os.listdir(file_name)
      full_children = []
      for child in children:
        full_children.append(os.path.join(file_name, child))
      text2places_cli(dstk, options, full_children, output)
    else:
      file_object = get_file_or_url_object(file_name)
      result = dstk.text2people(file_object)
      text2people_format(result, file_name, writer)

  return

def text2people_format(result, file_name, writer):
  for info in result:

    row = [
      info['matched_string'],
      info['first_name'],
      info['surnames'],
      info['title'],
      info['gender'],
      str(info['start_index']),
      str(info['end_index']),
      file_name
    ]
    writer.writerow(row)
  return

def text2times_cli(dstk, options, inputs, output):

  writer = csv.writer(sys.stdout)

  if options['showHeaders']:
    row = [
      'matched_string', 'time_string', 'time_seconds', 'is_relative',
      'start_index', 'end_index', 'file_name']
    writer.writerow(row)
  options['showHeaders'] = False

  if options['from_stdin']:
    result = dstk.text2times("\n".join(inputs))
    text2times_format(result, 'stdin', writer)
    return

  for file_name in inputs:
    if os.path.isdir(file_name):
      children = os.listdir(file_name)
      full_children = []
      for child in children:
        full_children.append(os.path.join(file_name, child))
      text2times_cli(dstk, options, full_children, output)
    else:
      file_object = get_file_or_url_object(file_name)
      result = dstk.text2times(file_object)
      text2times_format(result, file_name, writer)

  return

def text2times_format(result, file_name, writer):
  for info in result:

    row = [
      info['matched_string'],
      info['time_string'],
      info['time_seconds'],
      info['is_relative'],
      str(info['start_index']),
      str(info['end_index']),
      file_name
    ]
    writer.writerow(row)
  return

def text2sentiment_cli(dstk, options, inputs, output):
  writer = csv.writer(sys.stdout)

  if options['showHeaders']:
    row = ['sentiment', 'sentence', 'file_name']
    writer.writerow(row)
  options['showHeaders'] = False

  if options['from_stdin']:
    result = []
    for sentence in inputs:
      result = dstk.text2sentiment(sentence)
      text2sentiment_format(result, sentence, 'stdin', writer)
    return

  for file_name in inputs:
    if os.path.isdir(file_name):
      children = os.listdir(file_name)
      full_children = []
      for child in children:
        full_children.append(os.path.join(file_name, child))
      text2sentiment_cli(dstk, options, full_children, output)
    else:
      file_object = get_file_or_url_object(file_name)
      for sentence in file_object.split("\n"):
        result = dstk.text2sentiment(sentence)
        text2sentiment_format(result, sentence, 'stdin', writer)

  return

def text2sentiment_format(result, sentence, file_name, writer):
  row = [
    result['score'],
    sentence.strip(),
    file_name
  ]
  writer.writerow(row)
  return

def coordinates2statistics_cli(dstk, options, inputs, output):

  writer = csv.writer(output)

  coordinates_list = []
  for an_input in inputs:
    coordinates = an_input.split(',')
    if len(coordinates) != 2:
      output.write(
        'You must enter coordinates as a series of comma-separated pairs, eg 37.76,-122.42')
      exit(-1)
    coordinates_list.append([coordinates[0], coordinates[1]])

  results = dstk.coordinates2statistics(coordinates_list)

  if options['showHeaders']:
    row = ['latitude', 'longitude', 'statistic', 'value', 'description']
    writer.writerow(row)

  for result in results:

    location = result['location']
    statistics = result['statistics']

    for statistic, info in statistics.items():

      value = info['value']
      description = info['description']
      row = [
        location['latitude'],
        location['longitude'],
        statistic,
        value,
        description,
      ]
      writer.writerow(row)

  return

def get_file_or_url_object(file_name):
  if file_name.startswith('http://') or file_name.startswith('https://'):
    response = requests.get(file_name)
    file_object = io.BytesIO(b'')
    file_object.writelines(response.iter_lines())
    file_object.seek(0)
  else:
    file_object = open(file_name, 'rb')
  return file_object

def print_usage(message=''):

  print(message)
  print("Usage:")
  print("python dstk.py <command> [-a/--api_base 'http://yourhost.com'] [-h/--show_headers] <inputs>")
  print("Where <command> is one of:")
  print("  ip2coordinates          (lat/lons for IP addresses)")
  print("  street2coordinates      (lat/lons for postal addresses)")
  print("  coordinates2politics    (country/state/county/constituency/etc for lat/lon)")
  print("  text2places             (lat/lons for places mentioned in unstructured text)")
  print("  file2text               (PDF/Excel/Word to text, and OCR on PNG/Jpeg/Tiff images)")
  print("  text2sentences          (parts of the text that look like proper sentences)")
  print("  html2text               (text version of the HTML document)")
  print("  html2story              (text version of the HTML with no boilerplate)")
  print("  text2people             (gender for people mentioned in unstructured text)")
  print("  text2times              (times and dates mentioned in unstructured text)")
  print("  text2sentiment          (estimates the positive or negative sentiment of each line of text)")
  print("  coordinates2statistics  (population/climate/elevation/etc for lat/lon)")
  print("If no inputs are specified, then standard input will be read and used")
  print("See http://www.datasciencetoolkit.org/developerdocs for more details")
  print("Examples:")
  print("python dstk.py ip2coordinates 67.169.73.113")
  print("python dstk.py street2coordinates \"2543 Graystone Place, Simi Valley, CA 93065\"")
  print("python dstk.py file2text scanned.jpg")

  exit(-1)


def main():

  commands = {
    'ip2coordinates': {'handler': ip2coordinates_cli},
    'street2coordinates': {'handler': street2coordinates_cli},
    'coordinates2politics': {'handler': coordinates2politics_cli},
    'text2places': {'handler': text2places_cli},
    'file2text': {'handler': file2text_cli},
    'text2sentences': {'handler': text2sentences_cli},
    'html2text': {'handler': html2text_cli},
    'html2story': {'handler': html2story_cli},
    'text2people': {'handler': text2people_cli},
    'text2times': {'handler': text2times_cli},
    'text2sentiment': {'handler': text2sentiment_cli},
    'coordinates2statistics': {'handler': coordinates2statistics_cli},
  }
  switches = {
    'api_base': True,
    'show_headers': True
  }

  command = None
  options = {'showHeaders': False}
  inputs = []

  ignore_next = False
  for index, arg in enumerate(sys.argv[1:]):
    if ignore_next:
      ignore_next = False
      continue

    if arg[0] == '-' and len(arg) > 1:
      if len(arg) == 2:
        letter = arg[1]
        if letter == 'a':
          option = 'api_base'
        elif letter == 'h':
          option = 'show_headers'
      else:
        option = arg[2:]

      if option not in switches:
        print_usage('Unknown option "'+arg+'"')

      if option == 'api_base':
        if (index+2) >= len(sys.argv):
          print_usage('Missing argument for option "'+arg+'"')
        options['apiBase'] = sys.argv[index+2]
        ignore_next = True
      elif option == 'show_headers':
        options['showHeaders'] = True

    else:
      if command is None:
        command = arg
        if command not in commands:
          print_usage('Unknown command "'+arg+'"')
      else:
        inputs.append(arg)

  if command is None:
    print_usage('No command specified')

  if len(inputs) < 1:
    options['from_stdin'] = True
    inputs = sys.stdin.readlines()
  else:
    options['from_stdin'] = False

  command_info = commands[command]

  dstk = DSTK(api_base=options.get('apiBase'))

  command_info['handler'](dstk, options, inputs, sys.stdout)

if __name__ == '__main__':
  main()
