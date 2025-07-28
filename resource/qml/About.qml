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

    Button {
        id: closeAboutButton
        height: 32
        width: 32
        anchors {
            right: parent.right
            rightMargin: 8
            topMargin: 6
            top: parent.top
        }
        contentItem: Image {
            source: "../icons/close.svg"
            width: 32
            height: 32
            anchors.centerIn: parent
            fillMode: Image.PreserveAspectFit
        }
        background: Rectangle {
            color: "transparent"
        }
        hoverEnabled: true
        onClicked: aboutDialog.close()
    }

    Text {
        text: "AutomatedTest tool for Mot camera app, \nversion " + version
        color: Colors.primary
        y: 52
        anchors.left: parent.left
        anchors.leftMargin: 8
        font.pointSize: 11
        horizontalAlignment: Text.AlignLeft
        Layout.alignment: Qt.AlignHCenter
    }
    
    Text {
        text: "download/flash build automatically;\nlaunch mot camera app,\nswitch mode, capture photo/potrait/video automatically,\nswitch camera facing/zoom lens automatically."
        color: Colors.darkest
        y: 109
        anchors.left: parent.left
        anchors.leftMargin: 8
        font.pointSize: 10
        horizontalAlignment: Text.AlignLeft
        Layout.alignment: Qt.AlignHCenter
    }
    
    Text {
        text: "Copyright (c) 2025, MotCamera app team"
        color: Colors.darkest
        y: 220
        anchors.left: parent.left
        anchors.leftMargin: 8
        font.pointSize: 11
        horizontalAlignment: Text.AlignLeft
        Layout.alignment: Qt.AlignHCenter
    }
}
