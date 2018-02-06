import requests

url = "https://weibo.com/u/6448871601?from=myfollow_group&is_all=1"
cookies = {
    '_s_tentry': 'passport.weibo.com',
    'Apache': '10.13.240.39_1517922971.23858',
    'Apache': '1366268524968.7634.1517922959022',
    'SINAGLOBAL': '10.13.240.39_1517922971.23856',
    'SINAGLOBAL': '1366268524968.7634.1517922959022',
    'SUB': '_2AkMtJSWmf8NxqwJRmP4Uy2rnbo12wwHEieKbedR9JRMyHRl-yD9jqkYutRB6BqULQquRHIIefwp93PUiZ7P9HhLm_Zdd',
    'SUB': '_2AkMtJSWuf8NxqwJRmP4Uy2rnbo12wwHEieKbedR1JRMxHRl-yT9jqkYBtRB6BqULQRBn_ha6lRwVgXLxVx_ocoSUzogK',
    'SUBP': '0033WrSXqPxfM72-Ws9jqgMF55529P9D9WFP9iZ0I6qqIdQgTHCq3M5d',
    'SUBP': '0033WrSXqPxfM72-Ws9jqgMF55529P9D9WFP9iZ0I6qqIdQgTHCq3M5d',
    'TC-Page-G0': '9183dd4bc08eff0c7e422b0d2f4eeaec',
    'TC-V5-G0': '26e4f9c4bdd0eb9b061c93cca7474bf2',
    'ULV': '1517922959070:1:1:1:1366268524968.7634.1517922959022:',
    'wb_cusLike_3655689037': 'N'
}

r = requests.get(url, cookies=cookies)
print(r.text)