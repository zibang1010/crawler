(function () {
    'use strict';

    Object.defineProperties(window.navigator, {
        /*
        activeVRDisplays: {
            configurable: true,
            enumerable: true,
            get: function getActiveVRDisplays() {
                console.log("[ALERT] " + window.location.hostname + " accessed property Navigator.activeVRDisplays");
                return fakeActiveVRDisplaysValue;
            }
        },
        */

        appCodeName: {
            configurable: true,
            enumerable: true,
            get: function getAppCodeName() {
                console.log("[ALERT] " + window.location.hostname + " accessed property Navigator.appCodeName");

                return fakeAppCodeNameValue;
            }
        },
        appName: {
            configurable: true,
            enumerable: true,
            get: function getAppName() {
                console.log("[ALERT] " + window.location.hostname + " accessed property Navigator.appName");

                return fakeAppNameValue;
            }
        },
        appVersion: {
            configurable: true,
            enumerable: true,
            get: function getAppVersion() {
                console.log("[ALERT] " + window.location.hostname + " accessed property Navigator.appVersion");

                return fakeAppVersionValue;
            }
        },

        // TODO: This is getBattery() now
        /*
        battery: {
            configurable: true,
            enumerable: true,
            get: function getBattery() {
                console.log("[ALERT] " + window.location.hostname + " accessed property Navigator.battery");
                return fakeBatteryValue;
            }
        },
        connection: {
            configurable: true,
            enumerable: true,
            get: function getConnection() {
                console.log("[ALERT] " + window.location.hostname + " accessed property Navigator.connection");
                return fakeConnectionValue;
            }
        },
        geolocation: {
            configurable: true,
            enumerable: true,
            get: function getGeoLocation() {
                console.log("[ALERT] " + window.location.hostname + " accessed property Navigator.geolocation");
                return fakeGeoLocationValue;
            }
        },
        */

        hardwareConcurrency: {
            configurable: true,
            enumerable: true,
            get: function getHardwareConcurrency() {
                console.log("[ALERT] " + window.location.hostname + " accessed property Navigator.hardwareConcurrency");

                return fakeHardwareConcurrencyValue;
            }
        },

        /*
        javaEnabled: {
            configurable: true,
            enumerable: true,
            value: function getJavaEnabled() {
                console.log("[ALERT] " + window.location.hostname + " accessed property Navigator.javaEnabled");
                return fakeJavaEnabledValue;
            }
        },
        */

        language: {
            configurable: true,
            enumerable: true,
            get: function getLanguage() {
                console.log("[ALERT] " + window.location.hostname + " accessed property Navigator.language");

                return fakeLanguageValue;
            }
        },
        languages: {
            configurable: true,
            enumerable: true,
            get: function getLanguages() {
                console.log("[ALERT] " + window.location.hostname + " accessed property Navigator.languages");

                return fakeLanguagesValue;
            }
        },

        /*
        mimeTypes: {
            configurable: true,
            enumerable: true,
            get: function getMimeTypes() {
                console.log("[ALERT] " + window.location.hostname + " accessed property Navigator.mimeTypes");
                return fakeMimeTypesValue;
            }
        },
        */

        onLine: {
            configurable: true,
            enumerable: true,
            get: function getOnLine() {
                console.log("[ALERT] " + window.location.hostname + " accessed property Navigator.onLine");

                return fakeOnLineValue;
            }
        },
        oscpu: {
            configurable: true,
            enumerable: true,
            get: function getOscpu() {
                console.log("[ALERT] " + window.location.hostname + " accessed property Navigator.oscpu");

                return fakeOscpuValue;
            }
        },

        /*
        permissions: {
            configurable: true,
            enumerable: true,
            get: function getPermissions() {
                console.log("[ALERT] " + window.location.hostname + " accessed property Navigator.permissions");
                return fakePermissionsValue;
            }
        },
        */

        platform: {
            configurable: true,
            enumerable: true,
            get: function getPlatform() {
                console.log("[ALERT] " + window.location.hostname + " accessed property Navigator.platform");

                return fakePlatformValue;
            }
        },

        /*
        plugins: {
            configurable: true,
            enumerable: true,
            get: function getPlugins() {
                console.log("[ALERT] " + window.location.hostname + " accessed property Navigator.plugins");
                return fakePluginsValue;
            }
        },
        */

        product: {
            configurable: true,
            enumerable: true,
            get: function getProduct() {
                console.log("[ALERT] " + window.location.hostname + " accessed property Navigator.product");

                return fakeProductValue;
            }
        },

        /*
        serviceWorker: {
            configurable: true,
            enumerable: true,
            get: function getServiceWorker() {
                console.log("[ALERT] " + window.location.hostname + " accessed property Navigator.serviceWorker");
                return fakeServiceWorkerValue;
            }
        },
        storage: {
            configurable: true,
            enumerable: true,
            get: function getStorage() {
                console.log("[ALERT] " + window.location.hostname + " accessed property Navigator.storage");
                return fakeStorageValue;
            }
        },
        */

        userAgent: {
            configurable: true,
            enumerable: true,
            get: function getUserAgent() {
                console.log("[ALERT] " + window.location.hostname + " accessed property Navigator.userAgent");

                return fakeUserAgentValue;
            }
        },
        buildID: {
            configurable: true,
            enumerable: true,
            get: function getBuildID() {
                console.log("[ALERT] " + window.location.hostname + " accessed property Navigator.buildID");

                return fakeBuildIDValue;
            }
        }
    });
})();