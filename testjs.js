var express = require('express');
var bodyParser = require('body-parser');


var app = express();

app.use(bodyParser.json()); // support json encoded bodies
app.use(bodyParser.urlencoded({ extended: true })); // support encoded bodies


app.post("/KRA",function(req, res){
	console.log(req.body)
	console.log(req.body.result)

	res.send(req.body)
});

const PORT = process.env.PORT || 8080;
app.listen(PORT, function(){
  console.log('App listening on port'+ PORT);
  console.log('Press Ctrl+C to quit.');
});
