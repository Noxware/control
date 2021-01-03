// From my https://github.com/Noxware/qt-quick-flickable-and-zoomable-by-mouse-image-example

import QtQuick 2.15

Item {
    // Just some window configuration
    id: root
    anchors.fill: parent

    property string file

    // Important things!
    Flickable {
        anchors.fill: parent

        contentWidth: Math.max(image.width * image.scale, root.width)
        contentHeight: Math.max(image.height * image.scale, root.height)
        clip: true

        Image {
            id: image

            property real zoom: 0.0
            property real zoomStep: 0.1

            asynchronous: true
            cache: false
            smooth: true
            antialiasing: true
            mipmap: true

            anchors.centerIn: parent
            fillMode: Image.PreserveAspectFit
            transformOrigin: Item.Center
            scale: Math.min(root.width / width, root.height / height, 1) + zoom

            source: backend.url_from_file(file)
        }
    }

    // Mouse zoom
    MouseArea {
        anchors.fill: parent
        acceptedButtons: Qt.NoButton

        onWheel: {
            if (wheel.angleDelta.y > 0)
                image.zoom = Number((image.zoom + image.zoomStep).toFixed(1))
            else
                if (image.zoom > 0) image.zoom = Number((image.zoom - image.zoomStep).toFixed(1))

            wheel.accepted=true
        }
    }
}
