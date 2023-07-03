from multiprocessing import Process, Queue

from AudioRecorder.Processor import Processor
from AudioRecorder.Recorder import Recorder

if __name__ == "__main__":
    # Create a queue
    queue = Queue()

    # Create and start the recorder process
    recorder = Recorder(queue)
    recorder_process = Process(target=recorder.record_and_send)
    recorder_process.start()

    # Create and start the processor process
    processor = Processor(queue)
    processor_process = Process(target=processor.process)
    processor_process.start()
