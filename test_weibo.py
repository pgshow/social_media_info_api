import time

import requests

urls_str = """https://m.weibo.cn/status/4593014871955539
https://m.weibo.cn/status/4593016922705252
https://m.weibo.cn/status/4593028905836854
https://m.weibo.cn/status/4593039639317785
https://weibo.com/u/7292884462
https://m.weibo.cn/status/4593014472711172?
https://m.weibo.cn/7008775016/4593023374074781
https://m.weibo.cn/status/4593027493136766
https://m.weibo.cn/status/4593019468646350
https://m.weibo.cn/6943160712/4593139056902518
https://m.weibo.cn/status/4593052528939209?
https://m.weibo.cn/status/4593054231301820?
https://m.weibo.cn/status/4593051130933996?
https://m.weibo.cn/status/4593139707019293?
https://m.weibo.cn/status/4593142945284508?
https://m.weibo.cn/1582795727/4650638497024819
https://m.weibo.cn/6165567138/4650624006752426
https://m.weibo.cn/3281516321/4650619703660931
https://m.weibo.cn/2389985477/4650622341612193
https://m.weibo.cn/1715651433/4650620692469710
https://m.weibo.cn/5088605672/4650870949549692
https://m.weibo.cn/5910826744/4650622382769147
https://m.weibo.cn/2789359582/4650627626434908
https://m.weibo.cn/7626635656/4650624954407433
https://m.weibo.cn/6691258663/4650868018777564
https://m.weibo.cn/1653608561/4650641287546002
https://m.weibo.cn/2514125871/4650646306818921
https://m.weibo.cn/6483279103/4650631552570030
https://m.weibo.cn/status/4650857565519964?wm=3333_2001&from=10B6193010&sourcetype=weixin
https://m.weibo.cn/1749310241/4650626527269434
https://m.weibo.cn/6476850420/4650642566285238
https://m.weibo.cn/5687908297/4650659351892219
https://m.weibo.cn/6395821577/4650626137457083
https://m.weibo.cn/6410050838/4650628225961927
https://m.weibo.cn/1798970407/4650867330910469
https://m.weibo.cn/5066086702/4650626716271419
https://m.weibo.cn/1769995792/4650628187948940
https://m.weibo.cn/5703356514/4650861727319388
https://m.weibo.cn/6825898605/4650865510842456
https://m.weibo.cn/3957386360/4650864993898482
https://m.weibo.cn/5221480640/4650861953814895
https://m.weibo.cn/2712036683/4650871453650545
https://m.weibo.cn/3598241987/4650867674580373
https://m.weibo.cn/1864576941/4650873944281459
https://m.weibo.cn/3629496390/4650865505343013
https://m.weibo.cn/2815344953/4670898201957632
https://m.weibo.cn/5621475699/4671202968213457
https://m.weibo.cn/6173051977/4670864006841045
https://m.weibo.cn/6371787489/4671207314036359
https://m.weibo.cn/3263897702/4671209016659935
https://m.weibo.cn/1960490957/4670900076548245
https://m.weibo.cn/1989077937/4670869563770614
https://m.weibo.cn/1575159824/4670874114065455
https://m.weibo.cn/3719906947/4671170727118941
https://m.weibo.cn/2171553864/4670859187324722
https://m.weibo.cn/status/4671537477320851
https://m.weibo.cn/2389985477/4671528743998724
https://m.weibo.cn/status/4671233117129062
https://m.weibo.cn/7261158770/4671527910114393
https://m.weibo.cn/6969984973/4671220514292122
https://m.weibo.cn/2239169850/4671217317187554
https://m.weibo.cn/6456123738/4671217103017909
https://m.weibo.cn/6348891761/4671275420884494
https://m.weibo.cn/7490715133/4671533731546982
https://m.weibo.cn/2438844840/4671571827885084
https://m.weibo.cn/2020275241/4671982292174129
https://m.weibo.cn/1773880997/4672630332851807
https://m.weibo.cn/6165567138/4672605788048043
https://m.weibo.cn/7566019786/4672892229388094
https://m.weibo.cn/5625044461/4672610027962883
https://m.weibo.cn/2804597314/4672684456152256
https://m.weibo.cn/3125633141/4672605233090217
https://m.weibo.cn/7013510140/4672600091134809
https://m.weibo.cn/5686962495/4673074816091232
https://m.weibo.cn/2052467021/4672990338094155
https://m.weibo.cn/6098749893/4672717901005528
https://m.weibo.cn/7619058581/4672686301382267
https://m.weibo.cn/6424484884/4672618659843127
https://m.weibo.cn/3605248243/4672983278291596
https://m.weibo.cn/1733142631/4673313219285383
https://m.weibo.cn/5420360920/4673313907409723
https://m.weibo.cn/6174425061/4673335366259626
https://m.weibo.cn/2178956813/4673374612101257
https://m.weibo.cn/2416286294/4673312665636001
https://m.weibo.cn/6508150349/4673348087058937
https://m.weibo.cn/7315132546/4673092393900279
https://m.weibo.cn/6336805897/4673330077239215
https://m.weibo.cn/5634702583/4673702434964602
https://m.weibo.cn/detail/4673682045405372
https://m.weibo.cn/status/4673666837119554?sourceType=weixin&from=10B8295060&wm=9006_2001&featurecode=newtitle
https://m.weibo.cn/2246767252/4673736928136559
https://m.weibo.cn/7549821592/4673681362780579
https://m.weibo.cn/1860079433/4673710944160872
https://m.weibo.cn/3896692979/4673675309090058
https://m.weibo.cn/2400894383/4673744645134006
https://m.weibo.cn/status/4673752652582820?wm=3333_2001&from=10B8293010&sourcetype=weixin
https://m.weibo.cn/status/4673753927125257?wm=3333_2001&from=10B8293010&sourcetype=weixin
https://m.weibo.cn/status/4673753922932475
https://m.weibo.cn/status/4673756847146035
https://m.weibo.cn/7626711478/4670825338242329
https://m.weibo.cn/3795954563/4670852253614909
https://m.weibo.cn/2287130690/4671923205970810
https://m.weibo.cn/3187242554/4671906910837497
https://m.weibo.cn/1768552065/4673649574153566
https://m.weibo.cn/1167121691/4671972921839733
https://m.weibo.cn/6317929923/4671849064040538
https://m.weibo.cn/2531950933/4671504816541577
https://m.weibo.cn/2033519391/4674879239228435
https://m.weibo.cn/2957087017/4675825817355434
"""

if __name__ == '__main__':
    urls = urls_str.split('\n')
    for url in urls:
        try:
            print('access', url)
            post_data = {
                'url': url,
                'platform': 'weibo'
            }
            r = requests.post('http://localhost:5000/api', data=post_data, timeout=60)
            print(r.status_code, r.text)

        except Exception as e:
            print(e)
        finally:
            time.sleep(22)
