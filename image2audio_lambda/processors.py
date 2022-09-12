import librosa
import librosa.display
import soundfile as sf
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageOps
from sklearn.preprocessing import MinMaxScaler

try:
    from IPython.display import Audio, display
except ModuleNotFoundError:
    def Audio(*args, **kwargs):
        pass
    display = Audio


class AudioProcessor:
    def __init__(self, sampling_rate=44100):
        self.sampling_rate = sampling_rate
        self.spectrogram = None
        self.soundwave = None
        self.spectrogram_image = None
        self.spectrogram_image_array = None
        self.scaler = MinMaxScaler(feature_range=(0, 255))

    def load_sound_wave(self, path):
        self.sampling_rate = librosa.get_samplerate(path)
        self.soundwave, self.sampling_rate = librosa.load(path, sr=self.sampling_rate)

    def wave_to_spec(self):
        self.spectrogram = librosa.amplitude_to_db(librosa.stft(self.soundwave))

    def spectrogram_to_wave(self):
        self.soundwave = librosa.griffinlim(librosa.db_to_amplitude(self.spectrogram))

    def plot_spectrogram(self):
        plt.figure(figsize=(15, 7))
        librosa.display.specshow(self.spectrogram, sr=self.sampling_rate, x_axis='time', y_axis='hz')
        plt.colorbar()

    def plot_soundwave(self):
        plt.figure(figsize=(15, 3))
        librosa.display.waveshow(self.soundwave)

    def plot_spectrogram_from_file(self, path):
        self.load_sound_wave(path)
        self.wave_to_spec()
        self.plot_spectrogram()

    def plot_wave_from_file(self, path):
        self.load_sound_wave(path)
        self.plot_soundwave()

    def spectrogram_to_image(self, path=None):
        self.spectrogram_image_array = self.scaler.fit_transform(self.spectrogram).astype('uint8')
        self.spectrogram_image = Image.fromarray(self.spectrogram_image_array[::-1])
        if path:
            self.spectrogram_image.save(path)

    def image_to_spectrogram(self, inverse_transform=True):
        if inverse_transform:
            self.spectrogram = self.scaler.inverse_transform(self.spectrogram_image_array)
        else:
            self.spectrogram = self.spectrogram_image_array.astype('float') - 127

    def load_image(self, path, inverse=True, mode='L'):
        self.spectrogram_image = Image.open(path).convert(mode)
        self.spectrogram_image_array = np.array(self.spectrogram_image)[::-1 if inverse else 1]

    def load_image_form_array(self, array):
        self.spectrogram_image_array = array

    def play_sound(self, path=''):
        display(Audio(self.soundwave, rate=self.sampling_rate))
        if path:
            sf.write(path, self.soundwave, self.sampling_rate)

    def normalize_audio(self):
        self.soundwave = MinMaxScaler((-1, 1)).fit_transform(self.soundwave.reshape(-1,1)).ravel()

    def change_volume(self, volume=1.0):
        self.soundwave *= volume


class ImageProcessor:
    def __init__(self):
        self.image_array = None
        self.image = None

    def load_image(self, path, mode='L'):
        self.image = Image.open(path).convert(mode)
        self.image_array = np.array(self.image)

    def resize(self, max_length=1000):
        image_size = self.image.size
        ratio = max_length / max(image_size)
        self.image = self.image.resize((int(image_size[0] * ratio), int(image_size[1] * ratio)))

    def add_top_padding(self, pad=1):
        size = self.image.size
        self.image = ImageOps.pad(self.image, (size[0], int(size[1] * (1+pad))), centering=(0.5, 1))
        self.image = self.image.resize(size)

    def flip(self):
        self.image = ImageOps.flip(self.image)

    def rotate(self, angle):
        self.image = self.image.rotate(angle, expand=True)

    def inverse_color(self):
        self.image = ImageOps.invert(self.image)

    def image_to_array(self):
        self.image_array = np.array(self.image)
        return self.image_array

    def display_image(self, path=''):
        display(self.image)
        if path:
            self.image.save(path)