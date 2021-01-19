const router = require("express").Router();
const auth = require("../middleware/auth");
const User = require("../models/userModel");
const { PythonShell } = require('python-shell');
const path = require('path');
const Products = require("../models/productModel");
const UserProducts = require("../models/userPostedProducts");
const axios = require('axios')

function isAsin(strText) {
    var asinPattern = new RegExp(/^(B[\dA-Z]{9}|\d{9}(X|\d))$/);
    var arrMatches = strText.match(asinPattern);

    if (arrMatches[0] == strText) {
        return true;
    }
    return false;
}

router.post("/new", auth, async (req, res) => {
    try {
    
        let { username, productInp } = req.body;
        // console.log(user)
        // console.log(productInp.title)
        //aage shopify te product pathao
        //then db te dhukao
        // const image = "https://cdn.shopify.com/s/files/1/0514/3520/8854/files/surplus-auction.png?v=1609197903"
        const api_url = "https://d5564278b7264d6ad974c0f10a2603c0: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@blitz-stock.myshopify.com/admin/api/2021-01/products.json"

        // if (productInp.image !== "") {
        //     image = productInp.image
        // }


        var productString = JSON.stringify(productInp)

        let options = {
            mode: 'json',
            pythonPath: process.env.PYTHON_PATH,
            pythonOptions: ['-u'], // get print results in real-time 
            scriptPath: path.join(__dirname, '../python'), //If you are having python_test.py script in same folder, then it's optional. 
            args: [productString, api_url] //An argument which can be accessed in the script using sys.argv[1] 
        };
        PythonShell.run('shopifyUpload.py', options, function (err, result) {
            if (err) throw err;

            // console.log('result: ', result); 
            // res.send(result[0])
            // const response = await axios.post(api_url,productDetails)
            try {
                const resp = result[0]
                console.log(resp)
                const newProduct = new Products({
                    shopifyID: resp['product']['id'],
                    upc: productInp.upc,
                    sku: productInp.sku,
                    title: productInp.title,
                    retail: productInp.retail,
                    discounted_price: productInp.discounted_price,
                    image: productInp.image,
                    description: productInp.description,
                    condition: productInp.condition,
                    quantity: productInp.quantity,
                    categories: [""]
                });
                const savedProduct = newProduct.save();

                const newUserProduct = new UserProducts({
                    username: username,
                    posted_products: resp['product']['id']
                });

                const saveUserProduct = newUserProduct.save();

                res.json(resp)
            } catch (err) {
                res.status(500).json({ error: err.message })
            }
        });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }



})

router.post("/", auth, async (req, res) => {
    try {

        //at first get the query
        //then check whether it is a upc/asin or a text string with space
        //1. If UPC, then follow one process (Sellerchamp way, if this one works, then no search list should be generated in the front end)
        //2. If text string, then follow another process (Product Data API way)
        const { searchQuery, marketplace } = req.body;

        marketplaceString = JSON.stringify(marketplace)
        var query = searchQuery;
        // console.log(query)
        if (isAsin(query)) {
            // console.log("gaitai")
            let dir = path.join(__dirname, '../python');
            // console.log(dir)
            let options = {
                mode: 'json',
                pythonPath: process.env.PYTHON_PATH,
                pythonOptions: ['-u'], // get print results in real-time 
                scriptPath: path.join(__dirname, '../python'), //If you are having python_test.py script in same folder, then it's optional. 
                args: [query, marketplaceString] //An argument which can be accessed in the script using sys.argv[1] 
            };
            PythonShell.run('apiController.py', options, function (err, result) {
                if (err) throw err;
                // console.log('result: ', result); 
                res.send(result[0])
            });

        }
        else {
            res.send('Error')
        }
    } catch (err) {
        res.status(500).json({ error: err.message });
    }


});

router.get("/getsku", auth, async (req, res) => {
    Products.countDocuments({}, function (err, count) {
        count++;
        const sku = "BTZ" + count.toString().padStart(7, "0");
        res.json(sku)
    })
})

module.exports = router;