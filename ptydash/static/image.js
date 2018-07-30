/*
 * JavaScript to receive images over a websocket.
 *
 */

const ws = new WebSocket("ws://localhost:8888/data");
ws.binaryType = "arraybuffer";

ws.onopen = function () {
    ws.send("Hello Websocket!");
};

ws.onmessage = function (evt) {
    const data = JSON.parse(evt.data);

    const elements = document.getElementsByName('image');
    for (let i = 0; i < elements.length; i++) {
        const image = elements[i];
        const imageId = image.id;
        const base64 = data.images[imageId];

        if (base64 != null) {
            image.src = 'data:image/png;base64,' + base64;
        }
    }


    setTimeout(function() { ws.send("newfig") }, 1000);
};
