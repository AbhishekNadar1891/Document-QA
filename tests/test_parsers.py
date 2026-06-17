from app.services.parsers.txt_parser import parse_txt


def test_parse_txt_reads_utf8(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_content = "Hello world\nThis is a test."
    file_path.write_text(file_content, encoding="utf-8")

    result = parse_txt(str(file_path))

    assert result["content"] == file_content
    assert result["pages"][0]["page_number"] == 1
