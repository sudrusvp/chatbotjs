$(function(){

	var sentHead = "<div class='row' style='margin: 5px 0px'> <div class='col-sm-offset-4 col-sm-8 text-right'> <div class='sent text-left'>";
	var receivedHead = "<div class='row' style='margin: 5px 0px'> <div class='col-sm-8 text-left'> <div class='received text-left'>";
	var tail = "</div> </div> </div>";

	
	$('button').click(function() {
		var data = {
			"message" : $("#message").val()
		};


		$('.chatdiv').append(sentHead+data.message+tail);
		$(".chatdiv").animate({ scrollTop: $('.chatdiv').prop("scrollHeight")}, 1000);
		$("#message").val("");

		$.post("/",data,function(res){
			console.log(res)
			$('.chatdiv').append(receivedHead+res+tail);
			$(".chatdiv").animate({ scrollTop: $('.chatdiv').prop("scrollHeight")}, 1000);

		});
		
		/*const client = new ApiAi.ApiAiClient({accessToken: '6d2145bdf1b4463c86d5c6bcc2f05b9c', sessionId : "session1"});
		let promise = client.textRequest(data.message);
		
		promise
		    .then(handleResponse)
    		.catch(heandleError);

		function handleResponse(serverResponse) {
		        console.log(serverResponse);
		        var res = serverResponse.result.fulfillment.speech;
		        $('.chatdiv').append(receivedHead+res+tail);
				$(".chatdiv").animate({ scrollTop: $('.chatdiv').prop("scrollHeight")}, 1000);

		}
		function heandleError(serverError) {
		        console.log(serverError);
		}
*/

	});

	$( "#myform" ).submit(function( event ) {

		$('button').trigger("click");
	  	event.preventDefault();
	});
});
