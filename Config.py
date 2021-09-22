class AppConfig:
    utility_database_uri = "120.78.140.25"
    utility_database_port = 6379
    utility_database_no = 0
    utility_database_passwd = "861238abcACBO"

    user_database_uri = "192.168.3.230"
    user_database_port = 6379
    user_database_no = 0
    user_database_passwd = "861238abcABCO"

    download_path = "E:/"

    scrapyrt_ip = "192.168.3.230"



class TransmissionConfig:
    torrent_path = ""
    client_adress = "192.168.3.204" #  "120.78.140.25"
    client_port = 9091
    user = "transmission"
    passwd = "861238abcABCO"
    # magnet:?xt=urn:btih:b8718cf5fe8da6390fedfc47eb2b8392a61998e6&tr=http://open.acgtracker.com:1096/announce
    tracker = "&tr=http://open.acgtracker.com:1096/announce"


class RequestConfig:
    proxy = {"https": "socks5h://127.0.0.1:7890", "http": "socks5h://127.0.0.1:7890"}
    UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.57 ' \
         'Safari/537.36 Edg/91.0.864.27 '
