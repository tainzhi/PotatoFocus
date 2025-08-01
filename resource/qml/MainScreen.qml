import QtQuick
import QtQuick.Window
import QtQuick.Controls

Window {
    id: mainWindow
    visible: false
    title: "Main Screen"
    color: "transparent"
    // 设置窗口标志, 去掉标题栏
    flags: Qt.FramelessWindowHint
    property real windowOpacity: 0

    property int breakTimerIntialValueInSecond: 5 * 60 // seconds
    property string breakTimerColor: "#ffffff"

    Connections {
        target: bridge
        function onBreakTimerIntialValueInSecondSignal(value) {
            breakTimerIntialValueInSecond = value;
        }
        
        function onBreakTimerColorSignal(value) {
            Qt.callLater(function() {
                timerText.color = value;
            });
        }
        
        function onFullScreenDesktopOverlayShowSignal(show) {
            if (show) {
                Qt.callLater(function() {
                    mainWindow.visible = true
                    mainWindow.showFullScreen()
                    mainWindow.raise()
                    mainWindow.requestActivate()
                })
            } else {
                mainWindow.visible = false
            }
        }
        
        function onSetBackgroundSignal(value) {
            backgroundImage.source =  value
        }
    }
    
    opacity: windowOpacity
    Behavior on windowOpacity {
        PropertyAnimation {
            target: mainWindow
            property: "windowOpacity"
            duration: 600
        }
    }

    Image {
        id: backgroundImage
        source: "../ScreenPhoto/default.jpg"
        objectName: "backgroundImage"
        fillMode: Image.PreserveAspectCrop
        anchors.fill: parent
    }

    Text {
        id: timerText
        // 格式化剩余时间为 mm:ss 格式
        text: Qt.formatTime(new Date(0, 0, 0, 0, Math.floor(breakTimer.remainingTime / 60000), Math.floor((breakTimer.remainingTime % 60000) / 1000)), "mm:ss")
        color: breakTimerColor
        font.pointSize: 80
        font.bold: true
        anchors.centerIn: parent
    }
    
    
    Text {
        // 格式化剩余时间为 mm:ss 格式
        text: "Esc 键退出屏保图片和休息倒计时, 开始work计时"
        color: "white"
        font.pointSize: 20
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 30
        anchors.left: parent.left
        anchors.leftMargin: 30
    }

    Timer {
        id: breakTimer
        interval: 1000 // 每秒触发一次
        running: false // 初始不运行
        repeat: true
        // 剩余时间属性，初始值为 5 分钟
        property int remainingTime: breakTimerIntialValueInSecond * 1000
        onTriggered: {
            remainingTime -= interval;
            if (remainingTime <= 0) {
                stop(); // 剩余时间为 0 时停止计时
                remainingTime = 0; // 确保剩余时间不小于 0
                bridge.onBreakTimeout();
            }
        }
    }

    Component.onCompleted: {
    }

    onVisibleChanged: {
        if (visible) {
            windowOpacity = 1;
            breakTimer.remainingTime = breakTimerIntialValueInSecond * 1000;
            breakTimer.start();
        } else {
            windowOpacity = 0;
            breakTimer.stop();
        }
    }
}