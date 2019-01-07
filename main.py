from multiprocessing import Pool
from mmspider_channel import channel_list
from mmspider_parase import get_page_from
def get_pages_from(channel):
    for i in range(1,100):
            get_page_from(channel,i)
 
if __name__ == '__main__':
    pool = Pool()
    # pool = Pool(processes=6)
    pool.map(get_pages_from,channel_list.split())
