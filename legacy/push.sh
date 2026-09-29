# 自动生成更新日期内容
nowDate=$(date +%F)
echo -e "# THE END \n\n更新日期："$nowDate  >  end.md
# 编译md为reveal幻灯片内容
pandoc --mathjax -t revealjs -s --css imd.css --highlight-style haddock --include-in-header=favicon.html --include-after-body=dev.html  --slide-level=5 title.md 媒介融合.md 融合新闻.md hugo.md 新媒体思维.md 短视频新闻.md 移动直播.md 选题策划.md end.md -o index.html
# 推送到远程仓库
git add .
git commit -m $1
git push
