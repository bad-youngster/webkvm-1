import os
import random
import string

import lockfile


class FilePermissionError(Exception):
    pass

def generate_key(key_length=64):

    if hasattr(random,'SystemRandom'):
        choice = random.SystemRandom().choice

    else:
        choice = random.choice
    return ''.join(map(lambda x: choice(string.digits + string.ascii_letters),
                       range(key_length)))

def generate_or_read_from_file(key_file='.secret_key',key_length=64):

    lock = lockfile.FileLock(key_file)

    if not lock.is_locked():
        if not os.path.exists(key_file):
            key = generate_key(key_length)
            old_umask = os.umask(0o177)
            with open(key_file,'w') as f:
                f.write(key)
            os.umask(old_umask)
        else:
            if oct(os.stat(key_file).st_mode & 0o777) != '0o600':
                raise FilePermissionError("Insecure key file permissions!")
            with open(key_file,'r') as f:
                key = f.readline()
        return key