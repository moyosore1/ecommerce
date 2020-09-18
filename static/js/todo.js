function addToList(){
	userInput = document.getElementById('myInput').value
	url = '/addtolist/'


	let xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function(){
		if(this.readyState == 4 && this.status == 200){
			responseData = JSON.parse(this.responseText)
			document.getElementById('myUL').innerHTML += "<li data-item_id="+responseData[1]+">"+responseData[0]+"</li>"
			document.getElementById('myInput').value = ''
		}
	};
	xhttp.open("POST", url, true)
	xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
	xhttp.setRequestHeader('X-CSRFTOKEN', csrftoken)
	xhttp.send('userInput='+userInput)

}

let unorderedList = document.getElementById('myUL')
let items = unorderedList.getElementsByTagName('li')
deleteURL = '/delete/'
for(let i = 0; i < items.length; i++){
	items[i].addEventListener('click', function(){
		this.style.textDecoration ='line-through'
		item_id = this.dataset.item_id
		item = this
		let xhttp = new XMLHttpRequest()
		xhttp.onreadystatechange = function(){
			if(this.readyState == 4 && this.status == 200){
				item.style.display = 'none'
			}
		}
		xhttp.open('POST', deleteURL, true)
		xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded')
		xhttp.setRequestHeader('X-CSRFTOKEN', csrftoken)
		xhttp.send('item_id='+item_id)
		
	})
}