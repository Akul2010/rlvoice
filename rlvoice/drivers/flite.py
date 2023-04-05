import os
import subprocess
import tempfile
import rlvoice.driver

class FliteDriver(rlvoice.driver.DriverBase):
    def __init__(self):
        super().__init__()
        self._flite_process = None
        self._audio_file = None

    def init(self):
        self._audio_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        self._flite_process = subprocess.Popen(
            ["flite", "-o", self._audio_file.name],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )

    def say(self, text, *args):
        self._flite_process.stdin.write(text)
        self._flite_process.stdin.flush()

    def stop(self):
        self._flite_process.kill()
        os.unlink(self._audio_file.name)

    def get_properties(self):
        return {"voice": "slt"}

    def set_properties(self, properties):
        voice = properties.get("voice")
        if voice is not None:
            self._flite_process.kill()
            self._flite_process = subprocess.Popen(
                ["flite", "-voice", voice, "-o", self._audio_file.name],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )
