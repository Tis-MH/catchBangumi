class AppConfig:
    utility_database_uri = "120.78.140.25"
    utility_database_port = 6379
    utility_database_no = 0
    utility_database_passwd = "861238abcACBO"
    
    user_database_uri = "192.168.1.104"
    user_database_port = 6379
    user_database_no = 0
    user_database_passwd = "861238abcABCO"

    download_path = "E:/"


class TransmissionConfig:
    torrent_path = ""
    client_adress = "120.78.140.25"
    client_port = 9091
    user = "transmission"
    passwd = "861238abcABCO"
    # magnet:?xt=urn:btih:b8718cf5fe8da6390fedfc47eb2b8392a61998e6&tr=http://open.acgtracker.com:1096/announce

    tracker = "&tr=http://open.acgtracker.com:1096/announce"