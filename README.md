## Info
这是一个 PyQt5 实现的**跨平台番茄钟久坐神器**

实现的功能：
1. 默认25min的番茄工作时间，然后弹出全屏屏保（如果是多屏幕，都会全屏屏保覆盖，但是只在主屏幕显示倒计时）并5min倒计时。
2. 倒计时结束或者按 Esc 键开启下一个25 min 工作循环。
3. 从[Pixabay](https://pixabay.com/api/docs/)下载图片, 随机选取作为break时间的桌面屏保(~~不使用更知名的[unsplash](https://unsplash.com/documentation#creating-a-developer-account), 应为在不开代理的情况下访问很不问题~~


目前只在windows测试，还未在mac和linux下测试。


其实已经有了很成熟的工具了。使用起来也很方便。
- focus(for macOS only)
- Workrave(for windows only)
- [wnr](https://github.com/RoderickQiu/wnr)(for macos/windows, electro实现)

## usage
```bash
# windows
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Todo
- [ ] 开机启动 [1](https://www.geeksforgeeks.org/autorun-a-python-script-on-windows-startup/) 和 [2](https://www.yisu.com/zixun/166099.html),也可参考 https://www.yisu.com/zixun/166099.html
- [ ] trayicon显示当前状态
- [ ] 添加设置 break和work的时间ui

## Reference
- 图标网址: https://www.iconfont.cn/search/index?searchType=icon&q=%E7%95%AA%E8%8C%84