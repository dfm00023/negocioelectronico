document.addEventListener("DOMContentLoaded", function () {
    function leer_etiqueta(input) {
        if ('NDEFReader' in window) {
            const ndef = new NDEFReader();
            ndef.scan().then(() => {
                console.log("Escaneo NFC iniciado.");
                document.getElementById(input).value = "Escaneando NFC...";

                ndef.onreadingerror = () => {
                    console.log("No se puede leer la etiqueta NFC. Intenta con otra.");
                    document.getElementById(input).value = "Error de lectura NFC";
                };

                ndef.onreading = event => {
                    console.log("Etiqueta NFC detectada.");
                    console.log("Serial Number:", event.serialNumber);
                    document.getElementById(input).value = event.serialNumber;
                };
            }).catch(error => {
                console.log(`Error: No se pudo iniciar el escaneo NFC - ${error}`);
                document.getElementById(input).value = "Escaneo NFC fallido";
            });
        } else {
            console.log("NFC no es compatible con este dispositivo.");
            document.getElementById(input).value = "NFC no soportado";
        }
    }

    // Hacer la función accesible desde el botón
    window.leer_etiqueta = leer_etiqueta;
});

// const ndef = new NDEFReader();
// ndef.scan().then(() => {
//     console.log("Scan started successfully.");
//     ndef.onreadingerror = () => {
//         console.log("Cannot read data from the NFC tag. Try another one?");
//     };
//     ndef.onreading = event => {
//         console.log("NDEF message read.");
//     };
// }).catch(error => {
//     console.log(`Error! Scan failed to start: ${error}.`);
// });