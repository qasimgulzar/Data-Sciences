import json
import os


class YouTubeDownloader():
    # pip install pytube

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
            content = downloader.getClosedCaptions(video_id)
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
            return extracted_informtaion

    def download_video(self, video_id='vt-zXEsJ61U', filename='vt-zXEsJ61U', out_dir='downloads',
                       progress_change_callback=None,
                       complete_callback=None):
        from pytube import YouTube
        out_dir = os.path.abspath('%s/%s' % (out_dir, video_id))
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

    def split_video(self, file_path='downloads/vt-zXEsJ61U/vt-zXEsJ61U.mp4', out_dir="downloads/vt-zXEsJ61U/clips",
                    video_id="vt-zXEsJ61U",
                    extracted_subscripts='extracted-subscripts.json'):
        import subprocess
        with open(extracted_subscripts) as subscript_file:
            extracted_subscripts = json.load(subscript_file)
            subscript = extracted_subscripts[video_id]
            file_path = os.path.abspath(file_path)
            out_dir = os.path.abspath(out_dir)
            if not os.path.exists(out_dir):
                os.mkdir(out_dir)
            curr_filename, file_extension = os.path.splitext(file_path)
            i = 0
            for subs in subscript:
                out_file = os.path.join(out_dir, "%s-%s%s" % (video_id, str(i),file_extension))
                # print(" ".join(["/usr/bin/ffmpeg", "-i", str(file_path), '-ss', subs['start_time'], '-t', subs['end_time'], '-async', '1', str(out_file)]))
                subprocess.call(["/usr/bin/ffmpeg", "-i", str(file_path), '-ss', subs['start_time'], '-t', subs['end_time'], '-async', '1', str(out_file)])
                i = i + 1


if __name__ == '__main__':
    downloader = YouTubeDownloader()
    # search_result = downloader.search()
    # json.dump(search_result, open('search-result.json', 'w'),indent=4)
    # extracted_info = downloader.extractClipDurations()
    # json.dump(extracted_info, open('extracted-subscripts.json', 'w'), indent=4)
    # downloader.download_video()
    downloader.split_video()
