import subprocess
import tempfile

def get_fingerprint(pubkey):
    try:
        with tempfile.NamedTemporaryFile(mode='w+') as f:
            f.write(pubkey)
            f.flush()
            # ssh-keygen -l -f <file>
            result = subprocess.check_output(['ssh-keygen', '-l', '-f', f.name], stderr=subprocess.STDOUT)
            return result.decode('utf-8').strip()
    except Exception as e:
        return f"Error: {e}"

key = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAII0E8WGBqA+IKr/WhN2Y7fvPhYj/2VFv8PJ4OJe5nyTu joe@x1c9"
print(get_fingerprint(key))
