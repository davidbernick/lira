#!/usr/bin/env python

import io
import requests
import zipfile
from StringIO import StringIO


def download_to_map(urls):
    """
    Reads contents from each url into memory and returns a
    map of urls to their contents
    """
    url_to_contents = {}
    for url in urls:
        contents = download(url)
        url_to_contents[url] = contents
    return url_to_contents


def make_zip(url_to_contents):
    """
    Given a map of urls and their contents, returns an in-memory zip file
    containing each file. For each url, the part after the last slash is used
    as the file name when writing to the zip archive.
    """
    buf = StringIO()
    with zipfile.ZipFile(buf, 'w') as zip_buffer:
        for url, contents in url_to_contents.items():
            name = url.split('/')[-1]
            zip_buffer.writestr(name, contents)
    return buf


def download(url):
    """
    Reads the contents located at the url into memory and returns them.
    Urls starting with http are fetched with an http request. All others are
    assumed to be local file paths and read from the local file system.
    """
    if url.startswith('http'):
        return download_http(url)
    else:
        return read_local_file(url)


def download_http(url):
    """
    Makes an http request for the contents at the given url and returns the response body.
    """
    response = requests.get(url)
    response_str = response.text.encode('utf-8')
    return response_str


def read_local_file(path):
    """
    Reads the file contents and returns them.
    """
    with open(path) as f:
        contents = f.read()
    return contents


if __name__ == '__main__':
    #analysis_url = 'https://raw.githubusercontent.com/HumanCellAtlas/skylab/master/smartseq2_single_sample/ss2_single_sample.wdl'
    analysis_url = '../../skylab/smartseq2_single_sample/ss2_single_sample.wdl'
    #submit_url = 'https://raw.githubusercontent.com/HumanCellAtlas/pipeline-tools/ds_move_wrapper_wdls_310/adapter_pipelines/submit.wdl'
    submit_url = '../../pipeline-tools/adapter_pipelines/submit.wdl'
    urls = [analysis_url, submit_url]
    url_to_contents = download_to_map(urls)
    buf = make_zip(url_to_contents)
    with open('temp_zip/test.zip', 'wb') as zf:
        zf.write(buf.getvalue())

