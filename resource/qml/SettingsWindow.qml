import QtQuick
import QtQuick.Window
import QtQuick.Controls

Window {
    id: settingsWindow
    visible: false
    title: "Settings"
    width: 600
    height: 400
    color: "white"

    Connections {
        target: bridge
        function onSettingsWindowShowSignal(show) {
            settingsWindow.visible = show
        }
    }

    Text {
        text: "Settings Window"
        anchors.centerIn: parent
    }
    
    // callback of window close icon
    onClosing: function(event) {
        event.accepted = false
        settingsWindow.visible = false
        bridge.onSettingsWindowClosed()
    }
}
