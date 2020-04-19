$(function(){
	var user = $('#user').val()
	var websocket = new WebSocket("ws://" + location.host + "/chat/?username=" + user)
	var chatwindow = document.getElementById('t-box')
	websocket.onmessage = function(e){
		data = $.parseJSON(e.data)
		if(data['user']=='sys'){
			$('#t-box').append("<p style='text-align: center; color: #FF5449; margin: 0; padding: 0;'>" + data['message'] + "</p>")
		}else if(data['user']==user){
			$('#t-box').append("<p style='text-align: left; color: #50A2A7; margin: 0; padding: 0;'>" + "[ " + user + " ]" +" " + data['message'] + "</p>")
		}else{
			$('#t-box').append("<p style='text-align: left; margin: 0; padding: 0;'>" + "[ " +  data['user'] + " ]" + " " + data['message'] + "</p>")
		}
		chatwindow.scrollTop = chatwindow.scrollHeight
	}
	$('#btn').click(function(){
		if($('#i-box').val()!=""){
			websocket.send($('#i-box').val())
			$('#i-box').val("")
		}	
	})
})
