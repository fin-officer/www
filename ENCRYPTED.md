Creating a MHTML file that can rewrite itself through a local Node.js script isn't straightforward because MHTML files are created by web browsers to capture full webpage (including HTML, images, CSS, JavaScript, etc.) into a single file. These files are not meant to be self-modifiable. But if your intention is to handle raw MHTML data and modify it somehow through a Node.js script, you can create the following script that reads and rewrites the MHTML file.

Here's how you would do it:

1. Create the Node.js Script:

First, you should have Node.js installed on your machine. If not installed, download from the official site [here](https://nodejs.org/en/download/).

Next, create a new file - "rewrite.js" - and use the fs (file system) package that comes bundled with Node.js to read, modify, and save your MHTML file.

```javascript
var fs = require('fs');

fs.readFile('path_to_your_file/sample.mhtml', 'utf8', function(err, data){
   if (err) {
      return console.error(err);
   }

   var result = data.replace(/old_content/g, 'new_content');

   fs.writeFile('path_to_your_file/sample.mhtml', result, 'utf8', function(err){
      if (err) return console.error(err);
      console.log('File rewrite successfully!');
   });
});
```

This script would:
- Read your MHTML file.
- Replace 'old_content' with 'new_content' in the file (you should define 'old_content' and 'new_content' as per your modification needs).
- Write the changes back to the MHTML file.

2. Run the Node.js Script:

Open terminal, navigate to your "rewrite.js" file directory, and run:

```bash
node rewrite.js
```

Again, this is a simplified approach. It may not work as expected if your MHTML file contains complex or encoded data. In more complex scenarios, you'd need to parse the MHTML content properly before modifying and rebuilding it. This typically requires a more advanced understanding of the MHTML format and coding experience with Node.js. Consider consulting with a software architect or a skilled programmer if required.



----



To encrypt or decrypt the MHTML file, you can use the crypto module in Node.js. To handle multipart splitting, you can parse the MHTML data.

Please refer to the following simplified example:

```javascript
const fs = require('fs');
const crypto = require('crypto');

// Provide your secret
const secret = 'your-secret-key';

function encrypt(text) {
    const cipher = crypto.createCipher('aes-256-ctr', secret);
    let crypted = cipher.update(text, 'utf8', 'hex');
    crypted += cipher.final('hex');
    return crypted;
}

function decrypt(text) {
    const decipher = crypto.createDecipher('aes-256-ctr', secret)
    let dec = decipher.update(text, 'hex', 'utf8')
    dec += decipher.final('utf8');
    return dec;
}

fs.readFile('./file.mhtml', 'utf8', function(err, data) {
    if (err) {
        return console.log(err);
    }

    // split multipart
    let multipartData = data.split("\n--"); // split by boundary

    // encrypt and then decrypt each part
    multipartData = multipartData.map(part => {
        const encrypted = encrypt(part);
        const decrypted = decrypt(encrypted);

        // perform your modification here
        // ...

        return decrypted;
    });

    // merge and overwrite the mhtml file
    fs.writeFile('./file.mhtml', multipartData.join("\n--"), 'utf8', function(err) {
        if (err) return console.log(err);
        console.log('Successfully re-wrote the MHTML file');
    });
});
```

In this script, the MHTML data is read, encrypted, decrypted, (you can modify it here as per your need), joined again and then written back to the MHTML file.

Make sure that you install Node crypto module by running `npm install crypto` in the terminal. 

Note: This is a simplified representation and may not work perfectly with complex MHTML data. You might need a real parser for MHTML to handle all edge cases, which are not covered by just splitting by newlines and "--". Please consider using a library/package if you need to work frequently or intensely with MHTML files. 

Also, ensure you are legally allowed to decrypt or encrypt files, and working with any sensitive data complies with GDPR or other data protection regulations applicable in your geographical location or your industry.



---





Creating a frontend in HTML essentially means allowing users to upload MHTML files for encryption or decryption through a webpage, handled by the backend (Node.js).

Firstly, create an HTML form where the user can upload a file:

```html
<!DOCTYPE html>
<html>
<body>

<h2>File Upload</h2>

<form action="/upload" method="post" enctype="multipart/form-data">
  Select file to upload:
  <input type="file" name="fileToUpload" id="fileToUpload">
  <input type="submit" value="Upload File" name="submit">
</form>

</body>
</html>
```

Then on the Node.js server side, you need to handle this file upload. You can use modules like Express and Multer to do this elegantly:

```nodejs
const express = require('express');
const multer  = require('multer');
const crypto = require('crypto');
const fs = require('fs');
const app = express();
const upload = multer({ dest: 'uploads/' }); //create a folder named "uploads" in the root directory beforehand

// Provide your secret
const secret = 'your-secret-key';

function encrypt(text) {
  const cipher = crypto.createCipher('aes-256-ctr', secret);
  let crypted = cipher.update(text, 'utf8', 'hex');
  crypted += cipher.final('hex');
  return crypted;
}

function decrypt(text) {
  const decipher = crypto.createDecipher('aes-256-ctr', secret)
  let dec = decipher.update(text, 'hex', 'utf8')
  dec += decipher.final('utf8');
  return dec;
}

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html'); 
});

app.post('/upload', upload.single('fileToUpload'), (req, res) => {
  let filePath = req.file.path;
  fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
      return res.send('Error: Couldn’t read file');
    }
    const encryptedData = encrypt(data);
    const decryptedData = decrypt(encryptedData);
    // In this stage, the decrypted data can be saved back to a file
    // perform operations to the file here

    fs.writeFile(filePath, decryptedData, 'utf8', err => {
      if (err) {
        return res.send('Error: Couldn’t write file');
      }
      res.send('File processed successfully');
    });
  });
});

app.listen(3000, () => {
  console.log('Server started on port 3000');
});
```

Please note that the code provided above is meant to illustrate a simple case. In any production system, steps for error handling and security measures should be added.

Also, this code requires the multer and express modules. You can install them using npm:

```bash
npm install express multer
```

Make sure to save your 'index.html' file and 'server.js' (or whatever name you gave to your server script) in the same folder. Then run your node.js server:

```bash
node server.js
```

Now you can go to `localhost:3000` in your browser, and you'll be able to upload a file for it to be encrypted and decrypted in your backend.
