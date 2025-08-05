import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs

Window {
    id: settingsWindow
    visible: false
    title: "Settings"
    color: "white"

    property int workTimeValue: 25
    property int breakTimeValue: 5
    property bool continuousWorkAfterBreakValue: false
    property int continuousWorkCountValue: 4
    property int longBreakTimeValue: 15
    property bool usePixabayImageValue: true
    property string pixabayApiKeyValue: ""
    property int pixabayMostUsedPerImageValue: 10

    Connections {
        target: bridge
        function onSettingsWindowShowSignal(show) {
            settingsWindow.visible = show;
        }

        function onWorkTimeInMinuteSignal(value) {
            workTimeValue = value;
        }

        function onBreakTimeInMinuteSignal(value) {
            breakTimeValue = value;
        }

        function onContinuousWorkAfterBreakSignal(value) {
            continuousWorkAfterBreakValue = value;
        }

        function onContinuousWorkCountSignal(value) {
            continuousWorkCountValue = value;
        }

        function onLongBreakTimeSignal(value) {
            longBreakTimeValue = value;
        }

        function onUsePixabayImageSignal(value) {
            usePixabayImageValue = value;
        }

        function onPixabayApiKeySignal(value) {
            pixabayApiKeyValue = value;
        }

        function onPixabayMostUsedPerImageSignal(value) {
            pixabayMostUsedPerImageValue = value;
        }
    }

    // Use ColumnLayout to manage content and calculate implicit size
    ColumnLayout {
        id: mainLayout

        Item {
            width: 514
            height: 406
            Layout.alignment: Qt.AlignCenter

            Text {
                id: workTextLabel
                text: "工作时间"
                font.pixelSize: 18
                anchors.left: parent.left
                anchors.leftMargin: 11
                anchors.top: parent.top
                anchors.topMargin: 20
            }

            MySpinBox {
                id: workSpinBox
                anchors.left: workTextLabel.right
                anchors.leftMargin: 16
                anchors.top: parent.top
                anchors.topMargin: 13
                value: workTimeValue
            }

            Text {
                id: workSpinBoxUnitLabel
                text: "分"
                font.pixelSize: 18
                anchors.left: workSpinBox.right
                anchors.leftMargin: 16
                anchors.top: workTextLabel.top
                anchors.bottom: workTextLabel.bottom
            }

            Text {
                id: breakTextLabel
                text: "休息时间"
                font.pixelSize: 18
                anchors.left: parent.left
                anchors.leftMargin: 11
                anchors.top: workTextLabel.bottom
                anchors.topMargin: 20
            }

            MySpinBox {
                id: breakSpinBox
                value: breakTimeValue
                anchors.left: breakTextLabel.right
                anchors.leftMargin: 16
                anchors.top: workSpinBox.bottom
                anchors.topMargin: 6
            }

            Text {
                id: breakSpinBoxUnitLabel
                text: "分"
                font.pixelSize: 18
                anchors.left: breakSpinBox.right
                anchors.leftMargin: 16
                anchors.top: breakTextLabel.top
                anchors.bottom: breakTextLabel.bottom
            }

            Text {
                id: continueSwitchLabel
                text: "休息结束后连续工作"
                font.pixelSize: 18
                anchors.left: parent.left
                anchors.leftMargin: 11
                anchors.top: breakTextLabel.bottom
                anchors.topMargin: 20
            }

            MySwitchBox {
                id: continueSwitchBox
                checked: continuousWorkAfterBreakValue
                anchors.left: continueSwitchLabel.right
                anchors.leftMargin: 88
                anchors.top: breakSpinBox.bottom
                anchors.topMargin: 13
            }

            Text {
                id: continueWorkCountTextLabel
                text: "连续工作的番茄钟次数"
                font.pixelSize: 18
                anchors.left: parent.left
                anchors.leftMargin: 11
                anchors.top: continueSwitchLabel.bottom
                anchors.topMargin: 20
            }

            MySpinBox {
                id: continueWorkCountSpinBox
                value: continuousWorkCountValue
                anchors.left: continueSwitchBox.left
                anchors.top: continueSwitchBox.bottom
                anchors.topMargin: 6
            }

            Text {
                id: continueWorkBreakTimeTextLabel
                text: "连续工作番茄钟后的休息时间"
                font.pixelSize: 18
                anchors.left: parent.left
                anchors.leftMargin: 11
                anchors.top: continueWorkCountTextLabel.bottom
                anchors.topMargin: 20
            }

            MySpinBox {
                id: continueWorkBreakTimeSpinBox
                value: longBreakTimeValue
                anchors.left: continueWorkBreakTimeTextLabel.right
                anchors.leftMargin: 16
                anchors.top: continueWorkCountSpinBox.bottom
                anchors.topMargin: 6
            }

            Text {
                id: continueWorkBreakTimeSpinBoxUnitLabel
                text: "分"
                font.pixelSize: 18
                anchors.left: continueWorkBreakTimeSpinBox.right
                anchors.leftMargin: 16
                anchors.top: continueWorkBreakTimeTextLabel.top
                anchors.bottom: continueWorkBreakTimeTextLabel.bottom
            }

            Text {
                id: pixabaySwitchLabel
                text: "使用Pixabay下载的图片作为全面屏背景图片"
                font.pixelSize: 18
                anchors.left: parent.left
                anchors.leftMargin: 11
                anchors.bottom: pixabayApiKeyTextLabel.top
                anchors.bottomMargin: 20
            }

            MySwitchBox {
                id: pixabaySwitchBox
                checked: usePixabayImageValue
                anchors.left: pixabayImageCountSpinBox.left
                anchors.leftMargin: 16
                anchors.bottom: pixabayApiKeyTextInput.top
                anchors.bottomMargin: 0
            }

            Text {
                id: pixabayApiKeyTextLabel
                text: "Pixabay Api Key"
                font.pixelSize: 18
                anchors.left: parent.left
                anchors.leftMargin: 11
                anchors.bottom: pixabayImageCountTextLabel.top
                anchors.bottomMargin: 20
            }

            TextInput {
                id: pixabayApiKeyTextInput
                text: pixabayApiKeyValue
                width: 350
                height: 34
                anchors.right: parent.right
                anchors.rightMargin: 11
                font.pixelSize: 16
                verticalAlignment: TextInput.AlignVCenter
                horizontalAlignment: TextInput.AlignLeft
                anchors.bottom: pixabayImageCountSpinBox.top
                anchors.bottomMargin: 9

                Rectangle {
                    z: -1
                    anchors.fill: parent
                    color: "#dcdbcc"
                }
                MouseArea {
                    anchors.fill: parent
                    acceptedButtons: Qt.RightButton
                    onClicked:(mouse) => {
                        var menu = menuComponent.createObject(pixabayApiKeyTextInput);
                        menu.popup(mouse.x, mouse.y);
                    }
                }

                Component {
                    id: menuComponent
                    Menu {
                        MenuItem {
                            text: qsTr("复制")
                            onTriggered: pixabayApiKeyTextInput.copy()

                        }
                        MenuItem {
                            text: qsTr("粘贴")
                            onTriggered: pixabayApiKeyTextInput.paste()
                        }
                        MenuItem {
                            text: qsTr("全选")
                            onTriggered: pixabayApiKeyTextInput.selectAll()
                        }
                    }
                }
            }

            Text {
                id: pixabayImageCountTextLabel
                text: "Pixabay每张图片最多使用次数"
                font.pixelSize: 18
                anchors.left: parent.left
                anchors.leftMargin: 11
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 16
            }

            MySpinBox {
                id: pixabayImageCountSpinBox
                value: pixabayMostUsedPerImageValue
                anchors.right: parent.right
                anchors.rightMargin: 11
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 9
            }
        }
    }

    // Set width and height based on the implicit size of the layout
    width: mainLayout.implicitWidth
    height: mainLayout.implicitHeight

    // callback of window close icon
    onClosing: function (event) {
        event.accepted = false;
        settingsWindow.visible = false;
        bridge.onWorkTimeInMinuteChanged(workSpinBox.value);
        bridge.onBreakTimeInMinuteChanged(breakSpinBox.value);
        bridge.onContinuousWorkAfterBreakChanged(continueSwitchBox.checked);
        bridge.onContinuousWorkCountChanged(continueWorkCountSpinBox.value);
        bridge.onLongBreakTimeInMinuteChanged(continueWorkBreakTimeSpinBox.value);
        bridge.onUsePixabayImageChanged(pixabaySwitchBox.checked);
        bridge.onPixabayApiKeyChanged(pixabayApiKeyTextInput.text);
        bridge.onPixabayMostUsedPerImageChanged(pixabayImageCountSpinBox.value);
        bridge.onSettingsWindowClosed();
    }
}
