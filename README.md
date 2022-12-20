# 施工中

## 簡介

測試用demo project

#### 2022.12.10

一直想把pytest測試flask做一個統整，算是整理一路遇到的狀況

## 使用方式

環境安裝之後，於terminal 輸入 pytest

會出現 /htmlcov/index.html (於本機)  
與 /testReport.html

OPEN IT!

## What is fixture() in pytest?

在 Pytest 中，fixture 是一個用來提供輸入資料給測試函數的函數。 
fixture 函數使用 @pytest.fixture 裝飾器
測試函數可以將其作為輸入引用。

例如:

    import pytest

    @pytest.fixture
    def fixture_data():
        return [1, 2, 3]

要在測試函數中使用此 fixture，可以將其指定為輸入引數：

    def test_using_fixture(fixture_data):
        assert len(fixture_data) == 3

fixture 可以用來建立臨時資料庫，執行使用資料庫的測試，然後在測試完成後刪除資料庫。

例如:
    
    import pytest
    
    @pytest.fixture
        def db():
            # open db
            yield
            # close db

Fixture 可以在任何 Python 模組中定義，
但通常在名為 conftest.py 的文件中定義它們，
該文件位於與測試文件相同的目錄中。 

conftest.py 文件被 Pytest 自動發現，
因此在其中定義的 fixture 可供同一目錄及其子目錄中的所有測試使用。

這對於以分層結構組織 fixture 是有用的，
其中根目錄中的 conftest.py 文件中可以定義常用的 fixture，
而子目錄中的 conftest.py 文件中可以定義更具體的 fixture。

以下是具有 conftest.py 文件的目錄結構的示例：

    project/
    ├── conftest.py
    └── test/
        ├── conftest.py
        ├── test_module1.py
        └── test_module2.py


## 將fixture與flask test client一同應用

### 目前有放入三種flask test client的開啟方式，介紹特點，於註解中有說明，簡單整理如下:

1. 用return test_client時，只可以在測試中看到response object，單純測試回傳值或status code時可以使用


    @pytest.fixture()
    def app_return():
        # 示範不yield，return test client的flow
        # 只能測試response本身，沒有辦法看到request流程內部的狀況(g, signal之類)
        app = create_app()
        app.config.update({
            "TESTING": True,
        })
    
        with app.test_client() as test_client:
            return test_client


2. 用yield test_client時，由於測試會停留在flask的life cycle內，可以在call api完後看懂flask內的東西，例如g:


    @pytest.fixture()
    def app_yield():
        # 示範不打開app context，可以在call client後測試g，但無法事先設定
        app = create_app()
        app.config.update({
            "TESTING": True,
        })
    
        with app.test_client() as test_client:
            yield test_client

3. 承2，手動開啟app context，可以在測試內的任何地方看懂g，例如可以另外設定g.param1，g.param2的值，提高測試的方便程度


    @pytest.fixture()
    def app():
        app = create_app()
        # flask建議於測試時加入config
        app.config.update({
            "TESTING": True,
        })
    
        with app.test_client() as test_client:
            # 手動打開 app context，讓整個測試都能用g
            with app.app_context():
                # yield讓測試結束前，測試本身都能停留在request行為內
                yield test_client