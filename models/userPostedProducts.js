const mongoose = require("mongoose");

const userProductSchema = new mongoose.Schema({
    posted_products: {type: String, required: true, unique: true}, //db or shopify id
    username: {type: String, required: true}    
},{ timestamps: true });

module.exports = UserProducts = mongoose.model("userPostedProducts", userProductSchema);