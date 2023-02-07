"""
pywinauto でブラウザ制御のテスト
他のアプリを調査する時の参考になるかもしれません
"""
from logging import getLogger, StreamHandler, Formatter, DEBUG
from pywinauto import Desktop, findwindows, timings
from pywinauto.application import Application

"""
ライブラリでlocale.getpreferredencoding()を使用してencodingを指定している場合
データにutf-8にしか存在しない文字が含まれているとエラーになる
下記のハックで強制的にutf-8を返す
"""
import locale
def getpreferredencoding(do_setlocale = True):
    return "utf-8"
locale.getpreferredencoding = getpreferredencoding

def print_windows():
    """
    起動しているアプリケーションを求める
    """
    from pywinauto import findwindows

    # このメソッドはローレベルな関数を使用するので使用を推奨されていない。
    if logger.isEnabledFor(DEBUG):
        wins = findwindows.find_elements()
        logger.debug("\n>>>Window list by find_elements")
        for win in wins: logger.debug(win)

        # アプリの一覧    
        app = Desktop(backend="uia")
            
        for win in app.windows():logger.debug(win)


def get_app_via_application_connect(app_name, tab_name):
    """
    Browserの情報取得Applicationクラス使用してコネクト
    """
    app = Application(backend="uia")

    try:
        # バッチで実行するとtimings.Timings.app_connect_timeoutが効かない
        # VS Codeのctrl+F5だと効く。なぜ
        # timeout引数はどちらも有効
        app.connect(title_re=f".*{app_name}", timeout=15)  # 起動していないとエラー アクティブでないと見つからない
        # connectで接続できるのは一つのタスク
    except findwindows.ElementAmbiguousError as e:  # 一致する要素が複数あった
        logger.info(e)
        app.connect(title_re=f".*{tab_name}")  # 起動していないとエラー アクティブでないと見つからない
    logger.info(">>>Connected app")

    return app

def get_app_via_desktop():
    """
    Browserの情報取得Desktopクラス使用
    """
    app = Desktop(backend="uia")

    return app

def get_dialog(app, app_name, tab_name):
    """
    ダイアログを取得
    """
    # トップウィンドウの名前を見つける
    if logger.isEnabledFor(DEBUG):
        logger.debug("\n>>>Window list")
        for win in app.windows(): logger.debug(win)

    try:
        browser_dlg = app.window(title_re=f".*{app_name}")
        browser_dlg.wait("exists", timeout=15)
    except findwindows.ElementAmbiguousError as e:
        logger.info(e)
        browser_dlg = app.window(title_re=f".*{tab_name}")
        browser_dlg.wait("exists")
    
    logger.info(">>>Got target tab")

    browser_dlg.set_focus()

    if logger.isEnabledFor(DEBUG):
        logger.debug("\n>>>Browser Control list")
        browser_dlg.print_control_identifiers(depth=3)
        # browser_dlg.print_control_identifiers(depth=4)  # depth=4にするとtabitemが見える
        # ブラウザでdepth=Noneでこれをやると止まらないのでその時はファイルに書き込み
        # browser_dlg.print_control_identifiers(depth=None, filename="Browser_ids.txt")

        # depthを3にするとタブが出てくる。その時のタイプはTabItem
        logger.debug("\n>>>Browser descendants list by depth")
        w = browser_dlg.descendants(depth=3)
        for i in w: logger.debug(i)
        logger.debug("\n>>>Browser TabItem list by type")
        wrapper_list = browser_dlg.descendants(control_type="TabItem")
        for wrapper in wrapper_list: logger.debug(wrapper)

    return browser_dlg
    
def ope_tab_page(browser_dlg, tab_name):
    """
    キー操作
    """
    b_tab_ctl = browser_dlg.child_window(title_re=f".*{tab_name}.*", control_type="TabItem")
    b_tab_ctl.wait("exists")
    logger.info(">>>Got TabItem control")

    if logger.isEnabledFor(DEBUG):
        logger.debug("\n>>>グループ tab Control list in TabItem")
        b_tab_ctl.print_control_identifiers()

    b_tab_ctl.click_input()
    b_tab_ctl.wait("visible")
    logger.info(">>>Got visible")
    logger.info(">>>start typing keys on グループ")
    browser_dlg.type_keys("{PGDN}")
    browser_dlg.type_keys("{PGDN}")
    # 検索
    # browser_dlg.type_keys("^f" "次のページ" "^g" "{ESC}") # ^はctrl
    # browser_dlg.type_keys("~")  # ~はEnter

    browser_dlg.type_keys("^f") # ^はctrl 検索した所でEscするとフォーカスが当たる
    if logger.isEnabledFor(DEBUG):
        logger.debug("\n>>>検索ダイアログあり tab Control list in TabItem")
        browser_dlg.print_control_identifiers()

    browser_dlg.type_keys("次のページ") # ^はctrl 検索した所でEscするとフォーカスが当たる
    browser_dlg.type_keys("^g" "{ESC}") # ^はctrl 検索した所でEscするとフォーカスが当たる
    # browser_dlg.type_keys("~")  # ~はEnter
    pass

if __name__ == '__main__':
    # logger setting
    # ログレベルをDEBUGにすると詳細情報が出る
    LOGLEVEL = "INFO"   # ログレベル('CRITICAL','FATAL','ERROR','WARN','WARNING','INFO','DEBUG','NOTSET')
    logger = getLogger(__name__)
    handler = StreamHandler()	# このハンドラーを使うとsys.stderrにログ出力
    handler.setLevel(LOGLEVEL)
    # ログ出形式を定義 時:分:秒.ミリ秒 L:行 M:メソッド名 T:スレッド名 コメント
    handler.setFormatter(Formatter("{asctime}.{msecs:.0f} L:{lineno:0=3} M:{funcName} T:{threadName} : {message}", "%H:%M:%S", "{"))
    logger.setLevel(LOGLEVEL)
    logger.addHandler(handler)
    logger.propagate = False

    logger.debug("start log")

    # start
    _app_name = "Chrome"
    _app_name = "Firefox"
    _tab_name = "グループ"

    # Grobal timings
    # timings.Timings.slow()
    timings.Timings.window_find_timeout = 10    # for wiat()
    timings.Timings.app_connect_timeout = 30     # for connect()

    print_windows()  # 低レベルで起動しているウィンドウをリストする
    app = get_app_via_application_connect(_app_name, _tab_name) # Applicationオブジェクトで接続
    # app = get_app_via_desktop()   # Desktopオブジェクトで接続
    dlg = get_dialog(app, _app_name, _tab_name) # ダイアログ(ウィンドウ)取得
    ope_tab_page(dlg, _tab_name)     # タブを指定してキー操作
