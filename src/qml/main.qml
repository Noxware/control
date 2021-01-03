import QtQuick 2.15
import QtQuick.Controls 2.15
import 'player'

ApplicationWindow {
    id: root
    width: 900
    height: 700
    title: qsTr('Control - Organizer')
    visible: true

    readonly property var typeToViewer: {
        'a': Text
    }

    /*menuBar: MenuBar {
        Menu {
            title: qsTr("&File")
            Action { text: qsTr("&New...") }
            Action { text: qsTr("&Open...") }
            Action { text: qsTr("&Save") }
            Action { text: qsTr("Save &As...") }
            MenuSeparator { }
            Action { text: qsTr("&Quit") }
        }
        Menu {
            title: qsTr("&Edit")
            Action { text: qsTr("Cu&t") }
            Action { text: qsTr("&Copy") }
            Action { text: qsTr("&Paste") }
        }
        Menu {
            title: qsTr("&Help")
            Action { text: qsTr("&About") }
        }
    }*/

    SplitView {
        anchors.fill: parent
        Rectangle {
            SplitView.fillWidth: true
            color: 'red'
        }

        Rectangle {
            color: 'blue'
            SplitView.preferredWidth: 250
            SplitView.minimumWidth: 200
            Player {
                anchors.centerIn: parent
                file: JSON.stringify(backend.data)
            }
        }
    }
}
