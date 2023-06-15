import tkinter as tk
from tkinter import filedialog
import sounddevice as sd
import soundfile as sf
from speechbrain.pretrained import SpeakerRecognition


class SpeakerVerificationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Speaker Verification App")

        self.audio_path_1 = ""
        self.audio_path_2 = ""

        self.create_widgets()

    def create_widgets(self):
        # Audio File 1 Selection
        audio_label_1 = tk.Label(self.root, text="Select Audio File 1:")
        audio_label_1.pack()
        audio_button_1 = tk.Button(self.root, text="Browse", command=self.select_audio_1)
        audio_button_1.pack()

        # Audio File 2 Selection
        audio_label_2 = tk.Label(self.root, text="Select Audio File 2:")
        audio_label_2.pack()
        audio_button_2 = tk.Button(self.root, text="Browse", command=self.select_audio_2)
        audio_button_2.pack()

        # Speaker Verification Button
        verify_button = tk.Button(self.root, text="Verify Speakers", command=self.verify_speakers)
        verify_button.pack()

        # Recording Button
        record_button = tk.Button(self.root, text="Record Audio", command=self.record_audio)
        record_button.pack()

    def select_audio_1(self):
        self.audio_path_1 = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav")])

    def select_audio_2(self):
        self.audio_path_2 = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav")])

    def verify_speakers(self):
        if self.audio_path_1 and self.audio_path_2:
            verification = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb",
                                                          savedir="pretrained_models/spkrec-ecapa-voxceleb")
            score, prediction = verification.verify_files(self.audio_path_1, self.audio_path_2)
            print("Score:", score)
            print("Prediction:", prediction)
        else:
            print("Please select both audio files.")

    def record_audio(self):
        duration = 10  # Duration in seconds
        sample_rate = 16000  # Sample rate in Hz

        # Record audio
        print("Recording started...")
        recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
        sd.wait()  # Wait until recording is finished
        print("Recording finished.")

        # Save the recording as a WAV file
        output_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV Files", "*.wav")])
        sf.write(output_path, recording, sample_rate)

        print("Recording saved as", output_path)


if __name__ == "__main__":
    root = tk.Tk()
    app = SpeakerVerificationApp(root)
    root.mainloop()
