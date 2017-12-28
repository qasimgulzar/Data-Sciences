import json


class YouTubeDownloader():
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
                            extracted_informtaion[res].append({'start': start, 'duration': duration, 'text': text})
            return extracted_informtaion


if __name__ == '__main__':
    downloader = YouTubeDownloader()
    # search_result = downloader.search()
    # json.dump(search_result, open('search-result.json', 'w'),indent=4)
    extracted_info = downloader.extractClipDurations()
    json.dump(extracted_info, open('extracted-subscripts.json', 'w'), indent=4)
