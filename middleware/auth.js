const jwt = require("jsonwebtoken");

const auth = (req, res, next) => {
  try {
    const token = req.header("x-auth-token");
    
    //401 code is for unauthorized
    if (!token)
      return res
        .status(401)
        .json({ msg: "No authentication token, authorization denied." });

    const verified = jwt.verify(token, process.env.JWT_SECRET);
    if (!verified)
      return res
        .status(401)
        .json({ msg: "Token verification failed, authorization denied." });

    req.user = verified.id; //returns the mongodb id of the user object
    next();
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

module.exports = auth; //export auth as a "module" to be used for other parts of the project
