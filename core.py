import os
import re
import sys
import traceback
import types

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QSettings, QRunnable, QThreadPool
from PyQt5.QtWidgets import QApplication
from bs4 import BeautifulSoup

from dbhelper import *
from file import CatFile
from movie import CatMovie
from video_util import VideoHelper
from kinopoisk.movie import Movie
import urllib.request


class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(bytes, int)
    progress = pyqtSignal(int)


class PosterWorker(QRunnable):

    def __init__(self, id, *args, **kwargs):
        super(PosterWorker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.id = id
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            item = Movie(id=self.id)
            image = None

            item.get_content('posters')
            url = item.posters[0] if len(item.posters) > 0 else None
            if url:
                req = urllib.request.urlopen(url, timeout=3)
                if not url[7:] in req.geturl():
                    image = b''
                else:
                    image = req.read()
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            #self.signals.error.emit((exctype, value, traceback.format_exc()))
            self.signals.result.emit(b'', self.id)
        else:
            self.signals.result.emit(image, self.id)  # Return the result of the processing
        finally:
            self.signals.finished.emit()


class CoreWorker(QObject):
    DEBUG = False

    signal_add_items_to_list = pyqtSignal(list)
    signal_fill_items_to_list = pyqtSignal(list)
    signal_update_db_result = pyqtSignal(str)
    signal_send_file_to_editdialog = pyqtSignal(CatFile)
    signal_send_movie_to_editdialog = pyqtSignal(list)
    signal_send_frames_to_editdialog = pyqtSignal(list)
    signal_update_progress_bar = pyqtSignal(int)
    signal_send_open_db_result = pyqtSignal(int)
    signal_update_poster_label = pyqtSignal(bytes)
    signal_movie_search_result = pyqtSignal(list)
    signal_start_parser = pyqtSignal()
    signal_parse_poster = pyqtSignal(int)
    signal_set_loading = pyqtSignal(str, bool)
    signal_show_filesdialog = pyqtSignal()
    signal_send_file_to_filesdialog = pyqtSignal(str)

    settings = QSettings("data/settings.ini", QSettings.IniFormat)

    breaker_parse_video = False
    movie_search_name = None
    poster_waiting_id = None

    movie_search_cache = {}
    movie_data_cache = {}

    def __init__(self):
        QObject.__init__(self)
        self.db_helper = DBHelper()
        self.signal_start_parser.connect(self.kinopoisk_parser)
        self.signal_parse_poster.connect(self.kinopoisk_poster_parser)

    def __del__(self):
        self.wait()

    @pyqtSlot(str)
    def request_list_data(self, command):
        self.debug('request_list_data', command)
        if command == 'start_list':
            db_data = self.db_helper.get_list_data(True)
            list_data = [[CatMovie(item), CatFile(item)] if item is not None else None for item in db_data]
            self.signal_fill_items_to_list.emit(list_data)
            return

        if command == 'add_list':
            db_data = self.db_helper.get_list_data()
            list_data = [[CatMovie(item), CatFile(item)] if item is not None else None for item in db_data]
            self.signal_add_items_to_list.emit(list_data)
            return

    @pyqtSlot(CatMovie, CatFile)
    def update_db(self, movie: CatMovie, file: CatFile):
        id, error = self.db_helper.update_movie(movie)

        if error is not None:
            self.signal_update_db_result.emit(error)
            return

        if file.movie_id == -1:
            file.movie_id = id

        error = self.db_helper.update_file(file)
        if error is not None:
            self.signal_update_db_result.emit(error)
            return

        self.request_list_data('start_list')
        self.signal_update_db_result.emit(None)

    @pyqtSlot(CatFile)
    def removefrom_db(self, file):
        self.db_helper.remove_file(file)

    @pyqtSlot(str)
    def parse_video_file(self, fname):
        self.breaker_parse_video = False
        video = VideoHelper(fname)
        self.signal_send_file_to_editdialog.emit(video.file)

        N = 20
        for i in range(N):
            frame = video.get_frame(i, N)

            QApplication.processEvents()

            if self.breaker_parse_video:
                self.breaker_parse_video = not self.breaker_parse_video
                return

            if frame is not None:
                video.frames.append(frame)
                self.signal_update_progress_bar.emit(i)

        self.signal_send_frames_to_editdialog.emit(video.frames)
        self.breaker_parse_video = True

    @pyqtSlot(str)
    def new_db(self, fname):
        self.db_helper.conn = None

        if Path(fname).is_file():
            os.remove(fname)

        if self.db_helper.create_db(fname):
            self.settings.setValue("last_db", fname)
            self.request_list_data('start_list')
        else:
            pass

    @pyqtSlot(str)
    def open_db(self, fname):
        if fname != "":
            self.db_helper.db_file = fname

        if not Path(self.db_helper.db_file).is_file():
            return False

        self.db_helper.conn = None

        if self.db_helper.create_connection():
            # self.db_helper.fill_test_data()
            self.settings.setValue("last_db", self.db_helper.db_file)
            self.signal_send_open_db_result.emit(1)
        else:
            self.signal_send_open_db_result.emit(0)

    @pyqtSlot(str)
    def load_poster(self, fname):
        if self.poster_waiting_id is not None:
            self.poster_waiting_id = None
            self.signal_set_loading.emit('poster', False)

        if fname:
            with open(fname, mode='rb') as f:
                image_binary = f.read()

                self.signal_update_poster_label.emit(image_binary)
        else:
            self.signal_update_poster_label.emit(b'')

    @pyqtSlot(str)
    def set_breaker(self, name):
        if name == 'edit_dialog':
            self.breaker_parse_video = True
            self.search_movie_name = None
            self.poster_waiting_id = None

    @pyqtSlot(str)
    def search_movie_name(self, name):
        self.debug('search_movie_name', name)

        if name:
            result = self.db_helper.search_movie_by_name(name)
            self.signal_movie_search_result.emit(['db',] + result)

            self.movie_search_name = name
            self.signal_start_parser.emit()

    @pyqtSlot(int)
    def get_movie_data_from_kinopoisk(self, id):
        self.debug('get_movie_data_from_kinopoisk', id)

        movie = None
        if id in self.movie_data_cache:
            movie = self.movie_data_cache[id]
        else:
            item = Movie(id=id)

            def replace_get(self):
                if self.instance.id:
                    self.content = self.request.get_content(self.instance.get_url(self.source_name))
                    self._content = self.content
                    self.parse()

            def replace_get_content(self, name):
                self._instance = self.get_source_instance(name, instance=self)
                self._instance.get = types.MethodType(replace_get, self._instance)
                self._instance.get()

            item.get_content = types.MethodType(replace_get_content, item)
            item.get_content('main_page')

            movie = [None, item.title, item.title_en, item.year, ','.join(item.countries), ','.join(item.genres), item.runtime if isinstance(item.runtime, int) else 0, '',
                           ', '.join([person.name_en if len(person.name_en) > 0 else person.name for person in item.directors]),
                           ', '.join([person.name_en if len(person.name_en) > 0 else person.name for person in item.screenwriters]),
                           ', '.join([person.name_en if len(person.name_en) > 0 else person.name for person in item.actors]),
                           item.plot, self.posters[0] if len(item.posters) > 0 else None]

            content_info = BeautifulSoup(item._instance._content, 'html.parser')
            table_info = content_info.find('table', {'class': re.compile(r'^info')})
            if table_info:
                for tr in table_info.findAll('tr'):
                    tds = tr.findAll('td')
                    name = tds[0].text

                    if name == 'рейтинг MPAA':
                        movie[7] = tds[1].attrs['class'][0]
                        break

            self.movie_data_cache[id] = movie

        self.signal_send_movie_to_editdialog.emit(movie)
        self.signal_set_loading.emit('movie', False)

        if movie[12] is None:
            self.poster_waiting_id = id
            self.signal_parse_poster.emit(id)
        else:
            self.set_poster_waiting_id(-1)

    @pyqtSlot()
    def kinopoisk_parser(self):
        self.debug('kinopoisk_parser', self.movie_search_name)
        import time
        time.sleep(0.5)

        QApplication.processEvents()
        if self.movie_search_name is not None:

            if self.movie_search_name in self.movie_search_cache:
                result = self.movie_data_cache[self.movie_search_name]
            else:
                movie_list = Movie.objects.search(self.movie_search_name)
                result = [[None, item.title, item.title_en, item.year, ','.join(item.countries), ','.join(item.genres),
                           item.runtime if isinstance(item.runtime, int) else 0, '',
                           ','.join([person.name_en if len(person.name_en) > 0 else person.name for person in item.directors]),
                           ','.join([person.name_en if len(person.name_en) > 0 else person.name for person in item.screenwriters]),
                           ','.join([person.name_en if len(person.name_en) > 0 else person.name for person in item.actors]),
                           item.plot, self.posters[0] if len(item.posters) > 0 else None, item.id]
                          for item in movie_list]

            QApplication.processEvents()
            if self.movie_search_name is not None:
                self.signal_movie_search_result.emit(['kinopoisk',] + result)
            self.movie_search_name = None

    @pyqtSlot(int)
    def set_poster_waiting_id(self, id):
        self.poster_waiting_id = id

    @pyqtSlot(int)
    def kinopoisk_poster_parser(self, id):
        self.debug('kinopoisk_poster_parser', id)

        movie = None
        if id in self.movie_data_cache:
            movie = self.movie_data_cache[id]

            if movie[12] is None:
                self.signal_set_loading.emit('poster', True)

                worker = PosterWorker(id)
                worker.signals.result.connect(self.poster_result)
                QThreadPool.globalInstance().start(worker)

            else:
                if self.poster_waiting_id is not None:
                    self.signal_send_movie_to_editdialog.emit(movie)

    @pyqtSlot(bytes, int)
    def poster_result(self, image, id):
        self.debug('poster_result')

        QApplication.processEvents()
        if self.poster_waiting_id == id:
            movie = self.movie_data_cache[id]
            movie[12] = image
            self.signal_set_loading.emit('poster', False)
            self.signal_send_movie_to_editdialog.emit(movie)

    @pyqtSlot(str)
    def scan_dir(self, dir_):
        from os import listdir
        from os.path import isfile, join, normpath

        video_files = [dir_ + '/' + f for f in listdir(dir_) if
                       isfile(join(dir_, f)) and f.split('.')[-1] in ['avi', 'mkv', 'mp4']]

        if len(video_files) == 0:
            return

        self.signal_show_filesdialog.emit()

        accepted_files = []
        #self.files_dialog.prepare(video_files)
        #if self.files_dialog.exec_():
        #    for i in range(self.files_dialog.listWidget.count()):
        #        item = self.files_dialog.listWidget.item(i)
        #        if item.checkState():
        #            accepted_files.append(item.data(Qt.UserRole))
        for f in video_files:
            files = self.db_helper.search_file(f.split('/')[-1], '/'.join(f.split('/')[:-1]))

            if len(files) == 0:
                self.signal_send_file_to_filesdialog.emit(f)

    def debug(self, *args):
        if self.DEBUG:
            with open('log_core.txt', 'a+') as f:
                print(*args, file=f)
