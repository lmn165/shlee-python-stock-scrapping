from urllib import parse

import urllib3

if __name__ == '__main__':
    q = '앤비디아'
    # q_enc = urllib.parse.unquote('%BE%D8%BA%F1%B5%F0%BE%C6')
    q_enc = parse.unquote('%BE%D8%BA%F1%B5%F0%BE%C6')
    print(q_enc)

    # %BE%D8%BA%F1%B5%F0%BE%C6
    # %EC%95%A4%EB%B9%84%EB%94%94%EC%95%84
    # %EC%95%A4%EB%B9%84%EB%94%94%EC%95%84