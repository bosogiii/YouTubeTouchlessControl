
# Youtube Touchless Controller
2019졸업프로젝트
한양대학교 구민우, 송보석
PythonServer(Hand Detection using Deep Learning) + WebServer(using Youtube API, Node.js)

## PythonServer

1.Detect Hand in the clip
2.Recognize the motion

Reference : https://github.com/MrEliptik/HandPose

## WebServer

1.Receive order from Python server(play,pause,mute,unmute,next,previous)
2.Send order to Client

### Server -> Client

서버->클라이언트 통신방법
1.소켓통신
2.Late pooling -> 해당 프로젝트에서 사용
```js
//server side
//client -> Node.js
app.get('/msg', function (req, res, next) {
    console.log('msg');
    session.resList.push(res);
});

//pythonServer -> Node.js
app.post('/gesture',function(req,res){
    var msg = req.body.msg;
    console.log("python: " + msg);
    let data = req.body.msg;
    for (let atom of session.resList) {
    console.log('sending ' + data);
        atom.send({data});
    }
    session.resList = [];
});
```
Client 에서 오는 요청을 session.resList에 저장해놓고
pythonServer에서 order가 오면 Client들에게 보냄
```j올
//client side
function resMsg() {
console.log('resMSG');
 axios.get('http://localhost:3000/msg')
  .then((res) => {
  if(res.data.data == 'play' && !isPlayed){
    player.playVideo();
    isPlayed = true;
  }
  resMsg();
  })
  .catch((res) => {
      console.log('get fail');
      setTimeout(resMsg, 5000);
  })
```
Server로부터 데이터를 받은후 곧바로 다시 요청을 보냄.
에러시 일정시간후 다시 보냄



### Youtube API
1.API key 발급
2.Iframe API -> youtube 영상 컨트롤
3.Data API -> 필요한 영상 search가능

```js
//연합뉴스채널의 뉴스 20가지를 뽑아오기
var optionParams={
q:"뉴스",
part:"id",
channelId:"UCTHCOPwqNfZ0uiKOvFyhGwg",
key:write your API key here,
order:"date",
type:"video",
maxResults:20,
regionCode:"KR",
videoDuration:"short"
};

//한글을 검색어로 전달하기 위해선 url encoding 필요!
optionParams.q=encodeURI(optionParams.q);

var url="https://www.googleapis.com/youtube/v3/search?";
for(var option in optionParams){
url+=option+"="+optionParams[option]+"&";
}

//url의마지막에 붙어있는 & 정리
url=url.substr(0, url.length-1);
var vidList = []; 

    function getVideoList(){
      axios.get(url)
        .then((res) => {
var vid = res.data.items;

for(var content in vid){
vidList.push(vid[content].id.videoId)
}
console.log(vidList);
        })
        .catch((res) => {
            console.log('failed to load VideoList');
        })
    }
getVideoList();
```
