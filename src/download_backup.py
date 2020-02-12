"""Downloads a backup in the s3 folder to downloaded.dump and stores
meta info in downloaded.json.

This will download the latest key in the appropriate folder unless the argument
--meta is specified and points to a .json file containing the information about
the file to download.
"""
import aws_utils
import os
import argparse
import json
import settings


def main(args=None):
    parser = argparse.ArgumentParser('Download backup')
    parser.add_argument('--meta', help='The meta file describing what to download')
    args = parser.parse_args(args=args)

    cfg = settings.load_settings()
    s3 = aws_utils.connect_to_s3(cfg)

    if args.meta is None:
        print('Finding the most recent backup...')
        key = get_most_recent(s3, cfg)
    else:
        print('Loading the meta file...')
        with open(args.meta, 'r') as infile:
            meta = json.load(infile)
        key = meta['key']

    local_name = key.split('/')[-1]
    print(f'Downloading {key} to {local_name}')
    s3.download_file(cfg['AWS_S3_BUCKET'], key, local_name)
    print('Done!')
    if os.path.exists('downloaded.dump'):
        print('Deleting downloaded.dump')
        os.remove('downloaded.dump')
    if os.path.exists('downloaded.json'):
        print('Deleting downloaded.json')
        os.remove('downloaded.json')
    print(f'Moving {local_name} to downloaded.dump')
    os.rename(local_name, 'downloaded.dump')
    print('Storing meta info in downloaded.json')
    with open('downloaded.json', 'w') as outfile:
        json.dump({'key': key}, outfile)


def get_most_recent(s3, cfg):
    # https://stackoverflow.com/a/45377836
    objs = s3.list_objects_v2(
        Bucket=cfg['AWS_S3_BUCKET'],
        Prefix=cfg['AWS_S3_FOLDER']
    )
    get_last_modified = lambda obj: int(obj['LastModified'].strftime('%s'))
    last_added = [obj['Key'] for obj in sorted(objs, key=get_last_modified)][0]

    print(f'Most recent backup: {last_added}')
    return last_added


if __name__ == '__main__':
    main()
