(() => {
    "use strict";
// This file contains utils that are build and included on the window object with some randomized prefix.
// some protections can mess with these to prevent the overrides - our script is first so we can reference the old values.
    const cache = {
        Reflect: {
            get: Reflect.get.bind(Reflect),
            apply: Reflect.apply.bind(Reflect),
        },
        // Used in `makeNativeString`
        nativeToStringStr: `${Function.toString}`, // => `function toString() { [native code] }`
    };

    /**
     * @param {object} masterObject - Object ot override
     * @param {string} propertyName - property to override
     * @param {function} proxyHandler - proxy handled with the new value
     */
    function overridePropertyWithProxy(masterObject, propertyName, proxyHandler) {
        const originalObject = masterObject[propertyName];
        const proxy = new Proxy(masterObject[propertyName], stripProxyFromErrors(proxyHandler));
        redefineProperty(masterObject, propertyName, {value: proxy});
        redirectToString(proxy, originalObject);
    }

    /**
     * @param {object} masterObject - Object ot override
     * @param {string} propertyName - property to override
     * @param {function} proxyHandler - proxy handled with getter handler
     */
    function overrideGetterWithProxy(masterObject, propertyName, proxyHandler) {
        const fn = Object.getOwnPropertyDescriptor(masterObject, propertyName).get;
        const fnStr = fn.toString(); // special getter function string
        const proxyObj = new Proxy(fn, stripProxyFromErrors(proxyHandler));
        redefineProperty(masterObject, propertyName, {get: proxyObj});
        redirectToString(proxyObj, fnStr);
    }

    /**
     * @param {Object} instance - instance to override such as navigator.
     * @param {Object} overrideObj - new instance values such as userAgent.
     */
// eslint-disable-next-line no-unused-vars
    function overrideInstancePrototype(instance, overrideObj) {
        Object.keys(overrideObj).forEach((key) => {
            try {
                overrideGetterWithProxy(Object.getPrototypeOf(instance), key, makeHandler().getterValue(overrideObj[key]));
            } catch (e) {
                console.error(`Could not override property: ${key} on ${instance}. Reason: ${e.message} `);
            }
        });
    }

    function redirectToString(proxyObj, originalObj) {
        const handler = {
            apply(target, ctx) {
                // This fixes e.g. `HTMLMediaElement.prototype.canPlayType.toString + ""`
                if (ctx === Function.prototype.toString) {
                    return makeNativeString('toString');
                }
                // `toString` targeted at our proxied Object detected
                if (ctx === proxyObj) {
                    const fallback = () => (originalObj && originalObj.name
                        ? makeNativeString(originalObj.name)
                        : makeNativeString(proxyObj.name));
                    // Return the toString representation of our original object if possible
                    return `${originalObj}` || fallback();
                }
                // Check if the toString prototype of the context is the same as the global prototype,
                // if not indicates that we are doing a check across different windows., e.g. the iframeWithdirect` test case
                const hasSameProto = Object.getPrototypeOf(Function.prototype.toString).isPrototypeOf(ctx.toString); // eslint-disable-line no-prototype-builtins
                if (!hasSameProto) {
                    // Pass the call on to the local Function.prototype.toString instead
                    return ctx.toString();
                }
                return target.call(ctx);
            },
        };
        const toStringProxy = new Proxy(Function.prototype.toString, stripProxyFromErrors(handler));
        redefineProperty(Function.prototype, 'toString', {
            value: toStringProxy,
        });
    }

    function makeNativeString(name = '') {
        return cache.nativeToStringStr.replace('toString', name || '');
    }

    function redefineProperty(masterObject, propertyName, descriptorOverrides = {}) {
        return Object.defineProperty(masterObject, propertyName, {
            // Copy over the existing descriptors (writable, enumerable, configurable, etc)
            ...(Object.getOwnPropertyDescriptor(masterObject, propertyName) || {}),
            // Add our overrides (e.g. value, get())
            ...descriptorOverrides,
        });
    }

    function stripProxyFromErrors(handler) {
        const newHandler = {};
        // We wrap each trap in the handler in a try/catch and modify the error stack if they throw
        const traps = Object.getOwnPropertyNames(handler);
        traps.forEach((trap) => {
            newHandler[trap] = function () {
                try {
                    // Forward the call to the defined proxy handler
                    return handler[trap].apply(this, arguments || []); //eslint-disable-line
                } catch (err) {
                    // Stack traces differ per browser, we only support chromium based ones currently
                    if (!err || !err.stack || !err.stack.includes(`at `)) {
                        throw err;
                    }
                    // When something throws within one of our traps the Proxy will show up in error stacks
                    // An earlier implementation of this code would simply strip lines with a blacklist,
                    // but it makes sense to be more surgical here and only remove lines related to our Proxy.
                    // We try to use a known "anchor" line for that and strip it with everything above it.
                    // If the anchor line cannot be found for some reason we fall back to our blacklist approach.
                    const stripWithBlacklist = (stack, stripFirstLine = true) => {
                        const blacklist = [
                            `at Reflect.${trap} `,
                            `at Object.${trap} `,
                            `at Object.newHandler.<computed> [as ${trap}] `, // caused by this very wrapper :-)
                        ];
                        return (err.stack
                            .split('\n')
                            // Always remove the first (file) line in the stack (guaranteed to be our proxy)
                            .filter((line, index) => !(index === 1 && stripFirstLine))
                            // Check if the line starts with one of our blacklisted strings
                            .filter((line) => !blacklist.some((bl) => line.trim().startsWith(bl)))
                            .join('\n'));
                    };
                    const stripWithAnchor = (stack, anchor) => {
                        const stackArr = stack.split('\n');
                        anchor = anchor || `at Object.newHandler.<computed> [as ${trap}] `; // Known first Proxy line in chromium
                        const anchorIndex = stackArr.findIndex((line) => line.trim().startsWith(anchor));
                        if (anchorIndex === -1) {
                            return false; // 404, anchor not found
                        }
                        // Strip everything from the top until we reach the anchor line
                        // Note: We're keeping the 1st line (zero index) as it's unrelated (e.g. `TypeError`)
                        stackArr.splice(1, anchorIndex);
                        return stackArr.join('\n');
                    };
                    // Special cases due to our nested toString proxies
                    err.stack = err.stack.replace('at Object.toString (', 'at Function.toString (');
                    if ((err.stack || '').includes('at Function.toString (')) {
                        err.stack = stripWithBlacklist(err.stack, false);
                        throw err;
                    }
                    // Try using the anchor method, fallback to blacklist if necessary
                    err.stack = stripWithAnchor(err.stack) || stripWithBlacklist(err.stack);
                    throw err; // Re-throw our now sanitized error
                }
            };
        });
        return newHandler;
    }

// eslint-disable-next-line no-unused-vars
    function overrideWebGl(webGl) {
        // try to override WebGl
        try {
            // Remove traces of our Proxy
            const stripErrorStack = (stack) => stack
                .split('\n')
                .filter((line) => !line.includes('at Object.apply'))
                .filter((line) => !line.includes('at Object.get'))
                .join('\n');
            const getParameterProxyHandler = {
                get(target, key) {
                    try {
                        // Mitigate Chromium bug (#130)
                        if (typeof target[key] === 'function') {
                            return target[key].bind(target);
                        }
                        return Reflect.get(target, key);
                    } catch (err) {
                        err.stack = stripErrorStack(err.stack);
                        throw err;
                    }
                },
                apply(target, thisArg, args) {
                    const param = (args || [])[0];
                    // UNMASKED_VENDOR_WEBGL
                    if (param === 37445) {
                        return webGl.vendor;
                    }
                    // UNMASKED_RENDERER_WEBGL
                    if (param === 37446) {
                        return webGl.renderer;
                    }
                    try {
                        return cache.Reflect.apply(target, thisArg, args);
                    } catch (err) {
                        err.stack = stripErrorStack(err.stack);
                        throw err;
                    }
                },
            };
            const addProxy = (obj, propName) => {
                overridePropertyWithProxy(obj, propName, getParameterProxyHandler);
            };
            addProxy(WebGLRenderingContext.prototype, 'getParameter');
            addProxy(WebGL2RenderingContext.prototype, 'getParameter');
        } catch (err) {
            console.warn(err);
        }
    }

// eslint-disable-next-line no-unused-vars
    const overrideCodecs = (audioCodecs, videoCodecs) => {
        const codecs = {
            ...audioCodecs,
            ...videoCodecs,
        };
        const findCodec = (codecString) => {
            for (const [name, state] of Object.entries(codecs)) {
                const codec = {name, state};
                if (codecString.includes(codec.name)) {
                    return codec;
                }
            }
        };
        const canPlayType = {
            // eslint-disable-next-line
            apply: function (target, ctx, args) {
                if (!args || !args.length) {
                    return target.apply(ctx, args);
                }
                const [codecString] = args;
                const codec = findCodec(codecString);
                if (codec) {
                    return codec.state;
                }
                // If the codec is not in our collected data use
                return target.apply(ctx, args);
            },
        };
        overridePropertyWithProxy(HTMLMediaElement.prototype, 'canPlayType', canPlayType);
    };

// eslint-disable-next-line no-unused-vars
    function overrideBattery(batteryInfo) {
        const getBattery = {
            // eslint-disable-next-line
            apply: async function () {
                return batteryInfo;
            },
        };
        overridePropertyWithProxy(Object.getPrototypeOf(navigator), 'getBattery', getBattery);
    }

    function makeHandler() {
        return {
            // Used by simple `navigator` getter evasions
            getterValue: (value) => ({
                apply(target, ctx, args) {
                    // Let's fetch the value first, to trigger and escalate potential errors
                    // Illegal invocations like `navigator.__proto__.vendor` will throw here
                    const ret = cache.Reflect.apply(...arguments); // eslint-disable-line
                    if (args && args.length === 0) {
                        return value;
                    }
                    return ret;
                },
            }),
        };
    };

//# sourceMappingURL=utils.js.map

    const fp = {
        "screen": {"availHeight": 1901, "availWidth": 1030, "pixelDepth": 30, "height": 1901, "width": 1069},
        "navigator": {
            "cookieEnabled": true,
            "doNotTrack": "1",
            "language": "zh-CN",
            "languages": ["zh-CN", "zh"],
            "platform": "Win32",
            "deviceMemory": 8,
            "hardwareConcurrency": 8,
            "productSub": "20030107",
            "vendor": "Google Inc.",
            "maxTouchPoints": 0
        },
        "webGl": {
            "vendor": "Google Inc. (NVIDIA)",
            "renderer": "ANGLE (NVIDIA, NVIDIA GeForce GTX 1650 SUPER Direct3D11 vs_5_0 ps_5_0, D3D11-27.21.14.6137)"
        },
        "audioCodecs": {"ogg": "probably", "mp3": "probably", "wav": "probably", "m4a": "maybe", "aac": "probably"},
        "videoCodecs": {"ogg": "probably", "h264": "probably", "webm": "probably"},
        "pluginsData": {
            "mimeTypes": ["~~application/pdf~~pdf", "Portable Document Format~~application/x-google-chrome-pdf~~pdf", "Native Client Executable~~application/x-nacl~~", "Portable Native Client Executable~~application/x-pnacl~~"],
            "plugins": [{
                "name": "Chrome PDF Plugin",
                "description": "Portable Document Format",
                "mimeTypes": [{"type": "application/x-google-chrome-pdf", "suffixes": "pdf"}]
            }, {
                "name": "Chrome PDF Viewer",
                "description": "",
                "mimeTypes": [{"type": "application/pdf", "suffixes": "pdf"}]
            }, {
                "name": "Native Client",
                "description": "",
                "mimeTypes": [{"type": "application/x-nacl", "suffixes": ""}, {
                    "type": "application/x-pnacl",
                    "suffixes": ""
                }]
            }]
        },
        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
        "battery": true
    };
    (function inject() {

        // @ts-expect-error Internal browser code for injection

        const {batteryInfo, navigator: newNav, screen: newScreen, webGl, historyLength, audioCodecs, videoCodecs} = fp;

        // override navigator

        // @ts-expect-error Internal browser code for injection

        overrideInstancePrototype(window.navigator, newNav);

        // override screen

        // @ts-expect-error Internal browser code for injection

        overrideInstancePrototype(window.screen, newScreen);

        // @ts-expect-error Internal browser code for injection

        overrideInstancePrototype(window.history, {length: historyLength});

        // override webGl

        // @TODO: Find another way out of this.

        // This feels like a dirty hack, but without this it throws while running tests.

        // eslint-disable-next-line @typescript-eslint/ban-ts-comment

        // @ts-ignore Internal browser code for injection

        overrideWebGl(webGl);

        // override codecs

        // eslint-disable-next-line @typescript-eslint/ban-ts-comment

        // @ts-ignore Internal browser code for injection

        overrideCodecs(audioCodecs, videoCodecs);

        // override batteryInfo

        // eslint-disable-next-line @typescript-eslint/ban-ts-comment

        // @ts-ignore Internal browser code for injection

        overrideBattery(batteryInfo);

    })()
})()