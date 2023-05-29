"""
RPA for browser
"""
from logging import getLogger, StreamHandler, Formatter, DEBUG
from pywinauto import Desktop, findwindows, timings
from pywinauto.application import Application
import tkinter as tk
import tkinter.ttk as ttk
from pprint import pprint

"""
ライブラリでlocale.getpreferredencoding()を使用してencodingを指定している場合
データにutf-8にしか存在しない文字が含まれているとエラーになる
下記のハックで強制的にutf-8を返す
"""
import locale
def getpreferredencoding(do_setlocale = True):
    return "utf-8"
locale.getpreferredencoding = getpreferredencoding

class RPA4Browser():
    """
    制御クラス
    """
    def __init__(self, view:tk.Frame) -> None:
        """
        コンストラクタ：制御画面クラスを関連付ける
        Args:
            Frame:  画面クラス(ビュー)
        """
        self.app = None     # pywinautoのApplication(またはDesktop)オブジェクトを保持
        self.view = view    # 制御画面クラスのオブジェクト

        # Global timings
        # timings.Timings.slow()
        # VSCodeでは動くがバッチでは動かないので以下をコメントアウト
        # timings.Timings.window_find_timeout = 10
        # timings.Timings.app_connect_timeout = 10

    def get_app_via_application_connect(self, app_name:str):
        """
        ブラウザに接続
        Applicationオブジェクトを作成し、接続
        接続できなかった場合は例外が発生し、呼び出し元で処理
        Args:
            str:    アプリケーション名
        """
        self.app = Application(backend="uia")

        # 接続は、アプリが起動していないとエラー
        self.app.connect(title_re=f".*{app_name}", timeout=10)  # タイトルを正規表現で
        logger.info(">>>Connected app")

        return

    def get_app_via_desktop(self):
        """
        Browserの情報取得Desktopクラス使用
        """
        self.app = Desktop(backend="uia")

        return

    def get_dialog(self, app_name):
        """
        ダイアログを取得
        取得できなかった場合は例外が発生し、呼び出し元で処理
        ダイアログはself.browser_dlgに取得
        Args:
            str:    アプリケーション名
        """
        self.browser_dlg = self.app.window(title_re=f".*{app_name}")
        self.browser_dlg.wait("exists", timeout=10)
        logger.info(">>>Got target dialog")

        self.browser_dlg.set_focus()    # アプリを見えるようにしてその後の操作を見せる

        return
        
    def get_tab_ctl(self, tab_name):
        """
        タブコントロールを取得
        取得できなかった場合はタイムアウトの例外が発生し呼び出し元で処理
        タブコントロールはself.tab_ctlに取得
        Args:
            str:    タブ名
        """
        self.tab_ctl = self.browser_dlg.child_window(title_re=f".*{tab_name}.*", control_type="TabItem")
        self.tab_ctl.wait("exists", timeout=60)
        logger.info(">>>Got TabItem control")

        self.tab_ctl.click_input()      # タブをクリックして該当のタブを表示する
        self.tab_ctl.wait("visible", timeout=180)
        logger.info(">>>Got visible")

    def key_type(self, event=None, key:str=None):
        """
        ブラウザにキー操作を施す
        Args:
            str:    キーストローク名(key_stroke辞書のキーのどれか)
        """
        # self.browser_dlg.set_focus()
        # self.browser_dlg.wait("ready")

        # キー入力用辞書(キーストローク名:入力するキー)
        key_stroke = {"bottom":"{END}", "top":"{HOME}", "down":"{PGDN}", "up":"{PGUP}", "next_page":"次のページ", "search":"検索", "jump":"{TAB}", "back":"%{LEFT}", "see":"~"}
        logger.info(f">>>start typing keys:{key}")
        if key == "next_page":
            self.search_word(key_stroke.get(key))
            self.key_type(key="see")
        elif key == "search":
            self.search_word(self.view.var_word.get())
        else:
            self.browser_dlg.type_keys(key_stroke.get(key))
        
        self.browser_dlg.wait("ready")      # type_keysの動作が終わるのを待つ これをしないとfocus_force()が先に動いてしまう
        self.view.focus_force()             # 自分自身にフォーカスを戻す
        
        # ボタンが押されてこの処理に来た時は、マウスカーソルをボタンに戻す
        if event:
            event.widget.focus_set()
            self.view.event_generate("<Motion>", warp=True, x=event.widget.winfo_x()+10, y=event.widget.winfo_y()+10)

    def search_word(self, word:str):
        """
        検索
        ブラウザにctl+Fを出して、検索ワードを入力して検索する
        検索ダイアログは閉じる
        Args:
            str:    検索ワード
        """
        logger.info(f">>>\tsearch:{word}")
        if self.app_name == "Chrome":
            self.browser_dlg.type_keys("^f" f"{word}" "~" "{ESC}", pause=0.1) # ^:ctrl, ~:Enter chromeにはこれが合うみたい。でも十分ではない
            # Chromeで以下はうまくいかない。コントロールが見つからない。デバッグで止めると見つかるのはなぜ?
            # self.browser_dlg.type_keys("^f")      # 検索
            # search_ctrl = self.browser_dlg.Edit2
            # search_ctrl.wait("ready")
            # search_ctrl.set_edit_text(f"{word}")  # 検索ワード
            # search_ctrl.type_keys("{ESC}")        # 検索ダイアログを閉じる
        else:
            # self.browser_dlg.type_keys("'") # リンク検索 こちらは数秒で消える
            self.browser_dlg.type_keys("^f") # 検索
            search_ctrl = self.browser_dlg.child_window(title="ページ内検索", control_type="Edit")
            search_ctrl.wait("ready")
            search_ctrl.set_edit_text(f"{word}")    # 検索ワード
            self.browser_dlg.type_keys("{ESC}")     # 検索ダイアログを閉じる

    def connect_browser(self, app_name:str, tab_name:str, event=None) -> int:
        """
        ブラウザに接続
        Args:
            str:    アプリケーション名
            str:    タブ名
        Returns:
            int:    接続結果(0:OK, -1:TimeoutError, -2:NotUnique)
        """
        logger.info(f">>>Start connect, browser:{app_name}, tab:{tab_name}")

        self.app_name = app_name
        try:
            self.get_app_via_application_connect(app_name) # Applicationオブジェクトで接続
            # self.get_app_via_desktop()        # Desktopオブジェクトで接続
            self.get_dialog(app_name)           # ダイアログ(ウィンドウ)取得
            self.get_tab_ctl(tab_name)          # タブを指定
        except timings.TimeoutError:            # 接続中にタイムアウトが発生
            return -1
        except findwindows.ElementAmbiguousError as e:   # 一致する要素が複数あった
            return -2
        return 0

class MyFrame(tk.Frame):
    """
    操作画面クラス
    """
    def __init__(self, master) -> None:
        """
        コンストラクタ：画面作成
        """
        super().__init__(master)

        self.config(background="lightblue")     # ボタンの境目に色を出すために背景色を指定

        # ブラウザ選択コンボボックス
        lbl_browser = tk.Label(self, text="ブラウザ")
        lbl_browser.pack(fill=tk.X)
        lst_browser = ("Chrome", "Firefox")
        self.var_browser = tk.StringVar()
        cbb_browser = ttk.Combobox(self, textvariable=self.var_browser, values=lst_browser)
        cbb_browser.pack(fill=tk.X)
        cbb_browser.set(lst_browser[0])

        # タブ名指定エントリー
        lbl_tab_name = tk.Label(self, text="タブ名")
        lbl_tab_name.pack(fill=tk.X)
        self.var_tab_name = tk.StringVar(value="グループ")
        ent_tab_name = tk.Entry(self, textvariable=self.var_tab_name)
        ent_tab_name.pack(fill=tk.X)

        self.btn_connect = tk.Button(self, text="接続")
        self.btn_connect.pack(fill=tk.X, pady=(0,5))

        # 制御用ボタンの作成
        commands = {"down":"下", "next_page":"次のページ", "up":"上", "top":"トップ", "bottom":"ボトム", "jump":"次のリンク", "back":"戻る", "see":"見る", "search":"検索"}
        buttons = {}
        for key, value in commands.items():
            buttons[key] = tk.Button(self, text=value)
            buttons[key].bind("<1>", lambda event, key=key: self.rpa.key_type(event, key))
            buttons[key].bind("<space>", lambda event, key=key: self.rpa.key_type(event, key), add=True)
            buttons[key].bind("<Return>", lambda event, key=key: self.rpa.key_type(event, key), add=True)
            buttons[key].pack(fill=tk.X)
        
        # 検索ボタンとエントリーの作成
        buttons["search"].pack(pady=(5,0))
        self.var_word = tk.StringVar(value="")
        ent_word = tk.Entry(self, textvariable=self.var_word)
        ent_word.pack(fill=tk.X)

    def set_rpa(self, rpa:RPA4Browser):
        """
        コントロールの指定とボタンの操作をパイント
        Args:
            RPA4Browser:    コントロールオブジェクト(RPAを実施するオブジェクト)
        """
        self.rpa = rpa
        # 接続ボタンのバインド
        self.btn_connect.config(command=self.connect_browser)

    def connect_browser(self):
        """
        ブラウザに接続
        成功：背景色を緑に タイムアウト：背景色を赤に 対象が複数：背景色を黄色に
        マウスカーソルを接続ボタンに戻す
        """
        self.btn_connect.config(bg="white")
        # 画面で指定されたブラウザとタブ名でブラウザに接続
        connect_result = self.rpa.connect_browser(self.var_browser.get(), self.var_tab_name.get())
        # 接続結果に基づいてボタンの背景色を変える
        if connect_result == 0:
            self.btn_connect.config(bg="lightgreen")
        elif connect_result == -1:
            self.btn_connect.config(bg="red")
        else:
            self.btn_connect.config(bg="yellow")
        self.btn_connect.focus_force()    # ブラウザにあるフォーカスをアプリに戻す
        self.event_generate("<Motion>", warp=True
            , x=self.btn_connect.winfo_x()
            , y=self.btn_connect.winfo_y())  # マウスカーソルの移動

class App(tk.Tk):
    """
    アプリケーションクラス
    """
    def __init__(self) -> None:
        """
        コンストラクタ：操作画面クラスと制御クラスを作成し関連付ける
        """
        super().__init__()

        self.title("ブラウザ操作")      # タイトル
        my_frame = MyFrame(self)                    # MyFrameクラス(V)のインスタンス作成
        my_frame.pack()
        rpa_for_browser = RPA4Browser(my_frame)     # 制御クラス(C)のインスタンス作成
        my_frame.set_rpa(rpa_for_browser)           # MyFrameクラスに制御クラスを関連付ける

if __name__ == '__main__':
    # logger setting
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

    app = App()
    app.mainloop()
