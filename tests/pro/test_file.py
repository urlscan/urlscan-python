from io import BytesIO

from pytest_httpserver import HTTPServer

from urlscan.pro import Pro


def test_download(pro: Pro, httpserver: HTTPServer):
    file_hash = "foo"
    content = b"bar"
    httpserver.expect_request(f"/downloads/{file_hash}").respond_with_data(content)

    file = BytesIO()
    pro.download_file(file_hash=file_hash, file=file)

    assert file.getvalue() == content
