const router = require("express").Router();
const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");
const auth = require("../middleware/auth");
const User = require("../models/userModel");

router.post("/register", async (req, res) => {
  try {
    let { username, email, password, passwordCheck, displayName } = req.body;

    // validate
    const existingUser = await User.findOne({ username: username });
    if (existingUser)
      return res
        .status(400)
        .json({ msg: "An account with this username already exists." });

    if (!username || !email || !password || !passwordCheck)
      return res.status(400).json({ msg: "Not all fields have been entered." });
    if (!/^[_A-z0-9]{1,}$/.test(username))
      return res.status(400).json({ msg: "Username cannot have whitespace/invalid characters" });
    if (password.length < 8)
      return res
        .status(400)
        .json({ msg: "The password needs to be at least 5 characters long." });
    if (password !== passwordCheck)
      return res
        .status(400)
        .json({ msg: "Enter the same password twice for verification." });
    if(!/[^A-Za-z0-9]/.test(password)) {
        return res
        .status(400)
        .json({msg:"Password must contain atleast one special character"});
    }
    

    if (!displayName) displayName = username;

    const salt = await bcrypt.genSalt(); //asynchronous operation
    const passwordHash = await bcrypt.hash(password, salt); // the official bcryptjs documentation has a different way to implement this. 

    const newUser = new User({
      username,
      email,
      password: passwordHash,
      displayName,
    });
    const savedUser = await newUser.save();
    res.json(savedUser);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

router.post("/login", async (req, res) => {
  try {
    const { username, password } = req.body;

    // validate
    if (!username || !password)
      return res.status(400).json({ msg: "Please enter the username/password" });

    const user = await User.findOne({ username: username });
    if (!user)
      return res
        .status(400)
        .json({ msg: "User does not exist" });

    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch) return res.status(400).json({ msg: "Invalid credentials." });

    const token = jwt.sign({ id: user._id }, process.env.JWT_SECRET);
    res.json({
      token,
      user: {
        id: user._id,
        displayName: user.displayName,
        username: user.username,
        email: user.email
      },
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

router.delete("/delete", auth, async (req, res) => {
  try {
    const deletedUser = await User.findByIdAndDelete(req.user);
    res.json(deletedUser);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

router.post("/tokenIsValid", async (req, res) => {
  try {
    const token = req.header("x-auth-token");
    if (!token) return res.json(false); //we could have also used 401 code here too

    const verified = jwt.verify(token, process.env.JWT_SECRET);
    if (!verified) return res.json(false);

    const user = await User.findById(verified.id);
    if (!user) return res.json(false);
    
    return res.json(true);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

router.get("/", auth, async (req, res) => {
  const user = await User.findById(req.user);
  res.json({
    displayName: user.displayName,
    username: user.username,
    id: user._id,
  });
});

router.get("/test",(req,res)=>{
    res.send("Awesomeness")
})

module.exports = router;