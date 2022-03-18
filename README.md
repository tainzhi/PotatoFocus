## Info
这是一个 PyQt5 + Python3.9 （pycharm + poetry）实现的**跨平台番茄钟久坐神器**

实现的功能：默认25min的番茄工作时间，然后弹出全屏屏保（如果是多屏幕，都会全屏屏保覆盖，但是只在主屏幕显示倒计时）并5min倒计时。
倒计时结束或者按 Esc 键开启下一个25 min 工作循环。

目前只在windows测试，还未在mac和linux下测试。

## Todo
- [ ] 开机启动 [1](https://www.geeksforgeeks.org/autorun-a-python-script-on-windows-startup/) 和 [2](https://www.yisu.com/zixun/166099.html),也可参考 https://www.yisu.com/zixun/166099.html
- [ ] trayicon显示当前状态
- [ ] 从 [unsplash](https://unsplash.com/documentation#creating-a-developer-account) 下载屏保图片自动更新
- [ ] 添加设置 break和work的时间ui

## Reference
图标网址: https://www.iconfont.cn/search/index?searchType=icon&q=%E7%95%AA%E8%8C%84
python style https://peps.python.org/pep-0008/#function-and-variable-names
[PyQt5实战学习](https://github.com/cxinping/PyQt5)

