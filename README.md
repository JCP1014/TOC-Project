# TOC-Project
## FSM
  ![alt text](https://github.com/JCP1014/TOC-Project/blob/master/fsm.png)
### States
  * user : initial state, 跳出三種功能選擇
  * q1 : 選擇第一種功能後進入的第一題選擇題，詢問要選擇正餐還是點心/消夜類
  * q2 : 答覆完第一題後進入的第二題，詢問要選擇飯類、麵類、或其他種類
  * q3 : 答覆完第二題後進入的第三題，詢問要選擇乾的或是有湯的
  * q4 : 答覆完第三題後進入的第四題，詢問要選擇中式、西式、或日/韓式料理
  * q5 : 答覆完第三題後進入的最後一題，詢問要選擇 煎/炒/炸 還是 蒸/煮/滷/烤 的烹調方式
  * determine : 根據前面幾題的答覆，篩選出符合需求的食物
  * choosePlace : 選擇第二種功能後讓使用者輸入欲查詢地區
  * chooseFood : 得知欲查詢地區後讓使用者繼續輸入欲查詢食物
  * search : 根據使用者輸入的地區及食物搜尋出結果
  * top1 : 使用者點選第一個搜尋結果後可進入此，選擇查看店家在地圖上位置或店家詳細資料
  * top2 : 使用者點選第二個搜尋結果後可進入此，選擇查看店家在地圖上位置或店家詳細資料
  * setting : 選擇第三種功能後可進入此，選擇要直接從目前的口袋清單中隨機產生，或欲增加/刪除店家，或欲查看目前的口袋清單有哪些店家
  * random : 從口袋清單中隨機產生一個結果告訴使用者
  * modify : 在此選擇要新增店家還是刪除店家
  * add : 輸入店家名稱可加入清單
  * dele : 輸入店家名稱可從清單中移除
  * list : 列出目前的口袋清單中所有店家
  
## 功能說明
* "幫我想要吃什麼"
  * 問使用者5題選擇題
  * 根據使用者每一題的答覆，提出幾種建議的食物
* "幫我找店家" : 
  * 決定要吃什麼以後，若想知道附近地區哪裡有賣，可透過輸入地區和食物名稱讓chatbot幫忙搜尋該地區有哪些店家在賣該食物
  * chatbot會在"愛評網"上搜尋，並列出前兩名店家名稱以及該店家食物圖片，若想看更多其他店家，也可點選"查看更多"
  * 點選列出的前兩名店家按鈕後，點選"地圖"可查看google map上店家的位置，點選"詳細資料"則可以看到店家詳細資訊以及相關食記文
* "從我常去的店家挑選" : 
  * **此功能尚未完整**
  * 使用者可按"新增"按鈕後輸入欲加入清單的店家，按"移除"按鈕後可輸入欲從清單中刪除的店家
    > 此功能目前尚有問題待修復
  * 點選"隨機挑一間"按鈕，將從口袋清單裡的店家隨機抽取一間，若使用者不滿意該結果，可點擊"再抽一次"
    > 由於新增與移除之功能尚有問題，所以目前是由程式內定的食物種類中抽取一種
  * 點選"查看目前收藏名單"將列出目前名單裡的店家供使用者確認
    > 已可正確從database取得店家名稱並列出
## 如何使用
* 粉絲專頁名稱：**之後再改名**
* 一開始輸入"主選單"或是"go to options"，即會跳出三種功能的按鈕供使用者選擇
* 根據chatbot回傳的訊息，點擊按鈕或是輸入文字
    > **但  *主選單 >> 從我常去的店家中挑選 >> 新增或移除店家* -- 此功能目前無法使用尚待修復**
* 任何時候皆可透過輸入"回到主選單"，返回重新選擇功能

## Deploy on Heroku
* App name : project--what-to-eat
* Domain : https://project--what-to-eat.herokuapp.com/
* Add-ons : ClearDB MySQL
## 本地端執行方式
    export ACCESS_TOKEN="EAAKoYb0nyqYBACfdmgljZBQRiNowZBdtwq4Y78Q4kxPVo8bZBBZAfRWpbPMw1TFoZCZCFdy4lKixMXBwJ9V3WuPWcCT9TnbkYpOsNIx4ZAxeJ1EaPKxyVm2JPlb03udD32xlgOHs9qufDQk4wWKTXZBTQU38QsyOO89nygiM9tDElwZDZD"
    export VERIFY_TOKEN="verify"
    export PORT=5000
    python3 app.py
    
    # And then open another terminal and excute:
    ./ngrok http 5000
