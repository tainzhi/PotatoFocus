import QtQuick
import QtQuick.Controls.Basic

SwitchDelegate {
    id: control
    checked: true

    indicator: Rectangle {
        implicitWidth: 48
        implicitHeight: 26
        x: control.width - width - control.rightPadding
        y: parent.height / 2 - height / 2
        radius: 13
        color: control.checked ? "#17a81a" : "transparent"
        border.color: control.checked ? "#17a81a" : "#cccccc"

        Rectangle {
            x: control.checked ? parent.width - width : 0
            width: 26
            height: 26
            radius: 13
            color: control.down ? "#cccccc" : "#ffffff"
            border.color: control.checked ? (control.down ? "#17a81a" : "#21be2b") : "#999999"
        }
    }

    background: Rectangle {
        implicitWidth: 48
        implicitHeight: 34
        visible: control.down || control.highlighted
        color: control.down ? "#bdbebf" : "#eeeeee"
    }
}
