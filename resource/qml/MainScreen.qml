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

    property int breakTimeInSecond: 5 * 60 // seconds
    property string breakTimerColor: "white"

    Connections {
        target: bridge
        function onBreakTimeSignal(value) {
            breakTimeInSecond = value;
        }
        
        function onBreakTimerColorSignal(value) {
            timerText.color = value;
        }
    }
    
    opacity: windowOpacity
    Behavior on windowOpacity {
        PropertyAnimation {
            target: mainWindow
            property: "windowOpacity"
            duration: 300
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

    Timer {
        id: breakTimer
        interval: 1000 // 每秒触发一次
        running: false // 初始不运行
        repeat: true
        // 剩余时间属性，初始值为 5 分钟
        property int remainingTime: breakTimeInSecond * 1000
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
        // mainWindow.showFullScreen();
        // breakTimer.start();
    }

    onVisibleChanged: {
        if (visible) {
            windowOpacity = 1;
            breakTimer.remainingTime = breakTimeInSecond * 1000;
            breakTimer.start();
        } else {
            windowOpacity = 0;
            breakTimer.stop();
        }
    }
}