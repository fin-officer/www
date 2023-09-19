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
