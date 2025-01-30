# general Multiprocessing render script for VST instruments

import logging
import multiprocessing
import time
import traceback
from collections import namedtuple
from glob import glob
import os
from pathlib import Path

# extra libraries to install with pip
import dawdreamer as daw
from scipy.io import wavfile
from tqdm import tqdm


Item = namedtuple("Item", "preset_path")


class Worker:

    def __init__(self, queue: multiprocessing.Queue, plugin_path: str,
        sample_rate=44100, block_size=512, bpm=120, note_duration=2,
        render_duration=4, pitch_low=60, pitch_step=1, pitch_high=60, velocity=100,
        output_dir='output'):
        self.queue = queue
        self.sample_rate = sample_rate
        self.block_size = block_size
        self.bpm = bpm
        self.plugin_path = plugin_path
        self.note_duration = note_duration
        self.render_duration = render_duration
        self.pitch_low, self.pitch_step, self.pitch_high = pitch_low, pitch_step, pitch_high
        self.velocity = velocity
        self.output_dir = Path(output_dir)

    def startup(self):
        engine = daw.RenderEngine(self.sample_rate, self.block_size)
        engine.set_bpm(self.bpm)

        synth = engine.make_plugin_processor("synth", self.plugin_path)

        graph = [(synth, [])]
        engine.load_graph(graph)

        self.engine = engine
        self.synth = synth

    def process_item(self, item: Item):
        preset_path = item.preset_path
        self.synth.load_preset(preset_path)
        basename = os.path.basename(preset_path)
        basename_wo_ext = os.path.splitext(basename)[0]

        for pitch in range(self.pitch_low, self.pitch_high+1, self.pitch_step):
            self.synth.add_midi_note(pitch, self.velocity, 0.0, self.note_duration)
            self.engine.render(self.render_duration)
            self.synth.clear_midi()
            audio = self.engine.get_audio()
            output_path = self.output_dir / f'{basename_wo_ext}_C{int(pitch/12-1)}.wav'
            wavfile.write(str(output_path), self.sample_rate, audio.transpose())

    def run(self):
        try:
            self.startup()
            while True:
                try:
                    item = self.queue.get_nowait()
                    self.process_item(item)
                except multiprocessing.queues.Empty:
                    break
        except Exception as e:
            return traceback.format_exc()


def main(plugin_path, preset_dir, sample_rate=44100, bpm=120, note_duration=2,
    render_duration=4, pitch_low=60, pitch_step=1, pitch_high=60, num_workers=None,
    output_dir='output', logging_level='INFO'):

    # Create logger
    logging.basicConfig()
    logger = logging.getLogger('dawdreamer')
    logger.setLevel(logging_level.upper())

    # Glob all the preset file paths, looking shallowly only
    preset_paths = list(glob(str(Path(preset_dir) / '*.fxp')))

    # Get num items so that the progress bar works well
    num_items = len(preset_paths)

    # Create a Queue and add items
    input_queue = multiprocessing.Manager().Queue()
    for preset_path in preset_paths:
        input_queue.put(Item(preset_path))

    # Create a list to hold the worker processes
    workers = []

    # The number of workers to spawn
    num_processes = num_workers or multiprocessing.cpu_count()

    # Log info
    logger.info(f'Note duration: {note_duration}')
    logger.info(f'Render duration: {render_duration}')
    logger.info(f'Using num workers: {num_processes}')
    logger.info(f'Pitch low: {pitch_low}')
    logger.info(f'Pitch step: {pitch_step}')
    logger.info(f'Pitch high: {pitch_high}')
    logger.info(f'Output directory: {output_dir}')

    os.makedirs(output_dir, exist_ok=True)

    # Create a multiprocessing Pool
    with multiprocessing.Pool(processes=num_processes) as pool:
        # Create and start a worker process for each CPU
        for i in range(num_processes):
            worker = Worker(input_queue, plugin_path, sample_rate=sample_rate,
                bpm=bpm, note_duration=note_duration,
                render_duration=render_duration, pitch_low=pitch_low,
                pitch_step=pitch_step, pitch_high=pitch_high,
                output_dir=output_dir)
            async_result = pool.apply_async(worker.run)
            workers.append(async_result)

        # Use tqdm to track progress. Update the progress bar in each iteration.
        pbar = tqdm(total=num_items)
        while True:
            incomplete_count = sum(1 for w in workers if not w.ready())
            pbar.update(pbar.total - incomplete_count - pbar.n)
            if incomplete_count == 0:
                break
            time.sleep(0.1)
        pbar.close()

    # Check for exceptions in the worker processes
    for i, worker in enumerate(workers):
        exception = worker.get()
        if exception is not None:
            logger.error(f"Exception in worker {i}:\n{exception}")

    logger.info('All done!')

if __name__ == "__main__":
    # We're using multiprocessing.Pool, so our code MUST be inside __main__.
    # See https://docs.python.org/3/library/multiprocessing.html

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--plugin', required=True, type=str,
                        help="Path to plugin instrument (.dll, .vst3).")
    parser.add_argument('--preset-dir', required=True, type=str,
                        help="Directory path of plugin presets.")
    parser.add_argument('--sample-rate', default=44100, type=int,
                        help="Sample rate for the plugin.")
    parser.add_argument('--bpm', default=120, type=float,
                        help="Beats per minute for the Render Engine.")
    parser.add_argument('--note-duration', default=2, type=float,
                        help="Note duration in seconds.")
    parser.add_argument('--pitch-low', default=60, type=int,
                        help="Lowest MIDI pitch to be used (inclusive).")
    parser.add_argument('--pitch-step', default=1, type=int,
                        help="A step for difference between notes (inclusive).")
    parser.add_argument('--pitch-high', default=60, type=int,
                        help="Highest MIDI pitch to be used (inclusive).")
    parser.add_argument('--render-duration', default=4, type=float,
                        help="Render duration in seconds.")
    parser.add_argument('--num-workers', default=None, type=int,
                        help="Number of workers to use.")
    parser.add_argument('--output-dir', default=os.path.join(os.path.dirname(__file__),'output'),
                        help="Output directory.")
    parser.add_argument('--log-level', default='INFO',
                        choices=['DEBUG','INFO','WARNING','ERROR','CRITICAL', 'NOTSET'], help="Logger level.")
    args = parser.parse_args()

    main(args.plugin, args.preset_dir, args.sample_rate, args.bpm, args.note_duration,
        args.render_duration, args.pitch_low, args.pitch_step, args.pitch_high,
        args.num_workers, args.output_dir, args.log_level)
