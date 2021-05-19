import subprocess

'''
This script installs/upgrades all required packages.
'''
PACKAGES = [
    'google-api-python-client',
    'google-auth',
    'google-auth-oauthlib',
    'google-auth-httplib2',
    'youtube-dl'
]

if __name__ == '__main__':
    for pkg in PACKAGES:
        print(f'Installing {pkg}...')
        subprocess.run(['pip', 'install', '-U', pkg])
        print()
    print('Note: You need to install FFmpeg manually.')
