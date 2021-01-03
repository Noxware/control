import QtQuick 2.15
import QtQuick.Controls 2.15
import 'player'

ApplicationWindow {
    id: root
    width: 900
    height: 700
    title: qsTr('Control - Organizer')
    visible: true

    property var snapshot

    function updateSnapshot() {
        root.snapshot = backend.wait_for_snapshot();
        if (!root.snapshot) {
            Qt.quit();
        }
    }

    Component.onCompleted: {
        updateSnapshot();
    }

    SplitView {
        anchors.fill: parent
        Player {
            SplitView.fillWidth: true
            file: snapshot.file
        }

        ListView {
            model: snapshot.options
            delegate: Button {
                    width: parent.width
                    height: 40
                    text: snapshot.options[index].name
                    onClicked: {
                        backend.select(snapshot.options[index].name)
                        root.updateSnapshot()
                    }
            }
            SplitView.preferredWidth: 250
            SplitView.minimumWidth: 200
        }
    }
}
