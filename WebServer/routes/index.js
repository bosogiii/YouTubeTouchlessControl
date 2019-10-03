var express = require('express');
var router = express.Router();
var videos = require('../videos');
/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index2', { title: 'Express' });
});



// //YOUTUBE DATA API v3. Search
// //help for params : https://developers.google.com/youtube/v3/docs/search/list#--

// var request=require('request');
// var optionParams={
// 	q:"코코몽",
// 	part:"id",
// 	key:"AIzaSyD00N6Vnz9LFFQafkO-EVvGLnGeQtf4hcU",
// 	type:"video",
// 	maxResults:10,
// 	regionCode:"KR",
// 	videoDuration:"short"
//  };

// //한글을 검색어로 전달하기 위해선 url encoding 필요!
// optionParams.q=encodeURI(optionParams.q);

// var url="https://www.googleapis.com/youtube/v3/search?";
// for(var option in optionParams){
// 	url+=option+"="+optionParams[option]+"&";
// }

// //url의마지막에 붙어있는 & 정리
// url=url.substr(0, url.length-1);

// request(url, function(err, res, body){
// 	// console.log(body)
	
// 	//json형식을 서버로 부터 받음
// 	//console.log(body);
// 	var data=JSON.parse(body).items;
// 	for(var content in data){
// 		//youtube downloader에 videoId 넘기면 됨.
// 		//console.log(data[content].snippet.title+" : "+data[content].id.videoId);
// 		console.log(data[content].id.videoId);
//     	videos.vList.push(data[content].id.videoId);
// 	}

// 	console.log("HIHIHI");
//  //    for (let atom of videos.vList) {
//  //    	console.log(atom);
// 	// }
// 	var pplist = videos.vList
// 	console.log(pplist);
// });



module.exports = router;
