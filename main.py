import DataPreprocessing
from MidiToWavConverter import MidiToWavConverter
from ModelTrainer import ModelTrainer
from MusicCreator import MusicCreator
from OnsetDetectionNet import OnsetDetectionNet
from TextFileParser import TextFileParser
from ModelEvaluator import ModelEvaluator  # Make sure to import your new class
from TextFileWriter import TextFileWriter



class MainClass:
    def __init__(self):
        # Initialize variables
        self.saveLocation = 'E:\PythonScript\Audioleaner'
        self.fileNumber = 0
        self.BPM = 120
        self.durationTimeMin = 0.75
        self.durationTimeMax = 1.25

    def create_midi(self):
        # This method creates a MIDI file using MusicCreator
        midi_path = MusicCreator.compose(self.saveLocation, self.fileNumber, self.BPM, self.durationTimeMin,
                                         self.durationTimeMax)
        print(f"MIDI created in: {midi_path}")
        return midi_path

    def convert_midi_to_wav(self, midi_path):
        # This method converts a MIDI file to a WAV file using MidiToWavConverter
        wav_converter = MidiToWavConverter()
        wav_path = wav_converter.convert(midi_path)
        print(f"Converted MIDI to WAV: {wav_path}")
        return wav_path



    def run(self):
        # Initialize your preprocessor
        preprocessor = DataPreprocessing.AudioPreprocessor(sample_rate=22050, duration=5, n_mfcc=64)

        # Initialize your model
        model = OnsetDetectionNet()

        # Initialize your data reader
        data_reader = TextFileParser()

        # Initialize your model trainer
        trainer = ModelTrainer(model, preprocessor, data_reader)

        for i in range(1):
            # Create a MIDI file and convert it to WAV
            midi_path = self.create_midi()
            wav_path = self.convert_midi_to_wav(midi_path)

            # Train your model
            trainer.train(audio_filepath=wav_path, data_filepath=self.saveLocation + f'/Audio{i}.txt') # replace 1 with i and audiot_filepath to wav_path

            self.fileNumber += 1  # Increment the file number so as not to overwrite the previous files
            print(f'Trained step number: {i}')

        # Save the model
        trainer.save_model(f"{self.saveLocation}/saved_model.pth")

        # Create a new MIDI file and convert it to WAV for testing
        test_midi_path = self.create_midi()
        test_wav_path = self.convert_midi_to_wav(test_midi_path)

        # Initialize your model evaluator
        evaluator = ModelEvaluator(model, preprocessor, data_reader)

        # Load the trained model into evaluator
        evaluator.load_model(f"{self.saveLocation}/saved_model.pth")

        # Evaluate your model
        evaluator.evaluate(audio_filepath=test_wav_path, data_filepath=self.saveLocation + f'/Audio{self.fileNumber}.txt')
        # audio_filepath=test_wav_path, data_filepath=self.saveLocation + f'/Audio{self.fileNumber}.txt'


if __name__ == '__main__':
    main_instance = MainClass()
    main_instance.run()
    #main_instance.run2()


