const mongoose = require("mongoose");

const productSchema = new mongoose.Schema({
    // username: { type: String, required: true, unique: true },
    // email: { type: String, required: true, unique: true },
    // password: { type: String, required: true, minlength: 5 },
    // displayName: { type: String },
    shopifyID :{ type: String, required: true, unique: true},
    upc: { type: String, required: true },
    sku: {type: String, required:true},
    title: {type: String},
    retail: {type: String},
    discounted_price: {type: String},
    image: {type: String},
    description: {type: String},
    condition: {type:String},
    categories: [{type: String}],
    quantity: {type: String}
},{ timestamps: true });

module.exports = Products = mongoose.model("products", productSchema);






// So Model.find() returns an instance of the Query class. 
// You can chain find() calls to add additional query operators, 
// also known as filters, to the query. For example, both of 
// the following queries will find all customers whose email 
// contains 'foo.bar' and whose age is at least 30.

// // First parameter to `find()` is an object that contains query operators, see:
// // https://docs.mongodb.com/manual/reference/operator/query/
// Customer.find({ email: /foo\.bar/, age: { $gte: 30 } });
// // Equivalent:
// Customer.find({ email: /foo\.bar/ }).find({ age: { $gte: 30 } });


// The sort(), limit(), and skip() helpers modify 
//the query's options. For example, query.getOptions() 
//below will return an object that contains sort and limit properties.

// const query = Customer.find().sort({ name: 1 }).limit(1);
// query.getOptions(); // { sort: { name: 1 }, limit: 1 }