## 環境構築
node.jsのインストール

[https://nodejs.org/ja/download/](https://nodejs.org/ja/download/)

このレポジトリをクローン
```bash
git clone https://github.com/maron5274/QC-judge.git
```

node_modulesのインストール
```bash
npm install
```

## ローカル開発
```bash
npm run dev
```
### fastAPI
uvicornのインストール
```bash
pip install fastapi uvicorn
```
起動
```bash
cd ./pages/api
uvicorn apiTest:app
```
<<<<<<< HEAD

=======
>>>>>>> 66ca48cc28104d444c26e5eea63993df425d0212
## デプロイ
[https://maron5274.github.io/QC-judge/](https://maron5274.github.io/QC-judge/)に公開

mainブランチにpushして自動更新
```bash
git add -A
git commit -m "any message"
git push origin main
```
