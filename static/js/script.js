$(function(){

	$('button').click(function() {
		var data = {
			"message" : $("#message").val()
		};


		$('.chatdiv').append("<div class='row' style='margin: 5px 0px'> <div class='col-sm-offset-4 col-sm-8 text-right'> <div class='sent text-left'>"+data.message+"</div> </div> </div>");
		$(".chatdiv").animate({ scrollTop: $('.chatdiv').prop("scrollHeight")}, 1000);
		$("#message").val("");

/*		$.post("/",data,function(res){
			console.log(res)
			$('.chatdiv').append("<div class='row' style='margin: 5px 0px'> <div class='col-sm-8 text-left'> <div class='received text-left'>"+res+"</div> </div> </div>");
			$(".chatdiv").animate({ scrollTop: $('.chatdiv').prop("scrollHeight")}, 1000);

		});
*/
		const client = new ApiAi.ApiAiClient({accessToken: '326dceb2db07464bbe884f40a348ab5d'});
		let promise = client.textRequest(data.message);

		promise
		    .then(handleResponse)
    		.catch(heandleError);

		function handleResponse(serverResponse) {
		        console.log(serverResponse);
		        var res = serverResponse.result.fulfillment.speech;
		        $('.chatdiv').append("<div class='row' style='margin: 5px 0px'> <div class='col-sm-8 text-left'> <div class='received text-left'>"+res+"</div> </div> </div>");
				$(".chatdiv").animate({ scrollTop: $('.chatdiv').prop("scrollHeight")}, 1000);

		}
		function heandleError(serverError) {
		        console.log(serverError);
		}

	});

	$( "#myform" ).submit(function( event ) {

		$('button').trigger("click");
	  	event.preventDefault();
	});
});
