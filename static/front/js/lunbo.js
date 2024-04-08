		// 无缝轮播
		let oleft = document.querySelector('.left');//获取左按钮
    	let oright = document.querySelector('.right');
    	let oimglist = document.querySelector('.img-list');

    	var count=5
    	var nowing=1
    	//克隆第一张图片用于 跳5
    	let clonefirstimg = oimglist.firstElementChild.cloneNode();
    	oimglist.appendChild(clonefirstimg);

    	let index = 0;//索引
        let lock = true;
    	function rightbtn(){
            if(!lock) return;
    		index++;//控制图片
    		oimglist.style.left=index * -650 + "px";
    		oimglist.style.transition="0.5s ease";

    		if(index===5){
    			index=0;
    			setTimeout(()=>{
    				oimglist.style.left=0;
    				oimglist.style.transition= "none";
    			},500);
    		}
    		setcircle();
            lock=false;
            setTimeout(()=>{
                lock=true;
            },500);
    	}
    	//右按钮单击事件调用 向右方向轮播
    	oright.addEventListener("click",rightbtn);

    	function leftbtn(){
             if(!lock) return;
    		index--;//控制图
    		if(index===-1){
    			oimglist.style.left=5*  -650 + "px";//直接切换到加图
    			oimglist.style.transition="none";



    			index=4
    			setTimeout(()=>{
    				oimglist.style.left=index * -650 + "px";
    				oimglist.style.transition= "0.5s ease";



    			},0);
    		}else{
    			oimglist.style.left= index * -650 + "px";


    		}
    		setcircle();
            lock=false;
            setTimeout(()=>{
                lock=true;
            },500);
    	}

    	oleft.addEventListener("click",leftbtn);

    	//获取圆点
    	const circles= document.querySelectorAll(".circle");

    	//圆点变色
    	function setcircle(){
    		for(let i= 0; i < circles.length ; i++){
    			if( i === index){
    				circles[i].classList.add("active");
    			}else{
    				circles[i].classList.remove("active");
    			}
    		}
    	}

    	//单击远点 切换图片
    	const ocircle =document.querySelector(".circle-list");
    	ocircle.addEventListener("click",(e)=>{
    		//单击到原点上时
    		if(e.target.nodeName.toLowerCase()=== "li"){
    			const n = Number(e.target.getAttribute("data-n"));
    			index=n;
    			setcircle();
    			oimglist.style.transtion="0.5s ease";
    			oimglist.style.left= index* -650 +"px";


    		}
    	});
    	let auto =setInterval(rightbtn,2000);
    	const owrap =document.getElementById("wrap");

    	owrap.addEventListener("mouseenter",()=>{
    		clearInterval(auto);
    	});
    	owrap.addEventListener("mouseleave",()=>{
    		clearInterval(auto);
    		auto =setInterval(rightbtn,2000);
    	})