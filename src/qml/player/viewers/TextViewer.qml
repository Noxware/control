import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    anchors.fill: parent

    property string file

    ScrollView {
        anchors.fill: parent
        TextArea {
            text: backend.get_file_content(file)
            readOnly: true
            selectByMouse: true
        }
    }


}
