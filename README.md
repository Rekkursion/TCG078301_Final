# 109-1 TCG078301 大數據與程式設計導論 期末專題 <br /> 四資工四甲 B10615031 許晉捷

<br />

## 環境配置（*強烈建議使用 pyenv & virtualenv 或直接透過 PyCharm 內建功能來搭建虛擬 Python（及套件）環境*）

| 項目 | 配置 |
| ---- | ---- |
| 作業系統 | Windows 10 |
| Python 版本 | Python 3.7.8<span style="color:red">**\***</span> |
| 套件需求 | 撰於 <a href='https://github.com/Rekkursion/TCG078301_Final/blob/master/requirements.txt'>requirements.txt</a> 內 |
| 預訓練之 RekkModels | 連結一：https://drive.google.com/file/d/1Wzugo7b_gNyKTsl6DsN8hsgkW8cMI6bX/view?usp=sharing <br /> 連結二：https://mega.nz/file/mbYmFRSL#yLe9ZUgyvIOoz7SvgDZKNtmPE-Eyxi7AtrOQ69LtgQQ |

<span style="color:red">\*本專題中尚未嘗試其他版本的 Python，但根據我資工系大四專題製作的經驗，**mxnet 似乎只支援 Python 3.x**。因此在這邊強烈<ins>建議使用 **pyenv** & **virtualenv** 或直接使用 PyCharm 內建功能來搭建**虛擬 Python 環境**</ins>，可方便安裝指定版本的 Python 及相關套件而不影響現有環境，以方便執行本專題。</span>

<br />

## 執行步驟

1. （***可選但強烈建議***）安裝 pyenv & virtualenv 或使用 PyCharm 內建之功能來搭建 Python 虛擬環境。

2. 安裝 Python 至 **3.7.8**。
    + 3.x 應該也都行，但 3.7.8 是 100% 確定能正常運行本專題。
    + 若有搭建虛擬環境，可不必擔心影響到現有環境，所以強烈建議。
    
3. 安裝 <a href='https://github.com/Rekkursion/TCG078301_Final/blob/master/requirements.txt'>requirements.txt</a> 內的所有「**已指定版本**」的套件。
    + **勿亂改裡面所指定的版本**。
    + 若有搭建虛擬環境，可不必擔心影響到現有環境，所以強烈建議。

4. 下載預訓練之 RekkModel，其連結提供於上面的表格中。

5. 啟動一終端後 cd 至本 project 的根目錄下。

6. 執行以下指令：<code>python main_app.py</code>

7. 第一次執行需要設置預訓練之 RekkModel（於 Step 4. 中所下載的）的路徑，之後就可以正常使用了。

<br />

## Demo 影片

+ Youtube 連結：https://www.youtube.com/watch?v=WXmiCk5fRWQ