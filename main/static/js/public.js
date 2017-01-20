$(function(){
	/*彈窗使用 start*/
	$( "#html-content" ).click(function() {
		  $.sweetModal({
			title: '客戶服務條款',
			content: '客戶服務條款 <b>內容</b>'
			});
	});
	$( "#html-privacy" ).click(function() {
	  $.sweetModal({
		title: '客戶隱私權政策',
		content: '客戶隱私權政策 <b>內容</b>'
		});
	});
	$( ".changeBtn" ).click(function() {
	  
	});
	/*彈窗使用 End*/
	
	/*清除欄位值 start*/
	$( ".clearBtn" ).click(function() {
		$( ".sky-form" ).find( "input" ).attr("value", "");
	});
	/*清除欄位值 End*/
	
	/*確認欄位是否未填 start*/
	$('.changeBtn').click(function(){
        var passwdO=$(".passwordOld").val(), passwdN=$(".passwordNew").val(), passwdC=$(".passwordCon").val();
        if( passwdC=='' || passwdN=='' || passwdO=='' ){
            alert("提醒: \r\n 資料輸入不全!");
            return false;
        }else{
        	$.sweetModal({
			content: '修改成功',
			icon: $.sweetModal.ICON_SUCCESS
		});
        	var speed = 2000;
			setTimeout("history.back()", speed);
			function goto() {
			    location = "member.html";
			}
        }
	});
	/*確認欄位是否未填 End*/

});