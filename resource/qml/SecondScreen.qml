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
    property real windowOpacity: 0
    
    Image {
        id: backgroundImage
        source: "../ScreenPhoto/default.jpg"
        objectName: "backgroundImage"
        fillMode: Image.PreserveAspectCrop
        anchors.fill: parent
    }
    
    Connections {
        target: bridge
        function onFullScreenDesktopOverlayShowSignal(show) {
            if (show) {
                secondWindow.visible = true
            } else {
                secondWindow.visible = false
            }
        }
        
        function onSetBackgroundSignal(value) {
            backgroundImage.source =  value
        }
    }

    opacity: windowOpacity
    Behavior on windowOpacity {
        PropertyAnimation {
            target: secondWindow
            property: "windowOpacity"
            duration: 600
        }
    }

    onVisibleChanged: {
        if (visible) {
            windowOpacity = 1
            secondWindow.showFullScreen();
        } else {
            windowOpacity = 0
        }
    }
}
