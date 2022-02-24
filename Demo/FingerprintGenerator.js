const FingerprintGenerator = require('fingerprint-generator');
let fingerprintGenerator = new FingerprintGenerator({
        browsers: [
            {name: "firefox", minVersion: 80},
            {name: "chrome", minVersion: 87},
            "safari"
        ],
        devices: [
            "desktop"
        ],
        operatingSystems: [
            "windows"
        ]
});

console.log(fingerprintGenerator)