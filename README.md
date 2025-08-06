## Info
这是一个 PySide6 实现的**跨平台番茄钟久坐神器**

实现的功能：
1. 默认25min的番茄工作时间，然后弹出全屏屏保(**强制休息**),并5min倒计时。
2. **支持多屏显示器**（如果是多屏幕，都会全屏屏保覆盖，但是只在主屏幕显示倒计时）
3. 倒计时结束或者按 Esc 键开启下一个25 min 工作循环。
4. 从[Pixabay](https://pixabay.com/api/docs/)下载图片, 随机选取作为break时间的桌面屏保(~~不使用更知名的[unsplash](https://unsplash.com/documentation#creating-a-developer-account), 应为在不开代理的情况下访问很不问题~~

**注意**：api_key 获取页面 https://pixabay.com/api/docs/， 我的注册账号是qfq61@qq.com


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

## Reference
- 图标网址: https://www.iconfont.cn/search/index?searchType=icon&q=%E7%95%AA%E8%8C%84