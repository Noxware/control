import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    property string file

    ColumnLayout {
        anchors.centerIn: parent
        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

        Text {
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            text: qsTr("Fallback viewer for file: '") + file + "'"
        }
        Button {
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            text: qsTr('View in external app')
            onClicked: {
                backend.view_external_file(file)
            }
        }
    }


}
