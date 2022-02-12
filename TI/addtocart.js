const url = 'https://www.ti.com/occservices/v2/ti/addtocart'
const data = {
    "cartRequestList": [
        {
            "packageOption": "CTX",
            "opnId": "LM358DR",
            "quantity": "1",
            "tiAddtoCartSource": "store-pdp",
            "sparam": ""
        }
    ],
    "currency": "USD"
}
fetch(url, {
    headers: {
        "content-type": "application/json",
    },
    method: "POST",
    mode: "cors",
    credentials: "include",
    body: JSON.stringify(data),
})
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error)
    })