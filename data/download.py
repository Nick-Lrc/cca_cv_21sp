import os
import argparse
import subprocess

VIDEO_DIR = 'video'
FRAME_DIR = 'frame'

def download_videos(src, dst):
    video_output_dir = os.path.join(dst, VIDEO_DIR)
    create_directory(video_output_dir)
    with open(src, 'r') as f:
        os.chdir(video_output_dir)
        for video_id in f.readlines():
            subprocess.run(['youtube-dl', '--id', f'http://www.youtube.com/watch?v={video_id}'])
        os.chdir(os.path.join('..', '..'))

def video2frames(dst):
    video_input_dir = os.path.join(dst, VIDEO_DIR)
    frame_output_dir = os.path.join(dst, FRAME_DIR)
    create_directory(frame_output_dir)
    for i, f in enumerate(os.listdir(video_input_dir)):
        video_path = os.path.join(video_input_dir, f)
        frame_path = os.path.join(frame_output_dir, str(i))
        create_directory(frame_path)
        if os.path.isfile(video_path):
            subprocess.run([
                'ffmpeg',
                '-i', video_path,
                '-r', '1/1',
                f'{frame_path}{os.path.sep}%03d.jpg'
            ])

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def parse_options():
    parser = argparse.ArgumentParser(description='Download YouTube videos listed in the input file' + \
                                                 'and split each video into frames, one per second.')
    parser.add_argument('-i', '--input', type=str, help='List of YouTube video ids')
    return parser.parse_args()

if __name__ == '__main__':
    options = parse_options()
    output_dir = os.path.splitext(options.input)[0]
    create_directory(output_dir)

    print('Downloading videos...')
    download_videos(options.input, output_dir)
    print('Done.')
    print()

    print('Slicing videos into frames...')
    video2frames(output_dir)
    print('Done.')
