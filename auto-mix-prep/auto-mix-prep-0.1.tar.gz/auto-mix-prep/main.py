import pydub

import argparse
import os
import datetime
import shutil


def main():
    directory = '.'
    wave_file_list = []

    parser = argparse.ArgumentParser(description='Program for automatic gain' +
                                     'staging to desired dB')

    parser.add_argument('-dB',
                        '--decibel',
                        nargs=1,
                        help='dB to set')

    parser.add_argument('-f',
                        '--file',
                        nargs=1,
                        help='Set dB for individual file')

    parser.add_argument(
        '-d',
        '--directory',
        nargs=1,
        help='Set directory (working directory if not specified)')

    parser.add_argument(
        '-b',
        '--backup',
        nargs='?',
        const='',
        type=str,
        help='Backup files in specified directory before gain ' +
        'staging (Creates folder in working directory if not specified)')

    args = parser.parse_args()

    if args.backup:
        current_date = datetime.datetime.strftime(
            datetime.datetime.now(),
            '%Y-%m-%d %H:%M')

        backup_dir = 'Stems Backup ' + current_date
        os.mkdir(backup_dir)
        print('Making backup in folder "{}"'.format(backup_dir))

        for file in os.listdir(directory):
            if file.endswith('.wav'):
                shutil.copy2(file, '{}/{}'.format(backup_dir, file))

    if args.decibel:
        decibel = int((args.decibel[0]))
        print(decibel)

        if decibel > 0:
            if question_y_or_n('You\'ve selected a peak above 0 dB which will ' +
                               'cause clipping. Continue?', n_dominant=True):
                pass

            else:
                return 0

    if args.directory:
        directory = args.directory[0]

    if args.file:
        file_name = args.file[0]
        change_max_db(file_name, decibel)

    else:
        for file in os.listdir(directory):
            if file.endswith('.wav'):
                wave_file_list.append(file)

        for wave_file in wave_file_list:
            change_max_db(wave_file, decibel)
            print()


def question_y_or_n(question, y_dominant=True, n_dominant=False):
    if n_dominant:
        y_dominant = False

    yes_response = ['y', 'yes', 'ye']
    no_response = ['n', 'no']

    if y_dominant:
        yes_response.append('')
        print(question + ' [Y/n]')

    else:
        no_response.append('')
        print(question + ' [y/N]')

    user_choice = input().lower()

    if user_choice in yes_response:
        return True
    else:
        return False


def change_max_db(file_name, decibel):
    audio_file = pydub.AudioSegment.from_file(file_name)
    peak_amplitude = get_peak_db(file_name)

    print(
        '{} peak dB is currently {} dB'.format(
            file_name,
            audio_file.max_dBFS))

    reduction_gain = peak_amplitude - decibel
    audio_file = audio_file - reduction_gain

    if question_y_or_n('Export new file?'):
        audio_file.export(file_name, format='wav')

        print('{} exported'.format(file_name))
        print('With peak dB {}'.format(get_peak_db(file_name)))

    else:
        return


def get_peak_db(file_name):
    audio_file = pydub.AudioSegment.from_file(file_name)
    return audio_file.max_dBFS


if __name__ == '__main__':
    main()
