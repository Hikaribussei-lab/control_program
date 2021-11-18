from wos import WosClient
import wos.utils

with WosClient('JohnDoe', '12345') as client:
    print(wos.utils.query(client, 'AU=Knuth Donald'))