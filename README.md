


# Stocks Profits Tracker (+ Notion API Integration with Python)

1. There are 3 main steps to make this work
2. You can track live crypto prices from CoinGecko API (so get the API key for it for a free account)

![Cover.png](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/amu31tn9r9d6jfonp7n3.png)


# Integration Guide
---

** Follow these steps to create a notion integration:**

1. Click here → https://notion.so/my-integrations/ (**once you open this link in your browser, the website may ask you to login to your notion account**)
2. Make `+ New Integration` button 
    
![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/7wop4ntbxxdzhwz8wz0x.png)
    

3. Fill in the `Basic Information:` , you can set the following values:
    1. Type → `Internal`
    2. Associated Workspace → **Choose your notion account’s workspace**
    3. Name → `Stock Profits Tracker`
    

4. You’ll be on a webpage called `Secrets` 
> Copy & Paste the above 🔑 `Notion Integration Secret Key` in my_variable.yml 🔒 file.
    


## 1. Create a Notion Page (with Integration):
1. Create a new notion page & click on the three dots `...` in the top right corner of the duplicate notion template
2. Click on `+ Connections` at the end of the the drop down, 
3. Select ( `Stock Profits Tracker`)
    

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/i4tf41c2hdsom3epfgyl.png)
    

## 2. Create a Notion table
1. Create a notion database by typing `/database`.
2. Select `Database - Inline`
3. Create the following column with names:
    a. `Name` → for coin Name (BTC)
    b. `api id` → Add the amount you bought the stock units with
    c. `Current Price` → Get's the current price

💡 The above is only for live price tracking,.
💡 You can add more live columns supported by coinGecko by changing the code.
💡 Feel free to add any other columns on top of this as you like. Like your `avg buy price` etc.

4. Get database ID.
    a. Click on 3 dots `...` of the database you create
    b. Click `Copy Link To View`.
    c. Open the copied URL in a new page.
```
https://www.notion.so/fer6ff3d5fcs3dff1d2134349192cc?v=4rf43545...
                     |---------Database ID----------|
```
> Copy & Paste the above 🔑 `Database ID` in my_variable.yml 🔒 file.



## Running Python Script:

**The final part of the integration is about running a python script that will update the real stock prices for all the stock units you have in the database.**

---

1. **Clone this GitHub repository**
2. **Save the secret notion integration token in the `my_variables.yml` file**
    
    ```bash
    MY_NOTION_SECRET_TOKEN: paste-your-notion-integration-token-here
    ```
    
3. **Install the python requirements and dependency libraries by running the command in your terminal**
    
    ```bash
    python3 -m pip3 install -r requirements.txt
    ```
    
4. **Finally run this command in your terminal to start the live `Price/Unit` update process**
    
    ```bash
    python3 main.py
    ```
    

The following project has been inspired by a US stock portfolio github project by github user tnvMadhav