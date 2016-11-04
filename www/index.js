// index.js

//fs = require('fs');
var express = require('express');
var app = express();

//fs.readFile('../rht03/current.txt', 'utf8', function (err,data) {
//  if (err) {
//    return console.log(err);
//  }
//  console.log(data);
//});
app.get('/', function (req, res) {
  //res.render('main'); //'data is: {$data}');
  res.sendfile('rht03/current.html');             // one line response
  // res.sendfile('index.html');     // or send a webpage you designed
});

var server = app.listen(90, function () {

  console.log('Node Express Webserver Started');

});
