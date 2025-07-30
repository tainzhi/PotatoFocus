import QtQuick
import QtQuick.Window
import QtQuick.Controls

Window {
    id: secondWindow
    visible: false
    title: "Second Screen"
    color: "transparent"
    // 设置窗口标志, 去掉标题栏
    flags: Qt.FramelessWindowHint
    
    Image {
        id: backgroundImage
        source: "../ScreenPhoto/default.jpg"
        objectName: "backgroundImage"
        fillMode: Image.PreserveAspectCrop
        anchors.fill: parent
    }
    
    Connections {
        target: bridge
        function onWindowShowSignal(show) {
            if (show) {
                secondWindow.visible = true
            } else {
                secondWindow.visible = false
            }
        }
    }

    Component.onCompleted: {
        // secondWindow.showFullScreen()
    }

    onVisibleChanged: {
        if (visible) {
            secondWindow.showFullScreen();
        } else {
        }
    }
}
