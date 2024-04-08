var nav =document.getElementById('homenav')
		var scroll_y
		addEventListener("scroll",()=>{
			 scroll_y= window.scrollY
			if (scroll_y>150) {
				nav.style.backgroundColor='rgb(189,0,0,0.8)'
				nav.style.transition='0.3s linear'
			}else{
				nav.style.backgroundColor='rgb(0,0,0,0)'
				nav.style.transition='0.3s linear'
			}
		});