import QtQuick
import QtQuick.Controls.Basic
import QtQuick.Layouts


Dialog {
    property string version: "0.0.0"

    id: aboutDialog
    width: 420
    height: 270
    focus: true
    modal: true

    Text {
        text: "About"
        color: Colors.primary
        font.pointSize: 18
        font.bold: true
        anchors {
            top: parent.top
            left: parent.left
            topMargin: 8
            leftMargin: 8
        }
        horizontalAlignment: Text.AlignLeft
        // Layout.alignment: Qt.AlignHCenter
    }
} 
