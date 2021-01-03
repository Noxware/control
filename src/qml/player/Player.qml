import QtQuick 2.15

Item {
    property string file

    Loader {
        anchors.fill: parent
        id: loader
    }


    onFileChanged: {
        var t = backend.get_file_type(file);
        console.log(file)

        if (t === 'image')
            loader.setSource('viewers/ImageViewer.qml', {'file': file});
        else if (t === 'text')
            loader.setSource('viewers/TextViewer.qml', {'file': file});
        else
            loader.setSource('viewers/FileViewer.qml', {'file': file});
    }
}
