from enum import Enum
from web_scraping import WebScraping
from dynamodb import get_item_to_dynamodb, init_dynamodb, put_item_to_daynamodb
import pandas as pd
from slack import Slack
from dotenv import load_dotenv
# from utils import check_english
# from translator import translate

# TODO：CSVとか外部ファイルでデータを持つようにする
# 「会社名、スクレイピング対象のURL、スクレイピング対象のHTMLクラス名
url_list = [
    ["東京海上ホールディングス", "https://www.tokiomarinehd.com/ir", "list-news-01"],
    ["稲畑産業", "https://www.inabata.co.jp/investor", "irGroup new-info -large"],
    ["資生堂", "https://corp.shiseido.com/jp/news/", "p-resultList mb-m"],
    ["日本電気硝子", "https://www.neg.co.jp/ir", "irIndexLatestNews__content"],
    ["イビデン", "https://www.ibiden.co.jp/ir", "news_items has_bg_blue"],
    ["デクセリアルズ", "https://www.dexerials.jp/ir", "eirGroup colLinks_ir"],
    ["銀座ルノアール", "https://www.ginza-renoir.co.jp/ir/", "irGroup"],
    ["帝国ホテル", "https://www.imperialhotel.co.jp/j/company/release/2022/index.html", "short"],
    ["アルファポリス", "https://www.alphapolis.co.jp/company/ir", "timeline"],
    ["レーザーテック", "https://www.lasertec.co.jp/ir/", "eirGroup s_eirList"],
    ["ベイカレント", "https://www.baycurrent.co.jp/ir/", "s_eirList"],
    ["塩野義製薬", "https://www.shionogi.com/jp/ja/investors.html", "mod-news-top__content"],
    ["ブリヂストン", "https://www.bridgestone.co.jp/ir/",
        "ir_tabContentList js-newsList typesquare_tags"],
    ["住友金属鉱山", "https://www.smm.co.jp/ir/", "c-news"],

    ["ダイキン工業", "https://www.daikin.co.jp/investor", "g-pile"],
    ["村田製作所", "https://corporate.murata.com/ja-jp/newsroom", "c-news__items"],
    ["ソニーグループ", "https://www.sony.com/ja/SonyInfo/IR/",
        "com_newslist com_newslist_IRnews fSize85 anker_g"],
    ["東京エレクトロン", "https://www.tel.co.jp/ir/", "tpl-news-list__list"],
    ["ファナック", "https://www.fanuc.co.jp/", "update-box"],
    ["伊藤忠商事", "https://www.itochu.co.jp/ja/ir/index.html", "releaseWrap01"],
    ["三井物産", "https://www.mitsui.com/jp/ja/ir/index.html", "js-moduleAccordion2Items"],
    ["三菱商事", "https://www.mitsubishicorp.com/jp/ja/ir/", "latestInfo-list"],
    ["三越伊勢丹ホールディングス", "https://www.imhds.co.jp/ja/ir/index.html", "imhds-list-news"],
    ["三井住友フィナンシャルグループ", "https://www.smfg.co.jp/investor/", "c-info_list"],
    ["三菱UFJフィナンシャルグループ", "https://www.mufg.jp/ir/index.html", "m-list-dl-wide"],
    ["SOMPOホールディングス", "https://www.sompo-hd.com/ir/", "news-list"],
    ["MS&ADホールディングス", "https://www.ms-ad-hd.com/ja/ir.html", "tabItems"],
    ["三井不動産", "https://www.mitsuifudosan.co.jp/corporate/news/2022/",
        "p-news-release-list"],
    ["商船三井", "https://www.mol.co.jp/ir/", "newslist pad20b"],
    ["日本郵船", "https://www.nyk.com/ir/", "news-layout js-news-ir js-shiftAfter"],
    ["任天堂", "https://www.nintendo.co.jp/ir/index.html", "corp_ir_2018-newsDateList"],
    ["花王", "https://www.kao.com/jp/corporate/investor-relations/",
        "g-NewsIndexP--v2__list l-NewsIndexP--v2__list"],
    ["第一三共", "https://www.daiichisankyo.co.jp/investors/", "newsList"],

    ["Amazon", "https://ir.aboutamazon.com/overview/default.aspx",
        "ContentPaneDiv2"]

    # ["第一生命ホールディングス", "https://www.dai-ichi-life-hd.com/investor/index.html", "listInfo04"],
    # ["三菱重工業", "https://www.mhi.com/jp/finance", "comDayLi"],
    # ["信越化学工業", "https://www.shinetsu.co.jp/jp/", "news-wrapp"],
    # ["アートスパークホールディングス", "https://www.artspark.co.jp/news/ir", "clearfix"],
    # ["新光電気工業", "https://www.shinko.co.jp", "", "div.content > div"],
    # ["共立メンテナンス", "https://www.kyoritsugroup.co.jp/", "current first"],
    # ["コメダホールディングス", "https://www.komeda-holdings.co.jp/", "divDataArea"],
    # ["モロゾフ", "https://www.morozoff.co.jp/", "newsBox_cnt productAndTopics"],
    # ["モロゾフ", "https://www.morozoff.co.jp/", "newsBox_cnt"],
    # ["アフタヌーンティーサイト", "https://prtimes.jp/topics/keywords/%E3%82%A2%E3%83%95%E3%82%BF%E3%83%8C%E3%83%BC%E3%83%B3%E3%83%86%E3%82%A3%E3%83%BC", "container-thumbnail-list"]
]


class IRState(Enum):
    updated = 1
    not_updated = 2
    new_company = 3


def check_updated_IR(new_company_name, new_body):
    company_name = new_company_name
    body = new_body

    item = get_item_to_dynamodb(dynamodb, company_name)

    # print(f"{company_name}_{body}")

    if item:
        item_body = item["body"]
        if not item_body == body:
            print(f"{company_name}：IRが更新されました。\n")
            print(f"DB：{item_body}")
            print(f"スクレイピング：{body}")
            return IRState.updated
        else:
            print(f"{company_name}：IRは更新されていません")
            return IRState.not_updated

    else:
        print(f"{company_name}：IRが更新されました。{body}")
        return IRState.new_company


if __name__ == '__main__':
    print("スクレイピングを開始します")
    load_dotenv(verbose=True)
    dynamodb = init_dynamodb()
    web_scraping = WebScraping()
    slack = Slack()

    old = ""

    # スクレイピングしたデータをデータフレームに書き込んでいく
    df = pd.DataFrame(columns=["company_name", "date", "body", "link"])

    for url in url_list:
        scraping_data = web_scraping.get_ir_info(url[0], url[1], url[2])
        df_new = pd.DataFrame(scraping_data, columns=[
            "company_name", "date", "body", "link"])
        df = pd.concat([df, df_new])

        is_update = False
        idx = 0

        for data in range(len(df_new)):
            company_name = df_new.iloc[idx, 0]
            body = df_new.iloc[idx, 2]
            link = df_new.iloc[idx, 3]
            # print(company_name)
            # print(body)
            # print(link)

            item = get_item_to_dynamodb(dynamodb, company_name)

            if item:
                item_body = item["body"]
                if not item_body == body:
                    is_update = True
                    print(f"{company_name}：IRが更新されました。")
                    print(f"DB：{item_body}")
                    print(f"スクレイピング：{body}")
                else:
                    print(f"{company_name}：IRは更新されていません")
                    break

            else:
                # DBにデータのない会社は１件取得でOK
                is_update = True
                print(f"{company_name}：IRが更新されました。{body}")
                break

            if old != company_name:
                slack.message_heading(company_name)
                old = company_name

            # 本文が英語なら翻訳してからSlackに送信する
            # print(body)
            # print(check_english(
            #     "today"))
            # if check_english(body) is not None:
                # print("翻訳します")
            # body = translate(body)
            # Slackに送るメッセージとして追加
            slack.message_shaping(body, link)
            idx += 1
            print("\n")

        # IRが更新されていたら最新のデータだけをDBにセットする
        if is_update:
            update_company_name = df_new.iloc[0, 0]
            update_body = df_new.iloc[0, 2]
            put_item_to_daynamodb(dynamodb, update_company_name, update_body)

    print("\n")
    df.to_csv("./result/text.csv")
    # スクレイピング結果をSlackに投げる
    slack.show()
    slack.send()
    web_scraping.close()

    print("スクレイピングを終了しました")
