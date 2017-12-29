import json
import os
import shutil


class YouTubeDownloader():
    # pip install pytube

    def __init__(self, out_dir="downloads"):
        self.out_dir = os.path.abspath(
            out_dir
        )
        if not os.path.exists(self.out_dir):
            os.mkdir(self.out_dir)

    def search_videos(self, search_query):
        import urllib.request
        import urllib.parse
        import re
        query_string = urllib.parse.urlencode({"search_query": search_query})
        html_content = urllib.request.urlopen("http://www.youtube.com/results?sp=EgQoATAB&" + query_string)
        search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
        # for result in search_results:
        #     print("http://www.youtube.com/watch?v=" + result)
        return search_results;

    def getClosedCaptions(self, video_id='vt-zXEsJ61U'):
        from xml.etree.ElementTree import fromstring
        import urllib.request
        content = urllib.request.urlopen("http://video.google.com/timedtext?lang=en&v=%s" % video_id)
        content = content.read().decode()
        content_list = []
        if content:
            for text in fromstring(content):
                content_list.append({'attr': text.attrib, 'text': text.text})
        return content_list

    def search(self, search_query='Connect your Bank Account and Buy Bitcoins'):
        video_ids = self.search_videos(search_query=search_query)
        search_result = {}

        for video_id in video_ids:
            content = self.getClosedCaptions(video_id)
            search_result[video_id] = content
        return search_result

    def extractClipDurations(self, search_result_filename='search-result.json',
                             search_query='Connect your Bank Account and Buy Bitcoins'):
        import time
        with open(search_result_filename) as result_file:
            result = json.load(result_file)
            query_keywords = search_query.split(' ')
            extracted_informtaion = {}
            for query_keyword in query_keywords:
                for res in result:
                    transcript = result[res]
                    if res not in extracted_informtaion:
                        extracted_informtaion[res] = []
                    for subscript in transcript:
                        if ('start' in subscript['attr'] and 'dur' in subscript['attr'] and query_keyword in subscript[
                            'text']):
                            text = subscript['text']
                            duration = float(subscript['attr']['dur'])
                            start = float(subscript['attr']['start'])
                            start_time = time.strftime("%H:%M:%S", time.gmtime(start))
                            end_time = time.strftime("%H:%M:%S", time.gmtime(start + duration))
                            extracted_informtaion[res].append(
                                {'start': start, 'duration': duration, 'text': text, 'start_time': start_time,
                                 'end_time': end_time})
                            break

            return extracted_informtaion

    def download_video(self, video_id='vt-zXEsJ61U', filename='vt-zXEsJ61U',
                       progress_change_callback=None,
                       complete_callback=None):
        from pytube import YouTube
        out_dir = os.path.abspath('%s/%s' % (self.out_dir, video_id))
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)

        def on_complete(stream, file_handle):
            curr_filename, file_extension = os.path.splitext(file_handle.name)
            parent_folder = os.path.abspath(os.path.join(file_handle.name, '..'))
            fn = os.path.abspath(os.path.join(parent_folder, filename))
            os.rename(file_handle.name, '%s%s' % (fn, file_extension))

        def on_progress(stream, chunk, file_handle, bytes_remaining):
            print("Left: %s KB" % (bytes_remaining / 1000.0,))

        yt = YouTube('http://youtube.com/watch?v=%s' % video_id)
        yt.register_on_progress_callback(progress_change_callback if progress_change_callback else on_progress)
        yt.register_on_complete_callback(complete_callback if complete_callback else on_complete)
        yt.streams.first().download(out_dir)

    def split_video(self, file_path='vt-zXEsJ61U/vt-zXEsJ61U-encoded.mp4',
                    out_dir="vt-zXEsJ61U/clips",
                    video_id="vt-zXEsJ61U",
                    extracted_subscripts='extracted-subscripts.json'):
        file_path = os.path.abspath(os.path.join(self.out_dir, file_path))
        out_dir = os.path.abspath(os.path.join(self.out_dir, out_dir))
        import subprocess
        with open(extracted_subscripts) as subscript_file:
            extracted_subscripts = json.load(subscript_file)
            subscript = extracted_subscripts[video_id]
            file_path = os.path.abspath(file_path)
            out_dir = os.path.abspath(out_dir)
            if not os.path.exists(out_dir):
                os.mkdir(out_dir)
            else:
                shutil.rmtree(out_dir)
                os.mkdir(out_dir)
            curr_filename, file_extension = os.path.splitext(file_path)
            i = 0
            for subs in subscript:
                out_file = os.path.join(out_dir, "%s-%s%s" % (video_id, str(i), file_extension))
                # print(" ".join(["/usr/bin/ffmpeg", "-i", str(file_path), '-ss', subs['start_time'], '-t', subs['end_time'], '-async', '1', str(out_file)]))
                subprocess.call(
                    ["/usr/bin/ffmpeg", "-i", str(file_path), '-ss', subs['start_time'], '-t', subs['end_time'],
                     '-async', '1', str(out_file)])
                i = i + 1
        return out_dir

    def encode_rescale_file(self, file_path='vt-zXEsJ61U/vt-zXEsJ61U.mp4',
                            encoded_file_path='vt-zXEsJ61U/vt-zXEsJ61U-encoded.mp4'):
        file_path = os.path.abspath(os.path.join(self.out_dir, file_path))
        encoded_file_path = os.path.abspath(os.path.join(self.out_dir, encoded_file_path))
        import subprocess
        subprocess.call(
            ["/usr/bin/ffmpeg", "-r", "30", "-i", str(file_path), "-vf", "scale=640:360", "-c:v", "libx264", "-crf",
             "18", "-preset", "medium", "-c:a", "copy", encoded_file_path])
        return encoded_file_path

    def merge_videos(self, src_dir='downloads/vt-zXEsJ61U/clips', out_dir='downloads/vt-zXEsJ61U/clips',
                     out_name='merged_video.mp4'):
        import os
        import glob
        import subprocess
        out_file_path = os.path.join(out_dir, out_name)
        list_file_path = os.path.abspath(os.path.join(src_dir, 'list.txt'))
        if os.path.exists(list_file_path):
            os.remove(list_file_path)
        file_list = glob.glob(os.path.abspath(os.path.join(src_dir, '*')))
        with open(list_file_path, 'w') as list_file:
            for f in file_list:
                list_file.write("file '%s'\n" % f)

        subprocess.call(
            ["/usr/bin/ffmpeg", "-f", "concat", "-safe", "0", "-i", "%s" % list_file_path, "-c", "copy", out_file_path])
        return out_file_path

    def select_video_id(self, extracted_info=[]):
        max_res = 0
        selected_id = None
        for video_id in extracted_info:
            if max_res < len(extracted_info[video_id]):
                max_res = len(extracted_info[video_id])
                selected_id = video_id
        return selected_id


if __name__ == '__main__':
    downloader = YouTubeDownloader()
    search_result = downloader.search()
    json.dump(search_result, open('search-result.json', 'w'), indent=4)
    extracted_info = downloader.extractClipDurations()
    json.dump(extracted_info, open('extracted-subscripts.json', 'w'), indent=4)
    downloader.download_video()
    downloader.encode_rescale_file()
    downloader.split_video()
    downloader.merge_videos()
