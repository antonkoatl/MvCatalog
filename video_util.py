import math
import ffmpeg
from file import CatFile


class VideoHelper():

    def __init__(self, fname):
        self.fname = fname
        self.frames = []
        probe = ffmpeg.probe(fname)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        audio_streams = (stream for stream in probe['streams'] if stream['codec_type'] == 'audio')
        sub_streams = (stream for stream in probe['streams'] if stream['codec_type'] == 'subtitle')

        self.file = CatFile()
        self.file.name = fname.split('/')[-1]
        self.file.path = '/'.join(fname.split('/')[:-1]) + '/'
        self.file.size = probe['format']['size']
        self.file.resolution = str(video_stream['width']) + 'x' + str(video_stream['height'])
        self.file.codec = video_stream['codec_name']
        self.file.bitrate = probe['format']['bit_rate']
        self.file.length = float(probe['format']['duration'])
        self.file.audio = ",".join([x['tags']['language'] if 'tags' in x and 'language' in x['tags'] else 'unknown' for x in audio_streams])
        self.file.subtitles = ",".join([x['tags']['language'] if 'tags' in x and 'language' in x['tags'] else 'unknown' for x in sub_streams])

        self.frame_count = math.floor(self.file.length * eval(video_stream['avg_frame_rate']))




    def get_frames(self, signal):
        N = 20
        for i in range(N):
            #frame = self.get_frame(math.floor(i * self.frame_count / N))
            frame = self._get_frame_time(math.floor(i * self.file.length / N))
            if frame is not None:
                self.frames.append(frame)
                signal.emit(i)
            else:
                return

    def get_frame(self, index, N):
        return self._get_frame_time(math.floor(index * self.file.length / N))

    def _get_frame_time(self, time):
        out, _ = (
            ffmpeg
                .input(self.fname, ss=time)
                .filter('scale', 240, -1)
                .output('pipe:', vframes=1, format='image2', vcodec='mjpeg')
                .run(capture_stdout=True)
        )

        return out

    def _get_frame(self, frame):
        out, _ = (
            ffmpeg
                .input(self.fname)
                .filter('select', 'gte(n,{})'.format(frame))
                .filter('scale', 240, -1)
                .output('pipe:', vframes=1, format='image2', vcodec='mjpeg')
                .run(capture_stdout=True)
        )

        return out

