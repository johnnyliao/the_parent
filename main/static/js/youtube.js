$(function(){

	function c(){
		var date_id=$('.pVideoLink"').attr('href').match(/[^/]*$/)[0];
	}
    $(".pVideoLink").click(function () {
    	alert("test");

		event.preventDefault();
	});

});
