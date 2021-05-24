import transmissionrpc
from Config import TransmissionConfig



class Torrent:
    name: str
    hashString: str
    status: str

    def __init__(self, torrent):
        self.name = torrent.name
        self.hashString = torrent.hashString
        self.status = torrent.status
        self.id = torrent.id


class Transmission:
    client: transmissionrpc.Client
    torrent_list: list

    def __init__(self):
        self.client = transmissionrpc.Client(TransmissionConfig.client_adress, port=TransmissionConfig.client_port,
                                             user=TransmissionConfig.user,
                                             password=TransmissionConfig.passwd)

    def magnet_create(self, hash_id):
        # magnet:?xt=urn:btih:b8718cf5fe8da6390fedfc47eb2b8392a61998e6&tr=http://open.acgtracker.com:1096/announce
        head = "magnet:?xt=urn:btih:"
        tracker = TransmissionConfig.tracker
        return "{}{}{}".format(head, hash_id, tracker)

    def torrent_list(self):
        self.torrent_list = []
        for torrent in self.client.get_torrents():
            self.torrent_list.append(Torrent(torrent))

    def add_torrent(self, torrent_uri):
        if type(torrent_uri) != list:
            self.client.add_torrent(torrent_uri)
        else:
            for t in torrent_uri:
                self.client.add_torrent(t)

    def remove_torrents(self, torrent):
        if type(torrent) != list:
            self.client.stop_torrent(torrent.id)
            self.client.remove_torrent(torrent.hashString)
        else:
            for t in torrent:
                self.client.stop_torrent(t.id)
                self.client.remove_torrent(t.hashString)

    def search_torrent(self, bangumi_title: str):
        for torrent in self.client.get_torrents():
            if torrent.name == bangumi_title:
                return torrent

    def search_torrents_list(self, bangumi_title_list: list) -> list:
        torrents_list = self.client.get_torrents()
        result_list = []
        for title in bangumi_title_list:
            for torrent in torrents_list:
                if title == torrent.name:
                    result_list.append(torrent)
        return result_list




if __name__ == '__main__':
    a = Transmission()
    a.torrent_list()
    a.add_torrent('magnet:?xt=urn:btih:36e2f5578c3b7da315ed803493a6a19090c95e47&tr=http://open.acgtracker.com:1096/announce')
